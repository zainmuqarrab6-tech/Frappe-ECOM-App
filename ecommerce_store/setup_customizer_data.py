import frappe

def setup_all():
    print("Populating default Theme, Banners, Menus, Pages, and Reviews...")

    # 1. Store Theme Settings
    theme = frappe.get_single("Store Theme Settings")
    theme.store_tagline = "Premium Tech, Fashion & Lifestyle Delivered Fast"
    theme.enable_announcement_bar = 1
    theme.announcement_text = "🎉 Free Nationwide Shipping on orders over Rs. 3,000 | Flat 10% Off with Code: WELCOME10"
    theme.announcement_link = "/shop"
    theme.announcement_bg_color = "#0f172a"
    theme.announcement_text_color = "#ffffff"
    theme.primary_color = "#0284c7"
    theme.secondary_color = "#0f172a"
    theme.accent_color = "#f59e0b"
    theme.font_family = "Inter"
    theme.social_whatsapp = "+923001234567"
    theme.social_facebook = "https://facebook.com"
    theme.social_instagram = "https://instagram.com"
    theme.social_tiktok = "https://tiktok.com"
    theme.footer_about_text = "Your trusted destination for premium electronics, contemporary fashion, and lifestyle essentials with fast cash on delivery across Pakistan."
    theme.copyright_text = "© 2026 ProStore Ecommerce. All Rights Reserved."
    theme.save(ignore_permissions=True)
    print("Store Theme Settings configured.")

    # 2. Store Banners
    banners = [
        {
            "title": "Summer Mega Tech Sale",
            "banner_type": "Hero Slider",
            "heading": "Next-Gen Audio & Smart Wearables",
            "subheading": "Experience crystal clear acoustics with up to 30% off on active noise-canceling headsets.",
            "button_text": "Shop Tech Deals",
            "button_link": "/category/electronics",
            "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=1600&q=80",
            "sort_order": 1,
            "is_active": 1
        },
        {
            "title": "Urban Streetwear Collection",
            "banner_type": "Hero Slider",
            "heading": "New Arrival: Minimalist Summer Essentials",
            "subheading": "100% combed breathable cotton tees engineered for all-day comfort.",
            "button_text": "Explore Fashion",
            "button_link": "/category/fashion-apparel",
            "image": "https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=1600&q=80",
            "sort_order": 2,
            "is_active": 1
        }
    ]
    for b in banners:
        if not frappe.db.exists("Store Banner", {"title": b["title"]}):
            doc = frappe.get_doc(dict(doctype="Store Banner", **b))
            doc.insert(ignore_permissions=True)
            print(f"Created Banner: {b['title']}")

    # 3. Store Navigation Menus
    header_menu_name = "Header Main Menu"
    if not frappe.db.exists("Store Navigation Menu", header_menu_name):
        menu = frappe.get_doc({
            "doctype": "Store Navigation Menu",
            "menu_name": header_menu_name,
            "menu_location": "Header",
            "is_active": 1,
            "items": [
                {"label": "Home", "url": "/", "is_external": 0},
                {"label": "All Products", "url": "/shop", "is_external": 0},
                {"label": "Electronics", "url": "/category/electronics", "badge_text": "HOT", "is_external": 0},
                {"label": "Fashion", "url": "/category/fashion-apparel", "is_external": 0},
                {"label": "About Us", "url": "/page/about-us", "is_external": 0},
                {"label": "Contact", "url": "/page/contact-us", "is_external": 0}
            ]
        })
        menu.insert(ignore_permissions=True)
        print("Created Header Main Menu.")

    footer_menu_name = "Footer Policies Menu"
    if not frappe.db.exists("Store Navigation Menu", footer_menu_name):
        menu = frappe.get_doc({
            "doctype": "Store Navigation Menu",
            "menu_name": footer_menu_name,
            "menu_location": "Footer Policies",
            "is_active": 1,
            "items": [
                {"label": "Shipping & Delivery", "url": "/page/shipping-policy", "is_external": 0},
                {"label": "Refund & Returns", "url": "/page/refund-policy", "is_external": 0},
                {"label": "Privacy Policy", "url": "/page/privacy-policy", "is_external": 0},
                {"label": "Terms of Service", "url": "/page/terms", "is_external": 0}
            ]
        })
        menu.insert(ignore_permissions=True)
        print("Created Footer Policies Menu.")

    # 4. Custom CMS Pages
    pages = [
        {
            "title": "About Our Store",
            "route_slug": "about-us",
            "content": "<h2>Welcome to ProStore</h2><p>Founded with a passion for premium quality and customer delight, ProStore brings you curated tech gadgets, lifestyle fashion, and home essentials with fast nationwide cash-on-delivery.</p><p>We partner with leading global manufacturers to ensure 100% genuine products with warranty backed by fast customer care.</p>",
            "meta_description": "Learn more about ProStore and our commitment to genuine products and fast nationwide delivery."
        },
        {
            "title": "Shipping & Delivery Policy",
            "route_slug": "shipping-policy",
            "content": "<h2>Fast Nationwide Delivery</h2><p>We deliver across Pakistan within 2 to 4 business days. Free shipping automatically applies on all orders totaling Rs. 3,000 or above.</p><p>All parcels are trackable with real-time SMS and courier airway bills via TCS, Leopards, and M&P.</p>",
            "meta_description": "Our nationwide delivery timeline, shipping charges, and tracking details."
        },
        {
            "title": "7-Day Return & Replacement Policy",
            "route_slug": "refund-policy",
            "content": "<h2>100% Customer Satisfaction Guarantee</h2><p>Shop with complete peace of mind. If your parcel arrives damaged, defective, or incorrect, contact our WhatsApp support within 7 days for an instant free replacement or full refund.</p>",
            "meta_description": "Hassle-free 7-day return and refund policy."
        }
    ]
    for p in pages:
        if not frappe.db.exists("Store Page", p["route_slug"]):
            doc = frappe.get_doc(dict(doctype="Store Page", **p))
            doc.insert(ignore_permissions=True)
            print(f"Created CMS Page: {p['title']}")

    # 5. Product Review
    prod_id = frappe.db.get_value("Product", {"sku": "TECH-WH-001"}, "name")
    if prod_id and not frappe.db.exists("Product Review", {"product": prod_id}):
        review = frappe.get_doc({
            "doctype": "Product Review",
            "product": prod_id,
            "customer_name": "Hamza Khan",
            "customer_email": "hamza@example.com",
            "rating": "5",
            "title": "Incredible Sound Quality & Battery!",
            "review_text": "The bass is punchy, and the active noise cancellation completely blocks out background noise. Battery easily lasts 2 days of heavy use. Highly recommended!",
            "is_verified_buyer": 1,
            "status": "Approved"
        })
        review.insert(ignore_permissions=True)
        print("Created sample product review.")

    frappe.db.commit()
    print("Customizer setup completed successfully!")

if __name__ == "__main__":
    setup_all()

