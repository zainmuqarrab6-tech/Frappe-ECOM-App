import frappe

def create_customizer_doctypes():
    print("Starting DocType creation for Store Customizer, Themes, Banners, and CMS...")

    doctypes = [
        # 1. Store Menu Item (Child Table)
        {
            "doctype": "DocType",
            "name": "Store Menu Item",
            "module": "Ecommerce Store",
            "custom": 0,
            "istable": 1,
            "fields": [
                {"fieldname": "label", "fieldtype": "Data", "label": "Label", "reqd": 1, "in_list_view": 1},
                {"fieldname": "url", "fieldtype": "Data", "label": "URL / Path", "reqd": 1, "in_list_view": 1},
                {"fieldname": "badge_text", "fieldtype": "Data", "label": "Badge (e.g. HOT, NEW)", "in_list_view": 1},
                {"fieldname": "is_external", "fieldtype": "Check", "label": "External Link", "default": "0"}
            ],
            "permissions": []
        },

        # 2. Store Navigation Menu
        {
            "doctype": "DocType",
            "name": "Store Navigation Menu",
            "module": "Ecommerce Store",
            "custom": 0,
            "autoname": "field:menu_name",
            "fields": [
                {"fieldname": "menu_name", "fieldtype": "Data", "label": "Menu Name", "reqd": 1, "unique": 1, "in_list_view": 1},
                {"fieldname": "menu_location", "fieldtype": "Select", "label": "Display Location", "options": "Header\nFooter Column 1\nFooter Column 2\nFooter Policies", "default": "Header", "reqd": 1, "in_list_view": 1},
                {"fieldname": "is_active", "fieldtype": "Check", "label": "Is Active", "default": "1", "in_list_view": 1},
                {"fieldname": "sec_items", "fieldtype": "Section Break", "label": "Menu Links"},
                {"fieldname": "items", "fieldtype": "Table", "label": "Links", "options": "Store Menu Item"}
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "Guest", "read": 1}
            ]
        },

        # 3. Store Banner
        {
            "doctype": "DocType",
            "name": "Store Banner",
            "module": "Ecommerce Store",
            "custom": 0,
            "autoname": "format:BANNER-{#####}",
            "fields": [
                {"fieldname": "title", "fieldtype": "Data", "label": "Banner Title (Internal)", "reqd": 1, "in_list_view": 1},
                {"fieldname": "banner_type", "fieldtype": "Select", "label": "Banner Type", "options": "Hero Slider\nPromotional Banner\nSide Banner", "default": "Hero Slider", "reqd": 1, "in_list_view": 1},
                {"fieldname": "sort_order", "fieldtype": "Int", "label": "Sort Order", "default": "0", "in_list_view": 1},
                {"fieldname": "is_active", "fieldtype": "Check", "label": "Is Active", "default": "1", "in_list_view": 1},
                
                {"fieldname": "sec_content", "fieldtype": "Section Break", "label": "Banner Content"},
                {"fieldname": "heading", "fieldtype": "Data", "label": "Headline Text", "reqd": 1},
                {"fieldname": "subheading", "fieldtype": "Small Text", "label": "Subheading / Tagline"},
                {"fieldname": "button_text", "fieldtype": "Data", "label": "Button Label", "default": "Shop Now"},
                {"fieldname": "button_link", "fieldtype": "Data", "label": "Button Target Link", "default": "/shop"},
                
                {"fieldname": "sec_media", "fieldtype": "Section Break", "label": "Banner Images"},
                {"fieldname": "image", "fieldtype": "Attach Image", "label": "Desktop Image (1920x600 recommended)", "reqd": 1},
                {"fieldname": "mobile_image", "fieldtype": "Attach Image", "label": "Mobile Image (800x800 recommended)"}
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "Guest", "read": 1}
            ]
        },

        # 4. Store Page (CMS)
        {
            "doctype": "DocType",
            "name": "Store Page",
            "module": "Ecommerce Store",
            "custom": 0,
            "autoname": "field:route_slug",
            "fields": [
                {"fieldname": "title", "fieldtype": "Data", "label": "Page Title", "reqd": 1, "in_list_view": 1},
                {"fieldname": "route_slug", "fieldtype": "Data", "label": "URL Slug", "reqd": 1, "unique": 1, "in_list_view": 1},
                {"fieldname": "is_published", "fieldtype": "Check", "label": "Is Published", "default": "1", "in_list_view": 1},
                {"fieldname": "sec_content", "fieldtype": "Section Break", "label": "Page Content"},
                {"fieldname": "content", "fieldtype": "Text Editor", "label": "Content", "reqd": 1},
                {"fieldname": "sec_seo", "fieldtype": "Section Break", "label": "SEO & Metadata"},
                {"fieldname": "meta_description", "fieldtype": "Small Text", "label": "Meta Description"}
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "Guest", "read": 1}
            ]
        },

        # 5. Product Review
        {
            "doctype": "DocType",
            "name": "Product Review",
            "module": "Ecommerce Store",
            "custom": 0,
            "autoname": "format:REV-{#####}",
            "fields": [
                {"fieldname": "product", "fieldtype": "Link", "label": "Product", "options": "Product", "reqd": 1, "in_list_view": 1},
                {"fieldname": "customer_name", "fieldtype": "Data", "label": "Customer Name", "reqd": 1, "in_list_view": 1},
                {"fieldname": "customer_email", "fieldtype": "Data", "label": "Customer Email", "reqd": 1, "options": "Email"},
                {"fieldname": "rating", "fieldtype": "Select", "label": "Rating (1 to 5)", "options": "5\n4\n3\n2\n1", "default": "5", "reqd": 1, "in_list_view": 1},
                {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Pending\nApproved\nRejected", "default": "Approved", "in_list_view": 1},
                {"fieldname": "sec_review", "fieldtype": "Section Break", "label": "Review Content"},
                {"fieldname": "title", "fieldtype": "Data", "label": "Review Headline"},
                {"fieldname": "review_text", "fieldtype": "Small Text", "label": "Review Comments", "reqd": 1},
                {"fieldname": "is_verified_buyer", "fieldtype": "Check", "label": "Verified Buyer", "default": "1"}
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "Guest", "read": 1, "create": 1}
            ]
        },

        # 6. Store Theme Settings (Single)
        {
            "doctype": "DocType",
            "name": "Store Theme Settings",
            "module": "Ecommerce Store",
            "custom": 0,
            "issingle": 1,
            "fields": [
                {"fieldname": "sec_brand", "fieldtype": "Section Break", "label": "Brand Assets"},
                {"fieldname": "store_logo", "fieldtype": "Attach Image", "label": "Store Logo"},
                {"fieldname": "favicon", "fieldtype": "Attach Image", "label": "Favicon"},
                {"fieldname": "store_tagline", "fieldtype": "Data", "label": "Store Tagline", "default": "The Best Products, Delivered Fast"},

                {"fieldname": "sec_announcement", "fieldtype": "Section Break", "label": "Top Announcement Bar"},
                {"fieldname": "enable_announcement_bar", "fieldtype": "Check", "label": "Enable Announcement Bar", "default": "1"},
                {"fieldname": "announcement_text", "fieldtype": "Data", "label": "Announcement Text", "default": "🎉 Free Shipping on orders over Rs. 3,000 | Use Code: WELCOME10"},
                {"fieldname": "announcement_link", "fieldtype": "Data", "label": "Announcement Click Link", "default": "/shop"},
                {"fieldname": "announcement_bg_color", "fieldtype": "Data", "label": "Announcement Background Color (HEX)", "default": "#0f172a"},
                {"fieldname": "announcement_text_color", "fieldtype": "Data", "label": "Announcement Text Color (HEX)", "default": "#ffffff"},

                {"fieldname": "sec_colors", "fieldtype": "Section Break", "label": "Theme Colors & Styling"},
                {"fieldname": "primary_color", "fieldtype": "Data", "label": "Primary Brand Color (Buttons & Highlights)", "default": "#0284c7"},
                {"fieldname": "secondary_color", "fieldtype": "Data", "label": "Secondary Color (Dark Headers/Footers)", "default": "#0f172a"},
                {"fieldname": "accent_color", "fieldtype": "Data", "label": "Accent Color (Badges/Sale)", "default": "#f59e0b"},
                {"fieldname": "font_family", "fieldtype": "Select", "label": "Primary Font", "options": "Inter\nRoboto\nPoppins\nMontserrat\nOpen Sans", "default": "Inter"},

                {"fieldname": "sec_footer", "fieldtype": "Section Break", "label": "Footer & Social Media Links"},
                {"fieldname": "footer_about_text", "fieldtype": "Small Text", "label": "Footer About Us Text", "default": "Your trusted destination for premium electronics, fashion, and home goods with nationwide cash on delivery."},
                {"fieldname": "social_whatsapp", "fieldtype": "Data", "label": "WhatsApp Support Number", "default": "+923001234567"},
                {"fieldname": "social_facebook", "fieldtype": "Data", "label": "Facebook Page URL"},
                {"fieldname": "social_instagram", "fieldtype": "Data", "label": "Instagram Profile URL"},
                {"fieldname": "social_tiktok", "fieldtype": "Data", "label": "TikTok URL"},
                {"fieldname": "copyright_text", "fieldtype": "Data", "label": "Copyright Notice", "default": "© 2026 ProStore Ecommerce. All Rights Reserved."}
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1}
            ]
        }
    ]

    for dt_data in doctypes:
        name = dt_data["name"]
        if frappe.db.exists("DocType", name):
            print(f"Updating DocType: {name}")
            doc = frappe.get_doc("DocType", name)
            doc.update(dt_data)
            doc.save()
        else:
            print(f"Creating DocType: {name}")
            doc = frappe.get_doc(dt_data)
            doc.insert()

    frappe.db.commit()
    print("Store Customizer DocTypes created and committed successfully!")

if __name__ == "__main__":
    create_customizer_doctypes()

