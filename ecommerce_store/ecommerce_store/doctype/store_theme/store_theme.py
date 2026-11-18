# Copyright (c) 2026, Zain and contributors
# For license information, please see license.txt

import os
import json
import subprocess
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


@frappe.whitelist()
def deploy_theme_from_github(repo_url, branch="main", theme_name=None, publish_now=False):
	"""
	Clones a theme from GitHub repository, parses theme metadata/config,
	creates or updates a Store Theme document, and optionally publishes it immediately.
	"""
	if not frappe.has_permission("Store Theme", "create"):
		frappe.throw("Not permitted to install themes", frappe.PermissionError)

	if not repo_url:
		frappe.throw("GitHub Repository URL is required")

	repo_url = repo_url.strip()
	branch = (branch or "main").strip()

	# Derive a clean theme name if not provided
	if not theme_name:
		repo_clean = repo_url.rstrip("/").split("/")[-1]
		if repo_clean.endswith(".git"):
			repo_clean = repo_clean[:-4]
		theme_name = repo_clean.replace("-", " ").replace("_", " ").title()

	target_dir = os.path.join(frappe.get_site_path("public", "themes"), frappe.scrub(theme_name))
	os.makedirs(os.path.dirname(target_dir), exist_ok=True)

	try:
		if os.path.exists(target_dir):
			subprocess.run(
				["git", "-C", target_dir, "pull", "origin", branch],
				check=True,
				capture_output=True,
				text=True
			)
		else:
			subprocess.run(
				["git", "clone", "--depth", "1", "--branch", branch, repo_url, target_dir],
				check=True,
				capture_output=True,
				text=True
			)
	except subprocess.CalledProcessError as e:
		err_msg = e.stderr or e.stdout or str(e)
		frappe.throw(f"Git Clone / Pull failed: {err_msg}")

	# Check for theme.json or config.json inside the repo
	config_file = os.path.join(target_dir, "theme.json")
	if not os.path.exists(config_file):
		config_file = os.path.join(target_dir, "config.json")

	theme_meta = {}
	if os.path.exists(config_file):
		try:
			with open(config_file, "r") as f:
				theme_meta = json.load(f)
		except Exception:
			pass

	# Read custom CSS if present
	custom_css = ""
	css_file = os.path.join(target_dir, "style.css")
	if os.path.exists(css_file):
		try:
			with open(css_file, "r") as f:
				custom_css = f.read()
		except Exception:
			pass

	# Create or update Store Theme document
	if frappe.db.exists("Store Theme", theme_name):
		doc = frappe.get_doc("Store Theme", theme_name)
	else:
		doc = frappe.new_doc("Store Theme")
		doc.theme_name = theme_name

	doc.category = theme_meta.get("category", "General & Multipurpose")
	doc.description = theme_meta.get("description", f"Imported from {repo_url} (branch: {branch})")
	doc.badge_text = "GitHub"
	doc.version = theme_meta.get("version", "1.0.0")
	doc.primary_color = theme_meta.get("primary_color", "#0284c7")
	doc.secondary_color = theme_meta.get("secondary_color", "#0f172a")
	doc.accent_color = theme_meta.get("accent_color", "#f59e0b")
	doc.bg_color = theme_meta.get("bg_color", "#ffffff")
	doc.text_color = theme_meta.get("text_color", "#1e293b")
	doc.font_heading = theme_meta.get("font_heading", "Plus Jakarta Sans")
	doc.font_body = theme_meta.get("font_body", "Inter")
	doc.header_style = theme_meta.get("header_style", "Minimal Top Bar")
	doc.hero_banner_style = theme_meta.get("hero_banner_style", "Full Width Hero Slider")
	doc.product_card_style = theme_meta.get("product_card_style", "Card with Shadow")
	doc.cart_type = theme_meta.get("cart_type", "Slide-out Drawer Cart")
	doc.footer_style = theme_meta.get("footer_style", "Multi-column Mega Footer")
	doc.custom_css = custom_css or theme_meta.get("custom_css", "")
	doc.is_active = 1 if frappe.utils.cint(publish_now) else 0

	doc.save(ignore_permissions=True)
	frappe.db.commit()

	if doc.is_active:
		sync_theme_to_settings(doc)

	return {
		"status": "success",
		"message": f"Theme '{doc.theme_name}' successfully deployed from GitHub!",
		"theme": doc.as_dict()
	}
