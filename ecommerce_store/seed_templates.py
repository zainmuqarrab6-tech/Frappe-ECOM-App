import frappe

def seed_store_themes():
    print("Seeding ready-to-use customizable Store Themes...")

    templates = [
        {
            "theme_name": "Modern Flagship",
            "version": "1.0.0",
            "category": "General & Multipurpose",
            "is_active": 1,
            "badge_text": "Default",
            "description": "High-converting, clean, and modern layout suitable for any retail store. Features quick cart drawer, sticky header, and trust badges.",
            "primary_color": "#0284c7",
            "secondary_color": "#0f172a",
            "accent_color": "#f59e0b",
            "bg_color": "#ffffff",
            "text_color": "#1e293b",
            "font_heading": "Plus Jakarta Sans",
            "font_body": "Inter",
            "header_style": "Minimal Top Bar",
            "hero_banner_style": "Full Width Hero Slider",
            "product_card_style": "Card with Shadow",
            "cart_type": "Slide-out Drawer Cart",
            "footer_style": "Multi-column Mega Footer",
            "custom_css": "/* Modern Flagship Custom Styling */\n.hero-cta { box-shadow: 0 10px 25px -5px rgba(2, 132, 199, 0.4); }\n.product-card:hover { transform: translateY(-4px); transition: transform 0.2s ease; }"
        },
        {
            "theme_name": "Tech & Cyber Pro",
            "version": "1.0.0",
            "category": "Electronics & Tech",
            "is_active": 0,
            "badge_text": "Dark Mode",
            "description": "Futuristic dark mode theme tailored for electronics, smartphones, gaming accessories, and smart wearables.",
            "primary_color": "#3b82f6",
            "secondary_color": "#1e293b",
            "accent_color": "#06b6d4",
            "bg_color": "#0b0f19",
            "text_color": "#f1f5f9",
            "font_heading": "Montserrat",
            "font_body": "Inter",
            "header_style": "Centered Logo",
            "hero_banner_style": "Split Image & Text",
            "product_card_style": "Rounded Modern",
            "cart_type": "Slide-out Drawer Cart",
            "footer_style": "Multi-column Mega Footer",
            "custom_css": "/* Tech & Cyber Pro Styling */\nbody { background-color: #0b0f19; color: #f1f5f9; }\n.card-glass { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.08); }"
        },
        {
            "theme_name": "Velvet Elegance Boutique",
            "version": "1.0.0",
            "category": "Fashion & Apparel",
            "is_active": 0,
            "badge_text": "Luxury",
            "description": "Editorial, elegant boutique aesthetic designed for clothing lines, contemporary streetwear, shoes, and luxury jewelry.",
            "primary_color": "#18181b",
            "secondary_color": "#27272a",
            "accent_color": "#e11d48",
            "bg_color": "#fafaf9",
            "text_color": "#292524",
            "font_heading": "Playfair Display",
            "font_body": "Poppins",
            "header_style": "Minimal Top Bar",
            "hero_banner_style": "Minimal Grid",
            "product_card_style": "Standard Borderless",
            "cart_type": "Slide-out Drawer Cart",
            "footer_style": "Simple Centered",
            "custom_css": "/* Velvet Boutique Styling */\n.hero-heading { font-family: 'Playfair Display', serif; letter-spacing: -0.5px; }\n.btn-luxury { text-transform: uppercase; letter-spacing: 1.5px; font-size: 12px; }"
        },
        {
            "theme_name": "Fresh Bloom Organic",
            "version": "1.0.0",
            "category": "Grocery & Food",
            "is_active": 0,
            "badge_text": "Eco-Friendly",
            "description": "Vibrant, earthy natural design crafted for organic foods, health supplements, skincare, and sustainable lifestyle products.",
            "primary_color": "#059669",
            "secondary_color": "#064e3b",
            "accent_color": "#d97706",
            "bg_color": "#f0fdf4",
            "text_color": "#14532d",
            "font_heading": "Plus Jakarta Sans",
            "font_body": "Inter",
            "header_style": "Split Navigation",
            "hero_banner_style": "Split Image & Text",
            "product_card_style": "Card with Shadow",
            "cart_type": "Slide-out Drawer Cart",
            "footer_style": "Multi-column Mega Footer",
            "custom_css": "/* Fresh Bloom Organic */\n.badge-eco { background: #dcfce7; color: #166534; font-weight: 600; border-radius: 9999px; }"
        }
    ]

    for t in templates:
        name = t["theme_name"]
        if not frappe.db.exists("Store Theme", name):
            doc = frappe.get_doc(dict(doctype="Store Theme", **t))
            doc.insert(ignore_permissions=True)
            print(f"Created template: {name}")
        else:
            # Update existing with latest fields
            doc = frappe.get_doc("Store Theme", name)
            for k, v in t.items():
                setattr(doc, k, v)
            doc.save(ignore_permissions=True)
            print(f"Updated template: {name}")

    frappe.db.commit()
    print("Store Theme seeding complete.")

if __name__ == "__main__":
    seed_store_themes()
