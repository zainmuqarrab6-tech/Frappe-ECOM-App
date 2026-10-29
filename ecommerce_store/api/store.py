import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def get_store_settings():
    """
    Returns public store settings (currency, store name, shipping policy, etc.)
    for frontend initial setup/context.
    """
    try:
        settings = frappe.get_single("Store Settings")
        return {
            "status": "success",
            "data": {
                "store_name": settings.store_name or "My E-Commerce Store",
                "store_email": settings.store_email or "",
                "store_phone": settings.store_phone or "",
                "currency": settings.currency or "PKR",
                "currency_symbol": settings.currency_symbol or "Rs.",
                "default_shipping_fee": float(settings.default_shipping_fee or 0),
                "free_shipping_threshold": float(settings.free_shipping_threshold or 0),
                "tax_percentage": float(settings.tax_percentage or 0),
                "allow_guest_checkout": bool(settings.allow_guest_checkout),
                "allow_cod": bool(settings.allow_cod),
                "allow_online_payment": bool(settings.allow_online_payment)
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def check_health():
    """
    Simple API health check endpoint.
    """
    return {
        "status": "online",
        "message": "Ecommerce Store API is up and running smoothly!",
        "version": "1.0.0"
    }

