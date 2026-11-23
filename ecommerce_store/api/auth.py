import frappe
from frappe import _
from frappe.utils.password import update_password

@frappe.whitelist(allow_guest=True)
def register_customer(customer_name, email, password, phone=None):
    """
    Registers a new store customer account.
    Creates Frappe User + Store Customer record.
    """
    try:
        if not email or not password or not customer_name:
            return {"status": "error", "message": _("Name, email and password are required")}

        if frappe.db.exists("User", email):
            return {"status": "error", "message": _("An account with this email already exists")}

        user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": customer_name,
            "enabled": 1,
            "user_type": "Website User",
            "send_welcome_email": 0
        })
        user.insert(ignore_permissions=True)
        update_password(email, password)

        # Create or update Store Customer
        customer = None
        if frappe.db.exists("Store Customer", {"email": email}):
            customer = frappe.get_doc("Store Customer", {"email": email})
            customer.user = user.name
            customer.customer_name = customer_name
            customer.phone = phone or customer.phone
            customer.save(ignore_permissions=True)
        else:
            customer = frappe.get_doc({
                "doctype": "Store Customer",
                "customer_name": customer_name,
                "email": email,
                "phone": phone or "",
                "user": user.name
            })
            customer.insert(ignore_permissions=True)

        frappe.db.commit()

        return {
            "status": "success",
            "message": _("Registration successful"),
            "data": {
                "customer_id": customer.name,
                "customer_name": customer.customer_name,
                "email": customer.email,
                "phone": customer.phone
            }
        }
    except Exception as e:
        frappe.log_error("register_customer error", str(e))
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def login_customer(usr, pwd):
    """
    Authenticates customer with email & password.
    Returns customer details upon success.
    """
    try:
        login_manager = frappe.auth.LoginManager()
        login_manager.authenticate(user=usr, pwd=pwd)
        login_manager.post_login()

        customer = frappe.db.get_value(
            "Store Customer",
            {"email": usr},
            ["name", "customer_name", "email", "phone", "total_orders_placed", "total_spent"],
            as_dict=True
        ) or {
            "name": None,
            "customer_name": frappe.db.get_value("User", usr, "full_name"),
            "email": usr,
            "phone": ""
        }

        return {
            "status": "success",
            "message": _("Login successful"),
            "data": customer,
            "session_id": frappe.session.sid
        }
    except frappe.AuthenticationError:
        return {"status": "error", "message": _("Incorrect email or password")}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def get_customer_profile(email=None):
    """
    Fetches customer profile and saved addresses.
    Requires authentication to prevent IDOR / unauthorized data exposure.
    """
    try:
        if frappe.session.user == "Guest":
            return {"status": "error", "message": _("Authentication required. Please log in.")}

        # If email not specified, default to currently logged-in user
        email = (email or frappe.session.user).strip().lower()

        # Non-admins can only view their own profile
        is_admin = frappe.session.user == "Administrator" or "System Manager" in frappe.get_roles()
        if not is_admin and frappe.session.user.lower() != email:
            return {"status": "error", "message": _("Not authorized to view this customer profile")}

        cust = frappe.db.get_value(
            "Store Customer",
            {"email": email},
            ["name", "customer_name", "email", "phone", "total_orders_placed", "total_spent"],
            as_dict=True
        )
        if not cust:
            return {"status": "error", "message": _("Customer not found")}

        addresses = frappe.get_all(
            "Store Customer Address",
            filters={"customer": cust["name"]},
            fields=["name", "address_title", "address_line1", "address_line2", "city", "state", "postal_code", "country", "phone", "is_default"]
        )

        cust["addresses"] = addresses
        return {"status": "success", "data": cust}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def save_customer_address(
    customer_email=None,
    address_line1=None,
    city=None,
    address_title="Home",
    address_line2=None,
    state=None,
    postal_code=None,
    country="Pakistan",
    phone=None,
    is_default=0,
    **kwargs
):
    """
    Adds or updates a saved address for a customer.
    Requires authentication to prevent unauthorized profile tampering.
    """
    try:
        if frappe.session.user == "Guest":
            return {"status": "error", "message": _("Authentication required. Please log in.")}

        customer_email = (customer_email or frappe.session.user).strip().lower()
        if not address_line1 or not city:
            return {"status": "error", "message": _("Address line 1 and city are required")}

        is_admin = frappe.session.user == "Administrator" or "System Manager" in frappe.get_roles()
        if not is_admin and frappe.session.user.lower() != customer_email:
            return {"status": "error", "message": _("Not authorized to update this customer address")}

        customer_id = frappe.db.get_value("Store Customer", {"email": customer_email}, "name")
        if not customer_id:
            return {"status": "error", "message": _("Customer not found")}

        addr = frappe.get_doc({
            "doctype": "Store Customer Address",
            "customer": customer_id,
            "address_title": address_title or "Home",
            "address_line1": address_line1,
            "address_line2": address_line2 or "",
            "city": city,
            "state": state or "",
            "postal_code": postal_code or "",
            "country": country or "Pakistan",
            "phone": phone or "",
            "is_default": int(is_default or 0)
        })
        addr.insert(ignore_permissions=True)
        frappe.db.commit()

        return {"status": "success", "message": _("Address saved successfully"), "address_id": addr.name}
    except Exception as e:
        return {"status": "error", "message": str(e)}

