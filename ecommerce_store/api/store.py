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

@frappe.whitelist()
def get_shopify_dashboard_data():
    """
    Returns real-time Shopify-style store metrics, action items, and recent orders.
    """
    try:
        settings = frappe.get_single("Store Settings")
        currency_symbol = settings.currency_symbol or "Rs."
        currency = settings.currency or "PKR"

        # Sales & Orders count (non-cancelled)
        sales_data = frappe.db.sql("""
            SELECT COALESCE(SUM(grand_total), 0) as total_sales, COUNT(name) as total_orders
            FROM `tabStore Order`
            WHERE order_status != 'Cancelled'
        """, as_dict=True)[0]

        total_sales = float(sales_data.total_sales or 0)
        total_orders = int(sales_data.total_orders or 0)

        # Unfulfilled / Pending Orders
        pending_orders = frappe.db.count("Store Order", {"order_status": "Pending"})

        # Active Products
        active_products = frappe.db.count("Product", {"is_active": 1})

        # Low Stock Alerts
        low_stock_products = frappe.db.count("Product", {"track_inventory": 1, "stock_quantity": ["<=", 5]})

        # Total Customers
        total_customers = frappe.db.count("Store Customer")

        # 5 Recent Orders
        recent_orders = frappe.get_all(
            "Store Order",
            fields=["name", "customer_name", "order_date", "order_status", "payment_status", "grand_total"],
            order_by="creation desc",
            limit=5
        )

        return {
            "status": "success",
            "data": {
                "store_name": settings.store_name or "ProStore Ecommerce",
                "currency_symbol": currency_symbol,
                "currency": currency,
                "total_sales": total_sales,
                "total_orders": total_orders,
                "pending_orders": pending_orders,
                "active_products": active_products,
                "low_stock_products": low_stock_products,
                "total_customers": total_customers,
                "recent_orders": recent_orders
            }
        }
    except Exception as e:
        frappe.log_error("get_shopify_dashboard_data error", str(e))
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
