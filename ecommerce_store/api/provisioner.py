import os
import re
import json
import subprocess
import frappe
from frappe import _

RESERVED_SUBDOMAINS = {
    "admin", "administrator", "api", "app", "assets", "desk", "files",
    "frappe", "frappe-ecommerce", "login", "mail", "root", "sites",
    "static", "system", "test", "web", "www"
}

def _get_bench_path():
    """Returns absolute path to frappe-bench directory."""
    try:
        from frappe.utils import get_bench_path
        bench = get_bench_path()
        if bench and os.path.exists(bench):
            return bench
    except Exception:
        pass
    return "/home/zain/frappe-bench"

def _get_sites_path():
    """Returns absolute path to sites directory."""
    return os.path.join(_get_bench_path(), "sites")

def _sanitize_subdomain(subdomain):
    """Sanitizes and normalizes subdomain name."""
    if not subdomain:
        return ""
    clean = re.sub(r"[^a-z0-9-]", "", subdomain.lower().strip())
    clean = re.sub(r"-+", "-", clean).strip("-")
    return clean

@frappe.whitelist(allow_guest=True)
def check_subdomain_availability(subdomain):
    """
    Checks if a store subdomain is valid and available.
    """
    clean = _sanitize_subdomain(subdomain)
    if not clean:
        return {"available": False, "reason": _("Subdomain cannot be empty.")}
    
    if len(clean) < 3 or len(clean) > 30:
        return {"available": False, "reason": _("Subdomain must be between 3 and 30 characters.")}
    
    if clean in RESERVED_SUBDOMAINS:
        return {"available": False, "reason": _("This subdomain is reserved. Please choose another name.")}
    
    sites_path = _get_sites_path()
    site_candidate = f"{clean}.localhost"
    site_dir = os.path.join(sites_path, site_candidate)
    
    if os.path.exists(site_dir):
        return {"available": False, "subdomain": clean, "reason": _("Store subdomain is already taken.")}
    
    return {"available": True, "subdomain": clean, "site_name": site_candidate}

def initialize_new_store(store_name, admin_email, admin_password, admin_full_name=None):
    """
    Executed inside the new site database to set store settings,
    create the admin user, and seed starter categories and sample product.
    """
    from frappe.utils.password import update_password

    # 1. Update Store Settings
    if frappe.db.exists("Store Settings", "Store Settings"):
        s = frappe.get_doc("Store Settings", "Store Settings")
        s.store_name = store_name
        s.store_email = admin_email
        s.currency = "PKR"
        s.save(ignore_permissions=True)

    # 2. Setup Admin User if custom email
    if admin_email.lower() != "administrator":
        # Ensure Store Administrator role exists
        if not frappe.db.exists("Role", "Store Administrator"):
            r = frappe.new_doc("Role")
            r.role_name = "Store Administrator"
            r.desk_access = 1
            r.insert(ignore_permissions=True)

        if not frappe.db.exists("User", admin_email):
            user = frappe.get_doc({
                "doctype": "User",
                "email": admin_email,
                "first_name": admin_full_name or store_name,
                "enabled": 1,
                "user_type": "System User",
                "send_welcome_email": 0
            })
            user.insert(ignore_permissions=True)
        else:
            user = frappe.get_doc("User", admin_email)

        user.add_roles("System Manager", "Store Administrator")
        update_password(admin_email, admin_password)

    # 3. Seed starter categories
    starter_categories = [
        {"category_name": "Electronics", "route_slug": "electronics"},
        {"category_name": "Fashion & Apparel", "route_slug": "fashion-apparel"},
        {"category_name": "Home & Living", "route_slug": "home-living"}
    ]
    for cat in starter_categories:
        if not frappe.db.exists("Product Category", {"route_slug": cat["route_slug"]}):
            doc = frappe.get_doc({"doctype": "Product Category", **cat})
            doc.insert(ignore_permissions=True)

    # 4. Seed welcome starter product
    if not frappe.db.exists("Product", {"route_slug": "welcome-starter-product"}):
        prod = frappe.get_doc({
            "doctype": "Product",
            "title": "Sample Welcome Product",
            "route_slug": "welcome-starter-product",
            "category": "electronics",
            "price": 1499.0,
            "is_in_stock": 1,
            "stock_quantity": 50,
            "short_description": "Congratulations! Your store is live. Edit or delete this sample product in your Admin Dashboard."
        })
        prod.insert(ignore_permissions=True)

    frappe.db.commit()
    return {"status": "success"}

