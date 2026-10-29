import frappe
import json

def setup_dashboard():
    print("Updating Workspace with Store Customizer, Themes, Banners, CMS & Reviews...")

    # Workspace Content Layout
    ws_content = [
        # Store KPIs
        {"type": "header", "data": {"text": "<span class='h4 font-weight-bold'>📊 Store Performance KPIs</span>", "col": 12}},
        {"type": "number_card", "data": {"card_name": "Total Revenue", "col": 3}},
        {"type": "number_card", "data": {"card_name": "Total Orders", "col": 3}},
        {"type": "number_card", "data": {"card_name": "Pending Orders", "col": 2}},
        {"type": "number_card", "data": {"card_name": "Active Products", "col": 2}},
        {"type": "number_card", "data": {"card_name": "Total Customers", "col": 2}},

        {"type": "spacer", "data": {"col": 12}},

        # Shopify-Like Store Customizer Row
        {"type": "header", "data": {"text": "<span class='h4 font-weight-bold'>🎨 Storefront Design & Customizer (Shopify-Style)</span>", "col": 12}},
        {"type": "shortcut", "data": {"shortcut_name": "Store Customizer", "col": 3}},
        {"type": "shortcut", "data": {"shortcut_name": "Hero Banners", "col": 3}},
        {"type": "shortcut", "data": {"shortcut_name": "Navigation Menus", "col": 3}},
        {"type": "shortcut", "data": {"shortcut_name": "Pages & Policies", "col": 3}},

        {"type": "spacer", "data": {"col": 12}},

        # Sales & Orders Analytics
        {"type": "header", "data": {"text": "<span class='h4 font-weight-bold'>📈 Sales & Orders Analytics</span>", "col": 12}},
        {"type": "chart", "data": {"chart_name": "Daily Sales Trend", "col": 7}},
        {"type": "chart", "data": {"chart_name": "Orders by Status", "col": 5}},

        {"type": "spacer", "data": {"col": 12}},

        # Quick Actions
        {"type": "header", "data": {"text": "<span class='h4 font-weight-bold'>⚡ Commerce Operations</span>", "col": 12}},
        {"type": "shortcut", "data": {"shortcut_name": "Pending Orders", "col": 3}},
        {"type": "shortcut", "data": {"shortcut_name": "All Orders", "col": 3}},
        {"type": "shortcut", "data": {"shortcut_name": "Products", "col": 3}},
        {"type": "shortcut", "data": {"shortcut_name": "Low Stock Alerts", "col": 3}},
        {"type": "shortcut", "data": {"shortcut_name": "Customers", "col": 3}},
        {"type": "shortcut", "data": {"shortcut_name": "Product Reviews", "col": 3}},
        {"type": "shortcut", "data": {"shortcut_name": "Discounts & Coupons", "col": 3}},
        {"type": "shortcut", "data": {"shortcut_name": "Store Settings", "col": 3}},

        {"type": "spacer", "data": {"col": 12}},

        # Modules
        {"type": "header", "data": {"text": "<span class='h4 font-weight-bold'>📂 Store Management Modules</span>", "col": 12}},
        {"type": "card", "data": {"card_name": "Storefront Customizer", "col": 3}},
        {"type": "card", "data": {"card_name": "Catalog Management", "col": 3}},
        {"type": "card", "data": {"card_name": "Sales & Orders", "col": 3}},
        {"type": "card", "data": {"card_name": "Customer & Marketing", "col": 3}}
    ]

    ws_shortcuts = [
        # Store Customizer Shortcuts
        {
            "label": "Store Customizer",
            "link_to": "Store Theme Settings",
            "type": "DocType",
            "color": "Purple"
        },
        {
            "label": "Hero Banners",
            "link_to": "Store Banner",
            "type": "DocType",
            "color": "Blue",
            "format": "{} Active Banners",
            "stats_filter": json.dumps({"is_active": 1})
        },
        {
            "label": "Navigation Menus",
            "link_to": "Store Navigation Menu",
            "type": "DocType",
            "color": "Green"
        },
        {
            "label": "Pages & Policies",
            "link_to": "Store Page",
            "type": "DocType",
            "color": "Grey",
            "format": "{} Pages",
            "stats_filter": "{}"
        },
        # Commerce Operations
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
            "format": "{} Products",
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
            "label": "Product Reviews",
            "link_to": "Product Review",
            "type": "DocType",
            "color": "Yellow",
            "format": "{} Reviews",
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
        # Card 1: Storefront Customizer
        {"type": "Card Break", "label": "Storefront Customizer", "icon": "tool"},
        {"type": "Link", "link_type": "DocType", "link_to": "Store Theme Settings", "label": "Theme & Brand Colors"},
        {"type": "Link", "link_type": "DocType", "link_to": "Store Banner", "label": "Hero Sliders & Banners"},
        {"type": "Link", "link_type": "DocType", "link_to": "Store Navigation Menu", "label": "Header & Footer Menus"},
        {"type": "Link", "link_type": "DocType", "link_to": "Store Page", "label": "Custom Pages & Policies"},

        # Card 2: Catalog Management
        {"type": "Card Break", "label": "Catalog Management", "icon": "box"},
        {"type": "Link", "link_type": "DocType", "link_to": "Product", "label": "All Products"},
        {"type": "Link", "link_type": "DocType", "link_to": "Product Category", "label": "Categories"},
        {"type": "Link", "link_type": "DocType", "link_to": "Product Brand", "label": "Brands"},
        {"type": "Link", "link_type": "DocType", "link_to": "Product Review", "label": "Customer Reviews & Ratings"},

        # Card 3: Sales & Orders
        {"type": "Card Break", "label": "Sales & Orders", "icon": "shopping-cart"},
        {"type": "Link", "link_type": "DocType", "link_to": "Store Order", "label": "Customer Orders"},
        {"type": "Link", "link_type": "DocType", "link_to": "Store Cart", "label": "Active Shopping Carts"},

        # Card 4: Customer & Marketing
        {"type": "Card Break", "label": "Customer & Marketing", "icon": "users"},
        {"type": "Link", "link_type": "DocType", "link_to": "Store Customer", "label": "Customers Directory"},
        {"type": "Link", "link_type": "DocType", "link_to": "Store Coupon", "label": "Promotions & Coupons"},
        {"type": "Link", "link_type": "DocType", "link_to": "Store Settings", "label": "Shipping & Taxes Config"}
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
    ws_doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("Workspace updated with Store Customizer successfully!")

if __name__ == "__main__":
    setup_dashboard()
