# Copyright (c) 2026, Zain and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class StoreTheme(Document):
	def on_update(self):
		if self.is_active:
			# Ensure only one theme is marked active
			frappe.db.sql(
				"UPDATE `tabStore Theme` SET is_active = 0 WHERE name != %s",
				(self.name,)
			)
			# Sync to Store Theme Settings
			sync_theme_to_settings(self)


def sync_theme_to_settings(theme_doc):
	try:
		theme_settings = frappe.get_doc("Store Theme Settings")
		theme_settings.active_theme = theme_doc.name
		theme_settings.active_theme_name = theme_doc.theme_name
		theme_settings.primary_color = theme_doc.primary_color
		theme_settings.secondary_color = theme_doc.secondary_color
		theme_settings.accent_color = theme_doc.accent_color
		theme_settings.bg_color = theme_doc.bg_color
		theme_settings.text_color = theme_doc.text_color
		theme_settings.font_heading = theme_doc.font_heading
		theme_settings.font_body = theme_doc.font_body
		theme_settings.header_style = theme_doc.header_style
		theme_settings.hero_banner_style = theme_doc.hero_banner_style
		theme_settings.product_card_style = theme_doc.product_card_style
		theme_settings.cart_type = theme_doc.cart_type
		theme_settings.footer_style = theme_doc.footer_style
		theme_settings.custom_css = theme_doc.custom_css or ""
		theme_settings.save(ignore_permissions=True)
		frappe.db.commit()
	except Exception as e:
		frappe.log_error(title="Failed to sync theme to settings", message=str(e))


@frappe.whitelist()
def publish_theme(theme_name):
	"""Activates and publishes a theme as the store's current active template."""
	if not frappe.has_permission("Store Theme Settings", "write"):
		frappe.throw("Not permitted to change theme settings", frappe.PermissionError)

	theme = frappe.get_doc("Store Theme", theme_name)
	theme.is_active = 1
	theme.save()
	frappe.db.commit()

	return {
		"status": "success",
		"message": f"Theme '{theme.theme_name}' has been published successfully!",
		"theme": theme.as_dict()
	}


@frappe.whitelist()
def get_theme_library():
	"""Returns all templates in the theme library."""
	themes = frappe.get_all(
		"Store Theme",
		fields=[
			"name", "theme_name", "version", "category", "is_active",
			"badge_text", "description", "preview_image",
			"primary_color", "secondary_color", "accent_color", "bg_color", "text_color",
			"font_heading", "font_body", "header_style", "hero_banner_style",
			"product_card_style", "cart_type", "footer_style"
		],
		order_by="is_active DESC, theme_name ASC"
	)
	return themes


@frappe.whitelist()
def duplicate_theme(theme_name, new_name=None):
	"""Duplicates a theme for customization."""
	if not frappe.has_permission("Store Theme", "create"):
		frappe.throw("Not permitted", frappe.PermissionError)

	src = frappe.get_doc("Store Theme", theme_name)
	new_doc = frappe.copy_doc(src)
	new_doc.theme_name = new_name or f"{src.theme_name} Copy"
	new_doc.is_active = 0
	new_doc.badge_text = "Custom"
	new_doc.insert()
	frappe.db.commit()

	return {
		"status": "success",
		"message": f"Template '{new_doc.theme_name}' created!",
		"theme": new_doc.as_dict()
	}