@frappe.whitelist(allow_guest=True)
def create_store(store_name, subdomain, admin_email, admin_password, admin_full_name=None):
    """
    SaaS Engine: Automatically provisions a brand new, isolated Frappe site with
    dedicated MariaDB database, installs ecommerce_store, and configures the store admin.
    """
    try:
        store_name = (store_name or "").strip()
        admin_email = (admin_email or "").strip().lower()
        admin_password = (admin_password or "").strip()
        admin_full_name = (admin_full_name or store_name).strip()

        if not store_name or not admin_email or not admin_password:
            return {"status": "error", "message": _("Store Name, Admin Email and Password are required.")}

        if len(admin_password) < 6:
            return {"status": "error", "message": _("Password must be at least 6 characters.")}

        # Validate subdomain
        availability = check_subdomain_availability(subdomain)
        if not availability.get("available"):
            return {"status": "error", "message": availability.get("reason")}

        clean_sub = availability["subdomain"]
        site_name = availability["site_name"]
        bench_dir = _get_bench_path()

        # Step 1: Run bench new-site via CLI in the bench context
        cmd = [
            "bench", "new-site", site_name,
            "--mariadb-root-password", "root123",
            "--admin-password", admin_password,
            "--install-app", "ecommerce_store"
        ]

        result = subprocess.run(
            cmd,
            cwd=bench_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=300
        )

        if result.returncode != 0:
            error_msg = result.stderr or result.stdout or "Bench new-site failed"
            frappe.log_error(f"Failed to provision site {site_name}", error_msg)
            return {"status": "error", "message": f"Site creation failed: {error_msg[-200:]}"}

        # Step 2: Configure site_config.json for Headless mode (allow_cors and ignore_csrf)
        site_config_path = os.path.join(_get_sites_path(), site_name, "site_config.json")
        if os.path.exists(site_config_path):
            with open(site_config_path, "r") as f:
                config = json.load(f)
            config["allow_cors"] = "*"
            config["ignore_csrf"] = 1
            with open(site_config_path, "w") as f:
                json.dump(config, f, indent=1)

        # Step 3: Run post-install configuration inside the new site using bench execute
        subprocess.run(
            [
                "bench", "--site", site_name, "execute",
                "ecommerce_store.api.provisioner.initialize_new_store",
                "--kwargs", json.dumps({
                    "store_name": store_name,
                    "admin_email": admin_email,
                    "admin_password": admin_password,
                    "admin_full_name": admin_full_name
                })
            ],
            cwd=bench_dir,
            timeout=60
        )

        return {
            "status": "success",
            "message": _("Store provisioned successfully!"),
            "data": {
                "store_name": store_name,
                "subdomain": clean_sub,
                "site_name": site_name,
                "admin_email": admin_email,
                "store_url": f"http://{clean_sub}.localhost:3000",
                "admin_url": f"http://{clean_sub}.localhost:3000/#admin"
            }
        }

    except Exception as e:
        frappe.log_error("Store Provisioning Exception", str(e))
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def list_provisioned_stores():
    """
    Returns list of all active provisioned store sites in this bench.
    """
    sites_path = _get_sites_path()
    stores = []
    
    if not os.path.exists(sites_path):
        return {"status": "success", "data": []}

    for item in sorted(os.listdir(sites_path)):
        site_folder = os.path.join(sites_path, item)
        site_config = os.path.join(site_folder, "site_config.json")
        
        if os.path.isdir(site_folder) and os.path.exists(site_config) and item != "assets":
            try:
                with open(site_config, "r") as f:
                    cfg = json.load(f)
                
                # Only include sites with ecommerce_store installed
                installed = cfg.get("installed_apps", [])
                if "ecommerce_store" in installed:
                    subdomain = item.replace(".localhost", "").replace(".mygharmart.store", "")
                    stores.append({
                        "site_name": item,
                        "subdomain": subdomain,
                        "is_default": item == "frappe-ecommerce.localhost",
                        "store_url": f"http://{item}:3000" if item != "frappe-ecommerce.localhost" else "http://localhost:3000",
                        "admin_url": f"http://{item}:3000/#admin" if item != "frappe-ecommerce.localhost" else "http://localhost:3000/#admin"
                    })
            except Exception:
                continue

    return {"status": "success", "data": stores}
