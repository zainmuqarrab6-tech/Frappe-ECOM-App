import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def get_store_design():
    """
    Returns complete store branding, theme colors, announcement bar,
    hero banners, navigation menus, and store policies in ONE single call.
    Just like Shopify theme JSON!
    """
    try:
        # 1. Theme Settings
        theme = frappe.get_single("Store Theme Settings")
        store_settings = frappe.get_single("Store Settings")

        # 2. Hero & Promo Banners
        banners = frappe.get_all(
            "Store Banner",
            filters={"is_active": 1},
            fields=[
                "name", "title", "banner_type", "heading", "subheading",
                "button_text", "button_link", "image", "mobile_image", "sort_order"
            ],
            order_by="sort_order asc, creation desc"
        )
        for b in banners:
            if b.get("image"):
                b["image_url"] = frappe.utils.get_url(b["image"])
            if b.get("mobile_image"):
                b["mobile_image_url"] = frappe.utils.get_url(b["mobile_image"])

        # 3. Menus (Header & Footer)
        header_menu = None
        if frappe.db.exists("Store Navigation Menu", {"menu_location": "Header", "is_active": 1}):
            h_doc = frappe.get_doc("Store Navigation Menu", {"menu_location": "Header", "is_active": 1})
            header_menu = [
                {"label": it.label, "url": it.url, "badge_text": it.badge_text, "is_external": bool(it.is_external)}
                for it in h_doc.items
            ]

        footer_menu = None
        if frappe.db.exists("Store Navigation Menu", {"menu_location": "Footer Policies", "is_active": 1}):
            f_doc = frappe.get_doc("Store Navigation Menu", {"menu_location": "Footer Policies", "is_active": 1})
            footer_menu = [
                {"label": it.label, "url": it.url, "is_external": bool(it.is_external)}
                for it in f_doc.items
            ]

        # 4. Featured Categories for Homepage Grid
        categories = frappe.get_all(
            "Product Category",
            filters={"is_active": 1},
            fields=["name", "category_name", "route_slug", "category_image", "description"],
            order_by="sort_order asc, category_name asc",
            limit=6
        )
        for cat in categories:
            if cat.get("category_image"):
                cat["category_image_url"] = frappe.utils.get_url(cat["category_image"])

        # 5. Packaged Response
        design_data = {
            "brand": {
                "store_name": store_settings.store_name or "My E-Commerce Store",
                "tagline": theme.store_tagline or "",
                "logo": theme.store_logo,
                "logo_url": frappe.utils.get_url(theme.store_logo) if theme.store_logo else None,
                "favicon": theme.favicon,
                "favicon_url": frappe.utils.get_url(theme.favicon) if theme.favicon else None
            },
            "announcement_bar": {
                "enabled": bool(theme.enable_announcement_bar),
                "text": theme.announcement_text or "",
                "link": theme.announcement_link or "",
                "bg_color": theme.announcement_bg_color or "#0f172a",
                "text_color": theme.announcement_text_color or "#ffffff"
            },
            "colors": {
                "primary": theme.primary_color or "#0284c7",
                "secondary": theme.secondary_color or "#0f172a",
                "accent": theme.accent_color or "#f59e0b",
                "font_family": theme.font_family or "Inter"
            },
            "footer": {
                "about_text": theme.footer_about_text or "",
                "copyright_text": theme.copyright_text or "",
                "social_links": {
                    "whatsapp": theme.social_whatsapp or "",
                    "facebook": theme.social_facebook or "",
                    "instagram": theme.social_instagram or "",
                    "tiktok": theme.social_tiktok or ""
                }
            },
            "commerce_config": {
                "currency": store_settings.currency or "PKR",
                "currency_symbol": store_settings.currency_symbol or "Rs.",
                "default_shipping_fee": float(store_settings.default_shipping_fee or 0),
                "free_shipping_threshold": float(store_settings.free_shipping_threshold or 0),
                "allow_cod": bool(store_settings.allow_cod),
                "allow_online_payment": bool(store_settings.allow_online_payment)
            },
            "banners": banners,
            "menus": {
                "header": header_menu or [],
                "footer_policies": footer_menu or []
            },
            "featured_categories": categories
        }

        return {"status": "success", "data": design_data}
    except Exception as e:
        frappe.log_error("get_store_design error", str(e))
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def get_page(slug):
    """
    Returns custom CMS page content (e.g. About Us, Shipping Policy, Terms).
    """
    try:
        if not slug:
            return {"status": "error", "message": _("Page slug is required")}

        if not frappe.db.exists("Store Page", {"route_slug": slug, "is_published": 1}):
            return {"status": "error", "message": _("Page not found"), "code": 404}

        page = frappe.get_doc("Store Page", {"route_slug": slug, "is_published": 1})
        return {
            "status": "success",
            "data": {
                "title": page.title,
                "route_slug": page.route_slug,
                "content": page.content,
                "meta_description": page.meta_description or ""
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

