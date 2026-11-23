import frappe

def get_context(context):
	if frappe.session.user == "Guest":
		frappe.local.flags.redirect_location = "/login?redirect-to=/theme-editor"
		raise frappe.Redirect

	store = frappe.get_single("Store Settings")
	theme = frappe.get_single("Store Theme Settings")

	banners = frappe.get_all(
		"Store Banner",
		filters={"is_active": 1},
		fields=["name", "title", "heading", "subheading", "button_text", "button_link", "image"],
		order_by="sort_order asc"
	)

	categories = frappe.get_all(
		"Product Category",
		filters={"is_active": 1},
		fields=["name", "category_name", "route_slug", "category_image", "description"],
		order_by="sort_order asc"
	)

	products = frappe.get_all(
		"Product",
		filters={"is_active": 1},
		fields=["name", "title", "route_slug", "sku", "category", "price", "compare_at_price", "primary_image", "short_description"],
		limit=8
	)

	context.update({
		"store": store,
		"theme": theme,
		"banners": banners,
		"categories": categories,
		"products": products,
		"primary_banner": banners[0] if banners else None,
		"user": frappe.session.user
	})

	return context
