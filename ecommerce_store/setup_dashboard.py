import frappe
import json

def setup_dashboard():
    print("Setting up Ecommerce Dashboard, Number Cards, and Charts...")

    # 1. Number Cards
    cards = [
        {
            "name": "Ecom Total Revenue",
            "label": "Total Revenue",
            "type": "Document Type",
            "document_type": "Store Order",
            "function": "Sum",
            "aggregate_function_based_on": "grand_total",
            "filters_json": json.dumps([["Store Order", "order_status", "!=", "Cancelled"]]),
            "color": "#10B981",
            "is_public": 1,
            "is_standard": 1,
            "module": "Ecommerce Store"
        },
        {
            "name": "Ecom Total Orders",
            "label": "Total Orders",
            "type": "Document Type",
            "document_type": "Store Order",
            "function": "Count",
            "filters_json": "[]",
            "color": "#3B82F6",
            "is_public": 1,
            "is_standard": 1,
            "module": "Ecommerce Store"
        },
        {
            "name": "Ecom Pending Orders",
            "label": "Pending Orders",
            "type": "Document Type",
            "document_type": "Store Order",
            "function": "Count",
            "filters_json": json.dumps([["Store Order", "order_status", "=", "Pending"]]),
            "color": "#F59E0B",
            "is_public": 1,
            "is_standard": 1,
            "module": "Ecommerce Store"
        },
        {
            "name": "Ecom Active Products",
            "label": "Active Products",
            "type": "Document Type",
            "document_type": "Product",
            "function": "Count",
            "filters_json": json.dumps([["Product", "is_active", "=", 1]]),
            "color": "#8B5CF6",
            "is_public": 1,
            "is_standard": 1,
            "module": "Ecommerce Store"
        },
        {
            "name": "Ecom Total Customers",
            "label": "Total Customers",
            "type": "Document Type",
            "document_type": "Store Customer",
            "function": "Count",
            "filters_json": "[]",
            "color": "#EC4899",
            "is_public": 1,
            "is_standard": 1,
            "module": "Ecommerce Store"
        }
    ]

    for c in cards:
        card_name = c["name"]
        if frappe.db.exists("Number Card", card_name):
            doc = frappe.get_doc("Number Card", card_name)
            doc.update(c)
            doc.save(ignore_permissions=True)
            print(f"Updated Number Card: {card_name}")
        else:
            doc = frappe.get_doc(dict(doctype="Number Card", **c))
            doc.insert(ignore_permissions=True)
            print(f"Created Number Card: {card_name}")

    # 2. Dashboard Charts
    charts = [
        {
            "chart_name": "Orders by Status",
            "chart_type": "Group By",
            "document_type": "Store Order",
            "group_by_based_on": "order_status",
            "group_by_type": "Count",
            "type": "Donut",
            "filters_json": "[]",
            "is_public": 1,
            "is_standard": 1,
            "module": "Ecommerce Store"
        },
        {
            "chart_name": "Daily Sales Trend",
            "chart_type": "Sum",
            "document_type": "Store Order",
            "based_on": "creation",
            "value_based_on": "grand_total",
            "timeseries": 1,
            "time_interval": "Daily",
            "timespan": "Last Month",
            "type": "Bar",
            "filters_json": "[]",
            "is_public": 1,
            "is_standard": 1,
            "module": "Ecommerce Store"
        }
    ]

    for ch in charts:
        name = ch["chart_name"]
        if frappe.db.exists("Dashboard Chart", name):
            doc = frappe.get_doc("Dashboard Chart", name)
            doc.update(ch)
            doc.save(ignore_permissions=True)
            print(f"Updated Dashboard Chart: {name}")
        else:
            doc = frappe.get_doc(dict(doctype="Dashboard Chart", **ch))
            doc.insert(ignore_permissions=True)
            print(f"Created Dashboard Chart: {name}")

    # 3. Update Workspace with Rich Layout
    ws_content = [
        # KPI Header & Number Cards
        {"type": "header", "data": {"text": "<span class='h4 font-weight-bold'>📊 Store Performance KPIs</span>", "col": 12}},
        {"type": "number_card", "data": {"card_name": "Total Revenue", "col": 3}},
        {"type": "number_card", "data": {"card_name": "Total Orders", "col": 3}},
        {"type": "number_card", "data": {"card_name": "Pending Orders", "col": 2}},
        {"type": "number_card", "data": {"card_name": "Active Products", "col": 2}},
        {"type": "number_card", "data": {"card_name": "Total Customers", "col": 2}},

        {"type": "spacer", "data": {"col": 12}},

        # Charts Section
        {"type": "header", "data": {"text": "<span class='h4 font-weight-bold'>📈 Sales & Orders Analytics</span>", "col": 12}},
        {"type": "chart", "data": {"chart_name": "Daily Sales Trend", "col": 7}},
        {"type": "chart", "data": {"chart_name": "Orders by Status", "col": 5}},

        {"type": "spacer", "data": {"col": 12}},

        # Quick Actions Header
        {"type": "header", "data": {"text": "<span class='h4 font-weight-bold'>⚡ Quick Store Actions</span>", "col": 12}},
        {"type": "shortcut", "data": {"shortcut_name": "Pending Orders", "col": 3}},
        {"type": "shortcut", "data": {"shortcut_name": "All Orders", "col": 3}},
        {"type": "shortcut", "data": {"shortcut_name": "Products", "col": 3}},
        {"type": "shortcut", "data": {"shortcut_name": "Low Stock Alerts", "col": 3}},
        {"type": "shortcut", "data": {"shortcut_name": "Customers", "col": 3}},
        {"type": "shortcut", "data": {"shortcut_name": "Discounts & Coupons", "col": 3}},
        {"type": "shortcut", "data": {"shortcut_name": "Store Settings", "col": 3}},

        {"type": "spacer", "data": {"col": 12}},

        # Management Cards
        {"type": "header", "data": {"text": "<span class='h4 font-weight-bold'>📂 Store Management Modules</span>", "col": 12}},
        {"type": "card", "data": {"card_name": "Catalog Management", "col": 3}},
        {"type": "card", "data": {"card_name": "Sales & Orders", "col": 3}},
        {"type": "card", "data": {"card_name": "Customer Hub", "col": 3}},
        {"type": "card", "data": {"card_name": "Promotions & Settings", "col": 3}}
    ]

    ws_shortcuts = [
        {
            "label": "Pending Orders",
            "link_to": "Store Order",
            "type": "DocType",
            "color": "Orange",
            "format": "{} Pending",
            "stats_filter": json.dumps({"order_status": "Pending"})
        },
        {
            "label": "All Orders",
            "link_to": "Store Order",
            "type": "DocType",
            "color": "Blue",
            "format": "{} Orders",
            "stats_filter": "{}"
        },
        {
            "label": "Products",
            "link_to": "Product",
            "type": "DocType",
            "color": "Green",
            "format": "{} In Catalog",
            "stats_filter": "{}"
        },
        {
            "label": "Low Stock Alerts",
            "link_to": "Product",
            "type": "DocType",
            "color": "Red",
            "format": "{} Low Stock",
            "stats_filter": json.dumps({"track_inventory": 1, "stock_quantity": ["<=", 5]})
        },
        {
            "label": "Customers",
            "link_to": "Store Customer",
            "type": "DocType",
            "color": "Purple",
            "format": "{} Customers",
            "stats_filter": "{}"
        },
        {
            "label": "Discounts & Coupons",
            "link_to": "Store Coupon",
            "type": "DocType",
            "color": "Yellow",
            "format": "{} Coupons",
            "stats_filter": "{}"
        },
        {
            "label": "Store Settings",
            "link_to": "Store Settings",
            "type": "DocType",
            "color": "Grey"
        }
    ]

    ws_links = [
        # Card 1: Catalog Management
        {"type": "Card Break", "label": "Catalog Management", "icon": "box"},
        {"type": "Link", "link_type": "DocType", "link_to": "Product", "label": "All Products"},
        {"type": "Link", "link_type": "DocType", "link_to": "Product Category", "label": "Categories"},
        {"type": "Link", "link_type": "DocType", "link_to": "Product Brand", "label": "Brands"},

        # Card 2: Sales & Orders
        {"type": "Card Break", "label": "Sales & Orders", "icon": "shopping-cart"},
        {"type": "Link", "link_type": "DocType", "link_to": "Store Order", "label": "Customer Orders"},
        {"type": "Link", "link_type": "DocType", "link_to": "Store Cart", "label": "Active Carts"},

        # Card 3: Customer Hub
        {"type": "Card Break", "label": "Customer Hub", "icon": "users"},
        {"type": "Link", "link_type": "DocType", "link_to": "Store Customer", "label": "All Customers"},
        {"type": "Link", "link_type": "DocType", "link_to": "Store Customer Address", "label": "Delivery Addresses"},

        # Card 4: Promotions & Settings
        {"type": "Card Break", "label": "Promotions & Settings", "icon": "settings"},
        {"type": "Link", "link_type": "DocType", "link_to": "Store Coupon", "label": "Coupons & Discounts"},
        {"type": "Link", "link_type": "DocType", "link_to": "Store Settings", "label": "Store Settings"}
    ]

    ws_doc = frappe.get_doc("Workspace", "Ecommerce Store")
    ws_doc.content = json.dumps(ws_content)
    ws_doc.set("shortcuts", ws_shortcuts)
    ws_doc.set("links", ws_links)
    ws_doc.set("number_cards", [
        {"number_card_name": "Total Revenue"},
        {"number_card_name": "Total Orders"},
        {"number_card_name": "Pending Orders"},
        {"number_card_name": "Active Products"},
        {"number_card_name": "Total Customers"}
    ])
    ws_doc.set("charts", [
        {"chart_name": "Orders by Status"},
        {"chart_name": "Daily Sales Trend"}
    ])
    ws_doc.sequence_id = 1.0  # Show at the very top of the desk sidebar!
    ws_doc.save(ignore_permissions=True)
    print("Workspace updated with rich dashboard layout!")

    frappe.db.commit()
    print("Dashboard setup committed successfully!")

if __name__ == "__main__":
    setup_dashboard()
