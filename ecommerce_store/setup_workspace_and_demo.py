import frappe
import json

def setup_all():
    print("Setting up Store Settings, Workspace, and Demo Data...")

    # 1. Store Settings
    settings = frappe.get_single("Store Settings")
    settings.store_name = "ProStore Ecommerce"
    settings.store_email = "store@example.com"
    settings.store_phone = "+92 300 1234567"
    settings.currency = "PKR"
    settings.currency_symbol = "Rs."
    settings.order_prefix = "ORD-"
    settings.default_shipping_fee = 200
    settings.free_shipping_threshold = 3000
    settings.tax_percentage = 0
    settings.allow_guest_checkout = 1
    settings.allow_cod = 1
    settings.allow_online_payment = 1
    settings.save(ignore_permissions=True)
    print("Store Settings configured.")

    # 2. Workspace
    workspace_name = "Ecommerce Store"
    if not frappe.db.exists("Workspace", workspace_name):
        ws = frappe.get_doc({
            "doctype": "Workspace",
            "name": workspace_name,
            "label": "Ecommerce Store",
            "title": "Ecommerce Store",
            "module": "Ecommerce Store",
            "icon": "shopping-bag",
            "is_standard": 1,
            "public": 1,
            "shortcuts": [
                {"type": "DocType", "link_to": "Store Order", "label": "Orders", "icon": "shopping-cart"},
                {"type": "DocType", "link_to": "Product", "label": "Products", "icon": "box"},
                {"type": "DocType", "link_to": "Product Category", "label": "Categories", "icon": "tag"},
                {"type": "DocType", "link_to": "Store Customer", "label": "Customers", "icon": "users"},
                {"type": "DocType", "link_to": "Store Coupon", "label": "Coupons", "icon": "percent"},
                {"type": "DocType", "link_to": "Store Settings", "label": "Store Settings", "icon": "settings"}
            ],
            "links": [
                {
                    "label": "Catalog Management",
                    "type": "Card Break",
                    "icon": "box"
                },
                {"type": "Link", "link_type": "DocType", "link_to": "Product", "label": "All Products"},
                {"type": "Link", "link_type": "DocType", "link_to": "Product Category", "label": "Categories"},
                {"type": "Link", "link_type": "DocType", "link_to": "Product Brand", "label": "Brands"},
                {
                    "label": "Sales & Customers",
                    "type": "Card Break",
                    "icon": "shopping-cart"
                },
                {"type": "Link", "link_type": "DocType", "link_to": "Store Order", "label": "Orders"},
                {"type": "Link", "link_type": "DocType", "link_to": "Store Customer", "label": "Customers"},
                {"type": "Link", "link_type": "DocType", "link_to": "Store Cart", "label": "Active Carts"},
                {
                    "label": "Promotions & Setup",
                    "type": "Card Break",
                    "icon": "settings"
                },
                {"type": "Link", "link_type": "DocType", "link_to": "Store Coupon", "label": "Discounts & Coupons"},
                {"type": "Link", "link_type": "DocType", "link_to": "Store Settings", "label": "Store Configuration"}
            ]
        })
        ws.insert(ignore_permissions=True)
        print("Workspace created.")
    else:
        print("Workspace already exists.")

    # 3. Demo Categories
    categories = [
        {"name": "Electronics", "slug": "electronics", "desc": "Smartphones, Audio, and Gadgets"},
        {"name": "Fashion & Apparel", "slug": "fashion-apparel", "desc": "Clothing, Shoes, and Accessories"},
        {"name": "Home & Living", "slug": "home-living", "desc": "Modern Home Decor and Essentials"}
    ]
    for c in categories:
        if not frappe.db.exists("Product Category", c["slug"]):
            doc = frappe.get_doc({
                "doctype": "Product Category",
                "category_name": c["name"],
                "route_slug": c["slug"],
                "description": c["desc"],
                "is_active": 1
            })
            doc.insert(ignore_permissions=True)
    print("Categories checked/created.")

    # 4. Demo Brands
    brands = [
        {"name": "Nova Tech", "slug": "nova-tech", "desc": "Next-gen smart gadgets"},
        {"name": "Urban Style", "slug": "urban-style", "desc": "Contemporary lifestyle fashion"}
    ]
    for b in brands:
        if not frappe.db.exists("Product Brand", b["slug"]):
            doc = frappe.get_doc({
                "doctype": "Product Brand",
                "brand_name": b["name"],
                "route_slug": b["slug"],
                "description": b["desc"],
                "is_active": 1
            })
            doc.insert(ignore_permissions=True)
    print("Brands checked/created.")

    # 5. Demo Products
    products = [
        {
            "title": "Wireless Noise-Canceling Headphones",
            "slug": "wireless-noise-canceling-headphones",
            "sku": "TECH-WH-001",
            "category": "electronics",
            "brand": "nova-tech",
            "price": 6499.00,
            "compare_at_price": 7999.00,
            "stock_quantity": 25,
            "is_featured": 1,
            "short_description": "High fidelity sound with 30-hour battery life and active noise cancellation.",
            "description": "<p>Experience crystal clear sound with deep bass and premium active noise cancellation. Features Bluetooth 5.3, ultra-comfortable ear cushions, and fast USB-C charging.</p>"
        },
        {
            "title": "Smart Fitness Watch Ultra",
            "slug": "smart-fitness-watch-ultra",
            "sku": "TECH-SW-002",
            "category": "electronics",
            "brand": "nova-tech",
            "price": 4999.00,
            "compare_at_price": 5999.00,
            "stock_quantity": 40,
            "is_featured": 1,
            "short_description": "AMOLED touch display, heart rate sensor, and waterproof design.",
            "description": "<p>Track your workouts, sleep, and heart rate with high precision. Long battery life of up to 10 days on a single charge.</p>"
        },
        {
            "title": "Premium Cotton Graphic T-Shirt",
            "slug": "premium-cotton-graphic-tshirt",
            "sku": "FASH-TS-003",
            "category": "fashion-apparel",
            "brand": "urban-style",
            "price": 1899.00,
            "compare_at_price": 2299.00,
            "stock_quantity": 100,
            "is_featured": 1,
            "short_description": "100% breathable organic cotton with durable modern graphic print.",
            "description": "<p>Crafted for everyday comfort. Super soft combed cotton, pre-shrunk fabric, and ribbed collar.</p>"
        }
    ]

    for p in products:
        if not frappe.db.exists("Product", {"sku": p["sku"]}):
            doc = frappe.get_doc({
                "doctype": "Product",
                "title": p["title"],
                "route_slug": p["slug"],
                "sku": p["sku"],
                "category": p["category"],
                "brand": p["brand"],
                "price": p["price"],
                "compare_at_price": p["compare_at_price"],
                "is_active": 1,
                "is_featured": p["is_featured"],
                "is_in_stock": 1,
                "track_inventory": 1,
                "stock_quantity": p["stock_quantity"],
                "short_description": p["short_description"],
                "description": p["description"]
            })
            doc.insert(ignore_permissions=True)
    print("Products checked/created.")

    # 6. Demo Coupon
    coupon_code = "WELCOME10"
    if not frappe.db.exists("Store Coupon", coupon_code):
        doc = frappe.get_doc({
            "doctype": "Store Coupon",
            "coupon_code": coupon_code,
            "discount_type": "Percentage",
            "discount_value": 10,
            "min_order_amount": 1000,
            "max_discount_amount": 1500,
            "is_active": 1,
            "description": "10% off on your first order over Rs. 1000"
        })
        doc.insert(ignore_permissions=True)
        print("Coupon WELCOME10 created.")

    frappe.db.commit()
    print("Setup completed successfully!")

