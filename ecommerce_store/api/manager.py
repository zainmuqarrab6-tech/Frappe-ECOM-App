import frappe
from frappe import _
from frappe.utils.password import update_password
import secrets

def _check_admin_permission():
    """
    Security gatekeeper: Ensures caller is authenticated as Administrator or System Manager.
    """
    if frappe.session.user == "Guest":
        frappe.throw(_("Authentication required. Please log in as an administrator."), frappe.PermissionError)
    roles = frappe.get_roles()
    if "System Manager" not in roles and frappe.session.user != "Administrator":
        frappe.throw(_("Unauthorized: Administrator permissions required."), frappe.PermissionError)

@frappe.whitelist(allow_guest=True)
def admin_login(usr, pwd):
    """
    Authenticates store manager with username/email and password.
    Returns session details and confirms Administrator / System Manager role.
    """
    try:
        login_manager = frappe.auth.LoginManager()
        login_manager.authenticate(user=usr, pwd=pwd)
        login_manager.post_login()

        user = frappe.session.user
        roles = frappe.get_roles(user)
        is_manager = "System Manager" in roles or user == "Administrator"

        if not is_manager:
            return {
                "status": "error",
                "message": _("Access denied: This account does not have store manager privileges.")
            }

        return {
            "status": "success",
            "message": _("Welcome back! Manager authenticated."),
            "data": {
                "user": user,
                "full_name": frappe.db.get_value("User", user, "full_name") or user,
                "role": "Store Administrator",
                "session_id": frappe.session.sid
            }
        }
    except frappe.AuthenticationError:
        return {"status": "error", "message": _("Incorrect username or password.")}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def setup_hostinger_email(pwd="GharMart786@"):
    """
    Configures official Hostinger SMTP Email Account for store notifications.
    """
    try:
        # Check if already exists
        if frappe.db.exists("Email Account", "MyGharMart Store"):
            doc = frappe.get_doc("Email Account", "MyGharMart Store")
        elif frappe.db.exists("Email Account", {"email_id": "info@mygharmart.store"}):
            doc = frappe.get_doc("Email Account", {"email_id": "info@mygharmart.store"})
        else:
            doc = frappe.new_doc("Email Account")
            doc.email_account_name = "MyGharMart Store"

        doc.email_id = "info@mygharmart.store"
        doc.smtp_server = "smtp.hostinger.com"
        doc.smtp_port = 465
        doc.use_ssl = 1
        doc.use_tls = 0
        doc.enable_outgoing = 1
        doc.default_outgoing = 1
        doc.always_use_account_email_id_as_sender = 1
        doc.password = pwd
        doc.enable_incoming = 0
        doc.save(ignore_permissions=True)

        # Update Store Settings
        settings = frappe.get_doc("Store Settings")
        settings.store_name = "MyGharMart"
        settings.store_email = "info@mygharmart.store"
        settings.save(ignore_permissions=True)

        frappe.db.commit()

        return {
            "status": "success",
            "message": "Hostinger SMTP Email Account successfully configured as default outgoing!"
        }
    except Exception as e:
        frappe.log_error("setup_hostinger_email error", str(e))
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def admin_signup(full_name, email, password, phone=None, frontend_url=None, **kwargs):
    """
    Registers a new store administrator request.
    Creates disabled Frappe User and dispatches email verification link.
    """
    try:
        full_name = (full_name or "").strip()
        email = (email or "").strip().lower()
        password = (password or "").strip()

        if not full_name or not email or not password:
            return {"status": "error", "message": _("Full Name, Email and Password are required.")}

        if len(password) < 6:
            return {"status": "error", "message": _("Password must be at least 6 characters long.")}

        # Ensure verification table exists in MariaDB
        frappe.db.sql("""
            CREATE TABLE IF NOT EXISTS `tabAdmin Verification` (
                `email` VARCHAR(140) PRIMARY KEY,
                `token` VARCHAR(255) NOT NULL,
                `full_name` VARCHAR(140),
                `created_at` DATETIME,
                `verified` INT(1) DEFAULT 0
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

        # Check existing user
        if frappe.db.exists("User", email):
            roles = frappe.get_roles(email)
            if "System Manager" in roles:
                return {
                    "status": "error",
                    "message": _("An administrator account with this email already exists. Please log in.")
                }
            # Update password for pending unverified user
            update_password(email, password)
        else:
            # Create user in unverified state (enabled=0)
            user = frappe.get_doc({
                "doctype": "User",
                "email": email,
                "first_name": full_name,
                "enabled": 0,
                "user_type": "System User",
                "send_welcome_email": 0
            })
            user.insert(ignore_permissions=True)
            update_password(email, password)

        # Generate secure random token
        token = secrets.token_urlsafe(32)
        now = frappe.utils.now_datetime()

        frappe.db.sql("""
            INSERT INTO `tabAdmin Verification` (email, token, full_name, created_at, verified)
            VALUES (%s, %s, %s, %s, 0)
            ON DUPLICATE KEY UPDATE token=%s, created_at=%s, verified=0
        """, (email, token, full_name, now, token, now))
        frappe.db.commit()

        # Build verification URL dynamically matching the user's actual browser domain & port
        if frontend_url and frontend_url.startswith("http"):
            base_url = frontend_url.rstrip("/")
        else:
            origin = frappe.get_request_header("Origin") or frappe.get_request_header("Referer")
            if origin:
                from urllib.parse import urlparse
                parsed = urlparse(origin)
                base_url = f"{parsed.scheme}://{parsed.netloc}"
            else:
                base_url = "http://192.168.90.112:3000"

        verification_url = f"{base_url}/#verify-admin?token={token}"

        # Dispatch email via Frappe notification engine
        subject = _("Verify your Store Administrator Account - MyGharMart")
        email_html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; border: 1px solid #e2e8f0; border-radius: 12px; background: #ffffff;">
            <div style="background: linear-gradient(135deg, #4f46e5, #7c3aed); padding: 20px; border-radius: 8px; text-align: center; color: white;">
                <h1 style="margin: 0; font-size: 22px;">MyGharMart Administrator Access</h1>
            </div>
            <div style="padding: 24px 8px; color: #334155;">
                <p style="font-size: 16px;">Hello <strong>{full_name}</strong>,</p>
                <p>An administrator registration request has been submitted for your email address to access the <strong>MyGharMart E-commerce</strong> management portal.</p>
                <p>To confirm your identity and activate your administrator privileges (Products, Orders, Inventory, Discounts, Settings), please click the button below:</p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{verification_url}" style="background-color: #4f46e5; color: #ffffff; padding: 14px 28px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 15px; display: inline-block;">
                        Verify &amp; Activate Administrator Account
                    </a>
                </div>
                <p style="font-size: 13px; color: #64748b;">Or copy and paste this verification URL into your browser:</p>
                <p style="font-size: 12px; color: #4f46e5; word-break: break-all;">{verification_url}</p>
            </div>
            <div style="border-top: 1px solid #e2e8f0; padding-top: 16px; font-size: 12px; color: #94a3b8; text-align: center;">
                MyGharMart E-Commerce &bull; Automated Security Gateway
            </div>
        </div>
        """
        try:
            frappe.sendmail(
                recipients=[email],
                subject=subject,
                message=email_html,
                now=True
            )
        except Exception as mail_err:
            frappe.log_error("admin_signup sendmail error", str(mail_err))

        return {
            "status": "success",
            "message": _("Registration successful! A verification email has been sent to {0}. Please click the link to activate your administrator access.").format(email),
            "data": {
                "email": email,
                "full_name": full_name,
                "token": token,
                "verification_url": verification_url
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def verify_admin_email(token):
    """
    Verifies token, enables Frappe User, assigns System Manager role,
    and grants full administrative access.
    """
    try:
        if not token:
            return {"status": "error", "message": _("Verification token is required.")}

        # Query verification record
        records = frappe.db.sql("""
            SELECT email, full_name, verified FROM `tabAdmin Verification` WHERE token = %s
        """, (token,), as_dict=True)

        if not records:
            return {"status": "error", "message": _("Invalid or expired verification token.")}

        rec = records[0]
        email = rec["email"]
        full_name = rec["full_name"]

        if not frappe.db.exists("User", email):
            return {"status": "error", "message": _("User account not found for this verification.")}

        user = frappe.get_doc("User", email)
        user.enabled = 1
        user.save(ignore_permissions=True)

        # Assign System Manager role
        user.add_roles("System Manager")

        # Create or update Store Customer record
        if not frappe.db.exists("Store Customer", {"email": email}):
            cust = frappe.get_doc({
                "doctype": "Store Customer",
                "customer_name": full_name or user.first_name,
                "email": email,
                "user": user.name
            })
            cust.insert(ignore_permissions=True)

        # Mark as verified
        frappe.db.sql("""
            UPDATE `tabAdmin Verification` SET verified = 1 WHERE email = %s
        """, (email,))
        frappe.db.commit()

        return {
            "status": "success",
            "message": _("Administrator account verified successfully! You now have full store management permissions."),
            "data": {
                "email": email,
                "full_name": full_name or user.first_name,
                "verified": True
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def get_dashboard_stats():
    """
    Calculates key store metrics for the white-label Admin Dashboard.
    """
    try:
        _check_admin_permission()

        # Total Sales & Orders (excluding cancelled)
        total_sales = frappe.db.sql("""
            SELECT COALESCE(SUM(grand_total), 0) FROM `tabStore Order`
            WHERE order_status NOT IN ('Cancelled')
        """)[0][0] or 0.0

        total_orders = frappe.db.count("Store Order")
        pending_orders = frappe.db.count("Store Order", {"order_status": "Pending"})
        confirmed_orders = frappe.db.count("Store Order", {"order_status": "Confirmed"})
        shipped_orders = frappe.db.count("Store Order", {"order_status": "Shipped"})
        delivered_orders = frappe.db.count("Store Order", {"order_status": "Delivered"})

        # Products & Inventory
        total_products = frappe.db.count("Product")
        active_products = frappe.db.count("Product", {"is_active": 1})
        low_stock_products = frappe.db.count("Product", {
            "is_active": 1,
            "track_inventory": 1,
            "stock_quantity": ["<=", 5]
        })

        # Customers & Reviews
        total_customers = frappe.db.count("Store Customer")
        total_reviews = frappe.db.count("Product Review")
        pending_reviews = frappe.db.count("Product Review", {"status": "Pending"})

        # Recent Orders (Latest 6)
        recent_orders = frappe.get_all(
            "Store Order",
            fields=["name", "customer_name", "customer_phone", "grand_total", "order_status", "creation"],
            order_by="creation desc",
            limit=6
        )

        return {
            "status": "success",
            "data": {
                "total_sales": float(total_sales),
                "total_orders": int(total_orders),
                "pending_orders": int(pending_orders),
                "confirmed_orders": int(confirmed_orders),
                "shipped_orders": int(shipped_orders),
                "delivered_orders": int(delivered_orders),
                "total_products": int(total_products),
                "active_products": int(active_products),
                "low_stock_products": int(low_stock_products),
                "total_customers": int(total_customers),
                "total_reviews": int(total_reviews),
                "pending_reviews": int(pending_reviews),
                "recent_orders": recent_orders
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def get_admin_orders(status=None, search=None, page=1, limit=20):
    """
    Returns full order records with line items for store management.
    """
    try:
        _check_admin_permission()

        page = int(page)
        limit = min(int(limit), 100)
        start = (page - 1) * limit

        filters = {}
        if status and status != "all":
            filters["order_status"] = status

        or_filters = []
        if search:
            pattern = f"%{search.strip()}%"
            or_filters = [
                ["name", "like", pattern],
                ["customer_name", "like", pattern],
                ["customer_phone", "like", pattern],
                ["customer_email", "like", pattern]
            ]

        orders = frappe.get_all(
            "Store Order",
            filters=filters,
            or_filters=or_filters if or_filters else None,
            fields=[
                "name", "creation", "order_status", "payment_status", "payment_method",
                "customer_name", "customer_phone", "customer_email",
                "shipping_address", "shipping_city", "subtotal", "shipping_fee",
                "discount_amount", "grand_total", "tracking_courier", "tracking_number"
            ],
            order_by="creation desc",
            start=start,
            page_length=limit
        )

        # Attach line items for each order
        for o in orders:
            items = frappe.get_all(
                "Store Order Item",
                filters={"parent": o["name"]},
                fields=["product", "product_name", "sku", "price", "quantity", "total", "attributes_summary"]
            )
            o["items"] = items

        total_count = frappe.db.count("Store Order", filters=filters)

        return {
            "status": "success",
            "data": orders,
            "total_count": total_count,
            "page": page,
            "limit": limit
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def update_order_status(order_id, status, tracking_courier=None, tracking_number=None):
    """
    Updates order status and courier tracking info. If status becomes Cancelled, restores stock.
    """
    try:
        _check_admin_permission()

        if not frappe.db.exists("Store Order", order_id):
            return {"status": "error", "message": _("Order not found")}

        order = frappe.get_doc("Store Order", order_id)
        valid_statuses = ["Pending", "Confirmed", "Shipped", "Delivered", "Cancelled"]
        if status not in valid_statuses:
            return {"status": "error", "message": _("Invalid order status: {0}").format(status)}

        if status == "Cancelled" and order.order_status != "Cancelled":
            order.cancel_order("Cancelled by Store Manager via Custom Dashboard")
        else:
            order.order_status = status
            if tracking_courier is not None:
                order.tracking_courier = tracking_courier
            if tracking_number is not None:
                order.tracking_number = tracking_number
            order.save(ignore_permissions=True)

        frappe.db.commit()

        return {
            "status": "success",
            "message": _("Order {0} status updated to {1}").format(order_id, status),
            "order_status": order.order_status
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def get_admin_products(search=None, category=None, page=1, limit=50):
    """
    Returns full product list including inactive products for management.
    """
    try:
        _check_admin_permission()

        page = int(page)
        limit = min(int(limit), 100)
        start = (page - 1) * limit

        filters = {}
        if category and category != "all":
            filters["category"] = category

        or_filters = []
        if search:
            pattern = f"%{search.strip()}%"
            or_filters = [
                ["title", "like", pattern],
                ["sku", "like", pattern],
                ["name", "like", pattern]
            ]

        products = frappe.get_all(
            "Product",
            filters=filters,
            or_filters=or_filters if or_filters else None,
            fields=[
                "name", "title", "route_slug", "price", "compare_at_price",
                "stock_quantity", "is_in_stock", "category", "brand",
                "is_active", "is_featured", "primary_image", "sku", "creation"
            ],
            order_by="creation desc",
            start=start,
            page_length=limit
        )

        total_count = frappe.db.count("Product", filters=filters)

        return {
            "status": "success",
            "data": products,
            "total_count": total_count,
            "page": page,
            "limit": limit
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def save_product(product_id=None, title=None, price=None, compare_at_price=None,
                 stock_quantity=None, category=None, brand=None, short_description=None,
                 description=None, primary_image=None, sku=None, is_active=1, is_featured=0, **kwargs):
    """
    Creates a new product or updates an existing product with full attributes.
    """
    try:
        _check_admin_permission()

        if not title:
            return {"status": "error", "message": _("Product title is required")}

        price = float(price or 0)
        stock_quantity = int(stock_quantity or 0)
        compare_at_price = float(compare_at_price) if compare_at_price else 0.0

        if product_id and frappe.db.exists("Product", product_id):
            prod = frappe.get_doc("Product", product_id)
            prod.title = title
            prod.price = price
            prod.compare_at_price = compare_at_price
            prod.stock_quantity = stock_quantity
            prod.is_in_stock = 1 if stock_quantity > 0 else 0
            if category:
                prod.category = category
            if brand is not None:
                prod.brand = brand
            if short_description is not None:
                prod.short_description = short_description
            if description is not None:
                prod.description = description
            if primary_image is not None:
                prod.primary_image = primary_image
            if sku is not None:
                prod.sku = sku
            prod.is_active = int(is_active)
            prod.is_featured = int(is_featured)
            prod.save(ignore_permissions=True)
            action = "updated"
        else:
            prod = frappe.get_doc({
                "doctype": "Product",
                "naming_series": "PROD-.#####",
                "title": title,
                "price": price,
                "compare_at_price": compare_at_price,
                "stock_quantity": stock_quantity,
                "is_in_stock": 1 if stock_quantity > 0 else 0,
                "category": category or "electronics",
                "brand": brand or "",
                "short_description": short_description or "",
                "description": description or "",
                "primary_image": primary_image or "",
                "sku": sku or "",
                "is_active": int(is_active),
                "is_featured": int(is_featured),
                "track_inventory": 1,
                "status": "Active" if is_active else "Draft"
            })
            prod.insert(ignore_permissions=True)
            action = "created"

        frappe.db.commit()

        return {
            "status": "success",
            "message": _("Product '{0}' {1} successfully").format(prod.title, action),
            "data": {
                "id": prod.name,
                "title": prod.title,
                "price": prod.price,
                "stock_quantity": prod.stock_quantity,
                "is_active": prod.is_active
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def delete_product(product_id):
    """
    Deletes a product by ID.
    """
    try:
        _check_admin_permission()

        if not frappe.db.exists("Product", product_id):
            return {"status": "error", "message": _("Product not found")}

        title = frappe.db.get_value("Product", product_id, "title") or product_id
        frappe.delete_doc("Product", product_id, ignore_permissions=True)
        frappe.db.commit()

        return {"status": "success", "message": _("Product '{0}' deleted successfully").format(title)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def update_product_stock(product_id, stock_quantity):
    """
    Quick inline stock updater for the admin dashboard.
    """
    try:
        _check_admin_permission()

        if not frappe.db.exists("Product", product_id):
            return {"status": "error", "message": _("Product not found")}

        prod = frappe.get_doc("Product", product_id)
        new_qty = max(0, int(stock_quantity))
        old_qty = prod.stock_quantity
        prod.stock_quantity = new_qty
        prod.is_in_stock = 1 if new_qty > 0 else 0
        prod.save(ignore_permissions=True)

        prod.add_comment("Info", _("Stock adjusted via Manager Dashboard: {0} -> {1}").format(old_qty, new_qty))
        frappe.db.commit()

        return {
            "status": "success",
            "message": _("Stock updated"),
            "stock_quantity": prod.stock_quantity
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ==========================================
# CATEGORIES MANAGEMENT
# ==========================================

@frappe.whitelist(allow_guest=True)
def get_admin_categories():
    """
    Returns all product categories with associated product count and status.
    """
    try:
        _check_admin_permission()

        categories = frappe.get_all(
            "Product Category",
            fields=["name", "category_name", "route_slug", "category_image", "is_active", "sort_order", "description"],
            order_by="sort_order asc, category_name asc"
        )

        for cat in categories:
            cat["product_count"] = frappe.db.count("Product", {"category": cat["route_slug"]})

        return {"status": "success", "data": categories}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def save_category(category_name, route_slug=None, description=None, category_image=None, is_active=1, sort_order=0):
    """
    Creates or updates a product category.
    """
    try:
        _check_admin_permission()

        category_name = (category_name or "").strip()
        if not category_name:
            return {"status": "error", "message": _("Category name is required")}

        if not route_slug:
            route_slug = frappe.scrub(category_name).replace("_", "-")

        if frappe.db.exists("Product Category", route_slug):
            cat = frappe.get_doc("Product Category", route_slug)
            cat.category_name = category_name
            if description is not None:
                cat.description = description
            if category_image is not None:
                cat.category_image = category_image
            cat.is_active = int(is_active)
            cat.sort_order = int(sort_order or 0)
            cat.save(ignore_permissions=True)
            action = "updated"
        else:
            cat = frappe.get_doc({
                "doctype": "Product Category",
                "category_name": category_name,
                "route_slug": route_slug,
                "description": description or "",
                "category_image": category_image or "",
                "is_active": int(is_active),
                "sort_order": int(sort_order or 0)
            })
            cat.insert(ignore_permissions=True)
            action = "created"

        frappe.db.commit()

        return {
            "status": "success",
            "message": _("Category '{0}' {1} successfully").format(category_name, action),
            "data": {
                "route_slug": cat.route_slug,
                "category_name": cat.category_name,
                "is_active": cat.is_active
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def delete_category(category_id):
    """
    Deletes a product category if no active products are linked to it.
    """
    try:
        _check_admin_permission()

        if not frappe.db.exists("Product Category", category_id):
            return {"status": "error", "message": _("Category not found")}

        product_count = frappe.db.count("Product", {"category": category_id})
        if product_count > 0:
            return {
                "status": "error",
                "message": _("Cannot delete category with {0} linked products. Please reassign products first.").format(product_count)
            }

        frappe.delete_doc("Product Category", category_id, ignore_permissions=True)
        frappe.db.commit()

        return {"status": "success", "message": _("Category deleted successfully")}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ==========================================
# COUPONS & DISCOUNTS MANAGEMENT
# ==========================================

@frappe.whitelist(allow_guest=True)
def get_admin_coupons():
    """
    Returns all discount coupons with usage metrics.
    """
    try:
        _check_admin_permission()

        coupons = frappe.get_all(
            "Store Coupon",
            fields=[
                "name", "coupon_code", "discount_type", "discount_value",
                "is_active", "min_order_amount", "max_discount_amount",
                "valid_from", "valid_upto", "usage_limit", "times_used", "description"
            ],
            order_by="creation desc"
        )

        return {"status": "success", "data": coupons}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def save_coupon(coupon_code, discount_type="Percentage", discount_value=0,
                min_order_amount=0, max_discount_amount=0, valid_from=None,
                valid_upto=None, usage_limit=0, is_active=1, description=None):
    """
    Creates or updates a promotional discount coupon.
    """
    try:
        _check_admin_permission()

        code = (coupon_code or "").strip().upper()
        if not code:
            return {"status": "error", "message": _("Coupon code is required")}

        val = float(discount_value or 0)
        if val <= 0:
            return {"status": "error", "message": _("Discount value must be greater than zero")}

        if frappe.db.exists("Store Coupon", code):
            coupon = frappe.get_doc("Store Coupon", code)
            coupon.discount_type = discount_type
            coupon.discount_value = val
            coupon.min_order_amount = float(min_order_amount or 0)
            coupon.max_discount_amount = float(max_discount_amount or 0)
            if valid_from:
                coupon.valid_from = valid_from
            if valid_upto:
                coupon.valid_upto = valid_upto
            coupon.usage_limit = int(usage_limit or 0)
            coupon.is_active = int(is_active)
            if description is not None:
                coupon.description = description
            coupon.save(ignore_permissions=True)
            action = "updated"
        else:
            coupon = frappe.get_doc({
                "doctype": "Store Coupon",
                "coupon_code": code,
                "discount_type": discount_type,
                "discount_value": val,
                "min_order_amount": float(min_order_amount or 0),
                "max_discount_amount": float(max_discount_amount or 0),
                "valid_from": valid_from or None,
                "valid_upto": valid_upto or None,
                "usage_limit": int(usage_limit or 0),
                "times_used": 0,
                "is_active": int(is_active),
                "description": description or ""
            })
            coupon.insert(ignore_permissions=True)
            action = "created"

        frappe.db.commit()

        return {
            "status": "success",
            "message": _("Coupon '{0}' {1} successfully").format(code, action),
            "data": {
                "coupon_code": coupon.coupon_code,
                "discount_type": coupon.discount_type,
                "discount_value": coupon.discount_value,
                "is_active": coupon.is_active
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def delete_coupon(coupon_code):
    """
    Deletes a promotional coupon.
    """
    try:
        _check_admin_permission()

        if not frappe.db.exists("Store Coupon", coupon_code):
            return {"status": "error", "message": _("Coupon not found")}

        frappe.delete_doc("Store Coupon", coupon_code, ignore_permissions=True)
        frappe.db.commit()

        return {"status": "success", "message": _("Coupon '{0}' deleted").format(coupon_code)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ==========================================
# CUSTOMERS DIRECTORY
# ==========================================

@frappe.whitelist(allow_guest=True)
def get_admin_customers(search=None, page=1, limit=50):
    """
    Returns customer records including total orders and lifetime spending.
    """
    try:
        _check_admin_permission()

        page = int(page)
        limit = min(int(limit), 100)
        start = (page - 1) * limit

        or_filters = []
        if search:
            pattern = f"%{search.strip()}%"
            or_filters = [
                ["customer_name", "like", pattern],
                ["email", "like", pattern],
                ["phone", "like", pattern]
            ]

        customers = frappe.get_all(
            "Store Customer",
            or_filters=or_filters if or_filters else None,
            fields=[
                "name", "customer_name", "email", "phone",
                "is_active", "total_orders_placed", "total_spent", "creation"
            ],
            order_by="creation desc",
            start=start,
            page_length=limit
        )

        total_count = frappe.db.count("Store Customer")

        return {
            "status": "success",
            "data": customers,
            "total_count": total_count,
            "page": page,
            "limit": limit
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ==========================================
# REVIEWS MODERATION
# ==========================================

@frappe.whitelist(allow_guest=True)
def get_admin_reviews(status=None, page=1, limit=50):
    """
    Returns product reviews for moderation (Pending, Approved, Rejected).
    """
    try:
        _check_admin_permission()

        page = int(page)
        limit = min(int(limit), 100)
        start = (page - 1) * limit

        filters = {}
        if status and status != "all":
            filters["status"] = status

        reviews = frappe.get_all(
            "Product Review",
            filters=filters,
            fields=[
                "name", "product", "customer_name", "customer_email",
                "rating", "status", "title", "review_text",
                "is_verified_buyer", "creation"
            ],
            order_by="creation desc",
            start=start,
            page_length=limit
        )

        # Attach product title for clarity
        for r in reviews:
            r["product_title"] = frappe.db.get_value("Product", r["product"], "title") or r["product"]

        total_count = frappe.db.count("Product Review", filters=filters)

        return {
            "status": "success",
            "data": reviews,
            "total_count": total_count,
            "page": page,
            "limit": limit
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def update_review_status(review_id, status):
    """
    Moderates a review: sets status to Approved, Rejected, or Pending.
    """
    try:
        _check_admin_permission()

        if not frappe.db.exists("Product Review", review_id):
            return {"status": "error", "message": _("Review not found")}

        valid_statuses = ["Pending", "Approved", "Rejected"]
        if status not in valid_statuses:
            return {"status": "error", "message": _("Invalid status: {0}").format(status)}

        frappe.db.set_value("Product Review", review_id, "status", status)
        frappe.db.commit()

        return {"status": "success", "message": _("Review marked as {0}").format(status)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def delete_review(review_id):
    """
    Deletes a review permanently.
    """
    try:
        _check_admin_permission()

        if not frappe.db.exists("Product Review", review_id):
            return {"status": "error", "message": _("Review not found")}

        frappe.delete_doc("Product Review", review_id, ignore_permissions=True)
        frappe.db.commit()

        return {"status": "success", "message": _("Review deleted successfully")}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ==========================================
# STORE SETTINGS MANAGEMENT
# ==========================================

@frappe.whitelist(allow_guest=True)
def get_admin_store_settings():
    """
    Returns store configuration parameters for editing in the Admin Dashboard.
    """
    try:
        _check_admin_permission()

        settings = frappe.get_single("Store Settings")
        return {
            "status": "success",
            "data": {
                "store_name": settings.store_name or "ProStore Ecommerce",
                "store_email": settings.store_email or "",
                "store_phone": settings.store_phone or "",
                "primary_domain": settings.primary_domain or "",
                "currency": settings.currency or "PKR",
                "currency_symbol": settings.currency_symbol or "Rs.",
                "default_shipping_fee": float(settings.default_shipping_fee or 0),
                "free_shipping_threshold": float(settings.free_shipping_threshold or 0),
                "express_shipping_fee": float(settings.express_shipping_fee or 0),
                "tax_percentage": float(settings.tax_percentage or 0),
                "prices_include_tax": bool(settings.prices_include_tax),
                "allow_cod": bool(settings.allow_cod),
                "cod_label": settings.cod_label or "Cash on Delivery (COD)",
                "allow_guest_checkout": bool(settings.allow_guest_checkout),
                "minimum_order_amount": float(settings.minimum_order_amount or 0)
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def save_admin_store_settings(store_name=None, store_email=None, store_phone=None,
                              primary_domain=None, currency=None, currency_symbol=None,
                              default_shipping_fee=None, free_shipping_threshold=None,
                              express_shipping_fee=None, tax_percentage=None,
                              prices_include_tax=None, allow_cod=None, cod_label=None,
                              allow_guest_checkout=None, minimum_order_amount=None):
    """
    Updates the single DocType 'Store Settings' with the provided store parameters.
    """
    try:
        _check_admin_permission()

        settings = frappe.get_doc("Store Settings")

        if store_name is not None:
            settings.store_name = store_name.strip()
        if store_email is not None:
            settings.store_email = store_email.strip()
        if store_phone is not None:
            settings.store_phone = store_phone.strip()
        if primary_domain is not None:
            settings.primary_domain = primary_domain.strip()
        if currency is not None:
            settings.currency = currency.strip()
        if currency_symbol is not None:
            settings.currency_symbol = currency_symbol.strip()
        if default_shipping_fee is not None:
            settings.default_shipping_fee = float(default_shipping_fee)
        if free_shipping_threshold is not None:
            settings.free_shipping_threshold = float(free_shipping_threshold)
        if express_shipping_fee is not None:
            settings.express_shipping_fee = float(express_shipping_fee)
        if tax_percentage is not None:
            settings.tax_percentage = float(tax_percentage)
        if prices_include_tax is not None:
            settings.prices_include_tax = 1 if prices_include_tax in [1, True, "1", "true"] else 0
        if allow_cod is not None:
            settings.allow_cod = 1 if allow_cod in [1, True, "1", "true"] else 0
        if cod_label is not None:
            settings.cod_label = cod_label.strip()
        if allow_guest_checkout is not None:
            settings.allow_guest_checkout = 1 if allow_guest_checkout in [1, True, "1", "true"] else 0
        if minimum_order_amount is not None:
            settings.minimum_order_amount = float(minimum_order_amount)

        settings.save(ignore_permissions=True)
        frappe.db.commit()

        return {
            "status": "success",
            "message": _("Store settings saved successfully"),
            "data": {
                "store_name": settings.store_name,
                "currency": settings.currency,
                "currency_symbol": settings.currency_symbol
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
