import frappe
import json
import os

def update_all():
	print("Updating Sidebar and Workspace with Shopify-style Product sub-options...")

	sidebar_items = [
		{
			"added": 0,
			"child": 0,
			"collapsible": 0,
			"hidden": 0,
			"icon": "house",
			"indent": 0,
			"is_default_module": 0,
			"keep_closed": 0,
			"label": "Home",
			"link_to": "Ecommerce Store",
			"link_type": "Workspace",
			"open_in_new_tab": 0,
			"show_arrow": 0,
			"type": "Link"
		},
		{
			"added": 0,
			"child": 0,
			"collapsible": 0,
			"hidden": 0,
			"icon": "inbox",
			"indent": 0,
			"is_default_module": 0,
			"keep_closed": 0,
			"label": "Orders",
			"link_to": "Store Order",
			"link_type": "DocType",
			"open_in_new_tab": 0,
			"show_arrow": 0,
			"type": "Link"
		},
		# Products & its Shopify Sub-options
		{
			"added": 0,
			"child": 0,
			"collapsible": 1,
			"hidden": 0,
			"icon": "tag",
			"indent": 0,
			"is_default_module": 0,
			"keep_closed": 0,
			"label": "Products",
			"link_to": "Product",
			"link_type": "DocType",
			"open_in_new_tab": 0,
			"show_arrow": 1,
			"type": "Link"
		},
		{
			"added": 0,
			"child": 1,
			"collapsible": 0,
			"hidden": 0,
			"icon": "folder-tree",
			"indent": 1,
			"is_default_module": 0,
			"keep_closed": 0,
			"label": "Collections",
			"link_to": "Product Category",
			"link_type": "DocType",
			"open_in_new_tab": 0,
			"show_arrow": 0,
			"type": "Link"
		},
		{
			"added": 0,
			"child": 1,
			"collapsible": 0,
			"hidden": 0,
			"icon": "boxes",
			"indent": 1,
			"is_default_module": 0,
			"keep_closed": 0,
			"label": "Inventory",
			"link_to": "Stock Adjustment",
			"link_type": "DocType",
			"open_in_new_tab": 0,
			"show_arrow": 0,
			"type": "Link"
		},
		{
			"added": 0,
			"child": 1,
			"collapsible": 0,
			"hidden": 0,
			"icon": "file-text",
			"indent": 1,
			"is_default_module": 0,
			"keep_closed": 0,
			"label": "Purchase orders",
			"link_to": "Store Purchase Order",
			"link_type": "DocType",
			"open_in_new_tab": 0,
			"show_arrow": 0,
			"type": "Link"
		},
		{
			"added": 0,
			"child": 1,
			"collapsible": 0,
			"hidden": 0,
			"icon": "truck",
			"indent": 1,
			"is_default_module": 0,
			"keep_closed": 0,
			"label": "Transfers",
			"link_to": "Store Inventory Transfer",
			"link_type": "DocType",
			"open_in_new_tab": 0,
			"show_arrow": 0,
			"type": "Link"
		},
		{
			"added": 0,
			"child": 1,
			"collapsible": 0,
			"hidden": 0,
			"icon": "gift",
			"indent": 1,
			"is_default_module": 0,
			"keep_closed": 0,
			"label": "Gift cards",
			"link_to": "Store Gift Card",
			"link_type": "DocType",
			"open_in_new_tab": 0,
			"show_arrow": 0,
			"type": "Link"
		},
		{
			"added": 0,
			"child": 0,
			"collapsible": 0,
			"hidden": 0,
			"icon": "users",
			"indent": 0,
			"is_default_module": 0,
			"keep_closed": 0,
			"label": "Customers",
			"link_to": "Store Customer",
			"link_type": "DocType",
			"open_in_new_tab": 0,
			"show_arrow": 0,
			"type": "Link"
		},
		{
			"added": 0,
			"child": 0,
			"collapsible": 0,
			"hidden": 0,
			"icon": "badge-percent",
			"indent": 0,
			"is_default_module": 0,
			"keep_closed": 0,
			"label": "Discounts",
			"link_to": "Store Coupon",
			"link_type": "DocType",
			"open_in_new_tab": 0,
			"show_arrow": 0,
			"type": "Link"
		},
		{
			"added": 0,
			"child": 0,
			"collapsible": 0,
			"hidden": 0,
			"icon": "image",
			"indent": 0,
			"is_default_module": 0,
			"keep_closed": 0,
			"label": "Content",
			"link_to": "Store Page",
			"link_type": "DocType",
			"open_in_new_tab": 0,
			"show_arrow": 0,
			"type": "Link"
		},
		{
			"added": 0,
			"child": 0,
			"collapsible": 1,
			"hidden": 0,
			"icon": "store",
			"indent": 0,
			"is_default_module": 0,
			"keep_closed": 0,
			"label": "Sales channels",
			"link_type": "DocType",
			"open_in_new_tab": 0,
			"show_arrow": 1,
			"type": "Section Break"
		},
		{
			"added": 0,
			"child": 1,
			"collapsible": 0,
			"hidden": 0,
			"icon": "store",
			"indent": 1,
			"is_default_module": 0,
			"keep_closed": 0,
			"label": "Online Store",
			"link_to": "Store Theme Settings",
			"link_type": "DocType",
			"open_in_new_tab": 0,
			"show_arrow": 0,
			"type": "Link"
		},
		{
			"added": 0,
			"child": 1,
			"collapsible": 0,
			"hidden": 0,
			"icon": "layout-template",
			"indent": 1,
			"is_default_module": 0,
			"keep_closed": 0,
			"label": "Templates Library",
			"link_to": "Store Theme",
			"link_type": "DocType",
			"open_in_new_tab": 0,
			"show_arrow": 0,
			"type": "Link"
		},
		{
			"added": 0,
			"child": 1,
			"collapsible": 0,
			"hidden": 0,
			"icon": "compass",
			"indent": 1,
			"is_default_module": 0,
			"keep_closed": 0,
			"label": "Navigation",
			"link_to": "Store Navigation Menu",
			"link_type": "DocType",
			"open_in_new_tab": 0,
			"show_arrow": 0,
			"type": "Link"
		},
		{
			"added": 0,
			"child": 1,
			"collapsible": 0,
			"hidden": 0,
			"icon": "image",
			"indent": 1,
			"is_default_module": 0,
			"keep_closed": 0,
			"label": "Banners",
			"link_to": "Store Banner",
			"link_type": "DocType",
			"open_in_new_tab": 0,
			"show_arrow": 0,
			"type": "Link"
		},
		{
			"added": 0,
			"child": 0,
			"collapsible": 0,
			"hidden": 0,
			"icon": "settings",
			"indent": 0,
			"is_default_module": 0,
			"keep_closed": 0,
			"label": "Settings",
			"link_to": "Store Settings",
			"link_type": "DocType",
			"open_in_new_tab": 0,
			"show_arrow": 0,
			"type": "Link"
		}
	]

	# Update Sidebar JSON file
	sidebar_json_path = frappe.get_app_path("ecommerce_store", "ecommerce_store", "sidebar", "ecommerce_store", "ecommerce_store.json")
	if os.path.exists(sidebar_json_path):
		with open(sidebar_json_path, "r") as f:
			data = json.load(f)
		data["items"] = sidebar_items
		with open(sidebar_json_path, "w") as f:
			json.dump(data, f, indent=1)
		print(f"Updated {sidebar_json_path}")

	# Update Sidebar Doc in DB
	if frappe.db.exists("Sidebar", "Ecommerce Store"):
		sb = frappe.get_doc("Sidebar", "Ecommerce Store")
		sb.set("items", [])
		for item in sidebar_items:
			sb.append("items", item)
		sb.save(ignore_permissions=True)
		print("Updated Sidebar in DB")

	# Update Workspace Links & Shortcuts
	if frappe.db.exists("Workspace", "Ecommerce Store"):
		ws = frappe.get_doc("Workspace", "Ecommerce Store")
		
		# Ensure shortcuts for the sub-options exist
		existing_shortcuts = [s.label for s in ws.shortcuts]
		new_shortcuts = [
			{"label": "Collections", "link_to": "Product Category", "type": "DocType", "color": "Green"},
			{"label": "Purchase Orders", "link_to": "Store Purchase Order", "type": "DocType", "color": "Blue"},
			{"label": "Stock Transfers", "link_to": "Store Inventory Transfer", "type": "DocType", "color": "Orange"},
			{"label": "Gift Cards", "link_to": "Store Gift Card", "type": "DocType", "color": "Purple"}
		]
		for sc in new_shortcuts:
			if sc["label"] not in existing_shortcuts:
				ws.append("shortcuts", sc)

		# Ensure cards/links exist
		existing_links = [l.label for l in ws.links]
		catalog_links = [
			{"type": "Link", "link_type": "DocType", "link_to": "Product Category", "label": "Collections (Categories)"},
			{"type": "Link", "link_type": "DocType", "link_to": "Store Purchase Order", "label": "Purchase Orders (Suppliers)"},
			{"type": "Link", "link_type": "DocType", "link_to": "Store Inventory Transfer", "label": "Transfers (Locations)"},
			{"type": "Link", "link_type": "DocType", "link_to": "Store Gift Card", "label": "Gift Cards"}
		]
		for cl in catalog_links:
			if cl["label"] not in existing_links:
				ws.append("links", cl)

		ws.save(ignore_permissions=True)
		print("Updated Workspace in DB")

		# Write back to Workspace JSON
		ws_json_path = frappe.get_app_path("ecommerce_store", "ecommerce_store", "workspace", "ecommerce_store", "ecommerce_store.json")
		if os.path.exists(ws_json_path):
			with open(ws_json_path, "w") as f:
				json.dump(ws.as_dict(), f, indent=1, default=str)
			print(f"Updated {ws_json_path}")

	frappe.db.commit()
	print("Sidebar and Workspace updated successfully!")

if __name__ == "__main__":
	update_all()
