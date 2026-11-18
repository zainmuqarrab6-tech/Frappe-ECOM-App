import frappe

def get_context(context):
	# 1. Store & Theme Settings
	store = frappe.get_single("Store Settings")
	theme = frappe.get_single("Store Theme Settings")

	# 2. Hero Banners
	banners = frappe.get_all(
		"Store Banner",
		filters={"is_active": 1},
		fields=["title", "banner_type", "heading", "subheading", "button_text", "button_link", "image"],
		order_by="sort_order asc"
	)

	# 3. Categories
	categories = frappe.get_all(
		"Product Category",
		filters={"is_active": 1},
		fields=["name", "category_name", "route_slug", "description", "category_image"],
		order_by="category_name asc"
	)

	# 4. Featured & All Active Products
	products = frappe.get_all(
		"Product",
		filters={"is_active": 1},
		fields=[
			"name", "title", "route_slug", "sku", "category", "brand",
			"price", "compare_at_price", "is_featured", "is_in_stock",
			"short_description", "primary_image"
		],
		order_by="is_featured desc, creation desc"
	)

	# 5. Menus
	header_menu_items = []
	if frappe.db.exists("Store Navigation Menu", "Header Main Menu"):
		header_menu_items = frappe.get_doc("Store Navigation Menu", "Header Main Menu").items

	footer_menu_items = []
	if frappe.db.exists("Store Navigation Menu", "Footer Policies Menu"):
		footer_menu_items = frappe.get_doc("Store Navigation Menu", "Footer Policies Menu").items

	# 6. Customer Reviews
	reviews = frappe.get_all(
		"Product Review",
		filters={"status": "Approved"},
		fields=["customer_name", "rating", "title", "review_text", "creation"],
		order_by="creation desc",
		limit=6
	)

	# 7. Available Store Themes
	available_themes = frappe.get_all(
		"Store Theme",
		fields=["name", "theme_name", "category", "is_active", "primary_color", "badge_text"],
		order_by="is_active desc, theme_name asc"
	)

	# 8. User session status
	is_logged_in = frappe.session.user != "Guest"
	is_manager = is_logged_in and "System Manager" in frappe.get_roles()

	context.update({
		"store": store,
		"theme": theme,
		"banners": banners,
		"categories": categories,
		"products": products,
		"header_menu_items": header_menu_items,
		"footer_menu_items": footer_menu_items,
		"reviews": reviews,
		"available_themes": available_themes,
		"is_logged_in": is_logged_in,
		"is_manager": is_manager,
	})

	return context
