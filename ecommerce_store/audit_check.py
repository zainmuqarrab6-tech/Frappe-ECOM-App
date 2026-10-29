import frappe

def run_health_audit():
    print("=== SYSTEM HEALTH & AUDIT CHECK ===")

    # 1. Error Logs in Frappe
    errors = frappe.get_all("Error Log", fields=["name", "method", "error", "creation"], order_by="creation desc", limit=10)
    print(f"Total Error Logs found: {len(errors)}")
    for e in errors:
        print(f" - [{e.creation}] {e.method}: {e.error[:120]}...")

    # 2. Check DocTypes
    doctypes_to_check = [
        ("Product", False),
        ("Product Category", False),
        ("Product Brand", False),
        ("Store Order", False),
        ("Store Cart", False),
        ("Store Customer", False),
        ("Store Coupon", False),
        ("Store Settings", True)
    ]
    print("\n--- DocTypes Check ---")
    for dt, is_single in doctypes_to_check:
        exists = frappe.db.exists("DocType", dt)
        if is_single:
            doc = frappe.get_single(dt) if exists else None
            print(f" - {dt} (Single): {'OK' if exists and doc else 'MISSING'}")
        else:
            count = frappe.db.count(dt) if exists else 0
            print(f" - {dt}: {'OK' if exists else 'MISSING'} (Records: {count})")

    # 3. Check Workspace
    print("\n--- Workspace Check ---")
    ws_exists = frappe.db.exists("Workspace", "Ecommerce Store")
    print(f" - Workspace 'Ecommerce Store': {'OK' if ws_exists else 'MISSING'}")

    # 4. Check Number Cards & Charts
    print("\n--- Number Cards & Charts Check ---")
    cards = ["Total Revenue", "Total Orders", "Pending Orders", "Active Products", "Total Customers"]
    for c in cards:
        print(f" - Number Card '{c}': {'OK' if frappe.db.exists('Number Card', c) else 'MISSING'}")

    charts = ["Orders by Status", "Daily Sales Trend"]
    for ch in charts:
        print(f" - Dashboard Chart '{ch}': {'OK' if frappe.db.exists('Dashboard Chart', ch) else 'MISSING'}")

    # 5. Check Test Order
    print("\n--- Orders Integrity Check ---")
    orders = frappe.get_all("Store Order", fields=["name", "customer_name", "grand_total", "order_status", "payment_status"])
    for o in orders:
        order_doc = frappe.get_doc("Store Order", o.name)
        items_count = len(order_doc.items)
        print(f" - Order {o.name}: Status={o.order_status}, Payment={o.payment_status}, Total={o.grand_total}, ItemsCount={items_count}")

    print("\nAudit Complete.")
