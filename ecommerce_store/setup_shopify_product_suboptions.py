import frappe

def setup():
	print("Setting up Shopify-style Product sub-options...")

	# 1. Store Purchase Order Item (Child Table)
	if not frappe.db.exists("DocType", "Store Purchase Order Item"):
		doc = frappe.get_doc({
			"doctype": "DocType",
			"name": "Store Purchase Order Item",
			"module": "Ecommerce Store",
			"custom": 0,
			"istable": 1,
			"fields": [
				{"fieldname": "product", "fieldtype": "Link", "label": "Product", "options": "Product", "reqd": 1, "in_list_view": 1},
				{"fieldname": "sku", "fieldtype": "Data", "label": "SKU", "fetch_from": "product.sku", "in_list_view": 1, "read_only": 1},
				{"fieldname": "quantity_ordered", "fieldtype": "Int", "label": "Qty Ordered", "reqd": 1, "default": "1", "in_list_view": 1},
				{"fieldname": "quantity_received", "fieldtype": "Int", "label": "Qty Received", "default": "0", "in_list_view": 1},
				{"fieldname": "unit_cost", "fieldtype": "Currency", "label": "Unit Cost", "reqd": 1, "in_list_view": 1},
				{"fieldname": "total_cost", "fieldtype": "Currency", "label": "Total Cost", "read_only": 1, "in_list_view": 1}
			],
			"permissions": []
		})
		doc.insert(ignore_permissions=True)
		print("Created DocType: Store Purchase Order Item")

	# 2. Store Purchase Order
	if not frappe.db.exists("DocType", "Store Purchase Order"):
		doc = frappe.get_doc({
			"doctype": "DocType",
			"name": "Store Purchase Order",
			"module": "Ecommerce Store",
			"custom": 0,
			"autoname": "PO-.YYYY.-.#####",
			"is_submittable": 1,
			"show_name_in_global_search": 1,
			"fields": [
				{"fieldname": "naming_series", "fieldtype": "Select", "label": "Series", "options": "PO-.YYYY.-.#####", "hidden": 1, "default": "PO-.YYYY.-.#####"},
				{"fieldname": "sec_overview", "fieldtype": "Section Break", "label": "Purchase Order Details"},
				{"fieldname": "supplier_name", "fieldtype": "Data", "label": "Supplier / Vendor Name", "reqd": 1, "in_list_view": 1},
				{"fieldname": "order_date", "fieldtype": "Date", "label": "Order Date", "default": "Today", "reqd": 1, "in_list_view": 1},
				{"fieldname": "col_1", "fieldtype": "Column Break"},
				{"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Draft\nOrdered\nPartially Received\nReceived\nCancelled", "default": "Draft", "in_list_view": 1},
				{"fieldname": "expected_arrival", "fieldtype": "Date", "label": "Expected Arrival Date"},
				{"fieldname": "sec_shipping", "fieldtype": "Section Break", "label": "Destination & Payment"},
				{"fieldname": "destination_location", "fieldtype": "Data", "label": "Receiving Location / Warehouse", "default": "Main Distribution Center"},
				{"fieldname": "payment_terms", "fieldtype": "Select", "label": "Payment Terms", "options": "Payment on Delivery\nNet 15\nNet 30\nNet 60\nPrepaid", "default": "Payment on Delivery"},
				{"fieldname": "col_2", "fieldtype": "Column Break"},
				{"fieldname": "tracking_number", "fieldtype": "Data", "label": "Tracking Number"},
				{"fieldname": "shipping_carrier", "fieldtype": "Data", "label": "Shipping Carrier"},
				{"fieldname": "sec_items", "fieldtype": "Section Break", "label": "Products Ordered"},
				{"fieldname": "items", "fieldtype": "Table", "label": "Products", "options": "Store Purchase Order Item", "reqd": 1},
				{"fieldname": "sec_totals", "fieldtype": "Section Break", "label": "Totals & Notes"},
				{"fieldname": "total_quantity", "fieldtype": "Int", "label": "Total Quantity", "read_only": 1},
				{"fieldname": "total_cost", "fieldtype": "Currency", "label": "Total Cost", "read_only": 1, "in_list_view": 1},
				{"fieldname": "col_3", "fieldtype": "Column Break"},
				{"fieldname": "notes", "fieldtype": "Small Text", "label": "Supplier Notes / Instructions"},
				{"fieldname": "amended_from", "fieldtype": "Link", "label": "Amended From", "options": "Store Purchase Order", "read_only": 1, "no_copy": 1, "print_hide": 1}
			],
			"permissions": [
				{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "submit": 1, "cancel": 1, "amend": 1}
			]
		})
		doc.insert(ignore_permissions=True)
		print("Created DocType: Store Purchase Order")

	# 3. Store Inventory Transfer Item (Child Table)
	if not frappe.db.exists("DocType", "Store Inventory Transfer Item"):
		doc = frappe.get_doc({
			"doctype": "DocType",
			"name": "Store Inventory Transfer Item",
			"module": "Ecommerce Store",
			"custom": 0,
			"istable": 1,
			"fields": [
				{"fieldname": "product", "fieldtype": "Link", "label": "Product", "options": "Product", "reqd": 1, "in_list_view": 1},
				{"fieldname": "sku", "fieldtype": "Data", "label": "SKU", "fetch_from": "product.sku", "in_list_view": 1, "read_only": 1},
				{"fieldname": "quantity_to_transfer", "fieldtype": "Int", "label": "Qty to Transfer", "reqd": 1, "default": "1", "in_list_view": 1},
				{"fieldname": "quantity_received", "fieldtype": "Int", "label": "Qty Received", "default": "0", "in_list_view": 1}
			],
			"permissions": []
		})
		doc.insert(ignore_permissions=True)
		print("Created DocType: Store Inventory Transfer Item")

	# 4. Store Inventory Transfer
	if not frappe.db.exists("DocType", "Store Inventory Transfer"):
		doc = frappe.get_doc({
			"doctype": "DocType",
			"name": "Store Inventory Transfer",
			"module": "Ecommerce Store",
			"custom": 0,
			"autoname": "TRF-.YYYY.-.#####",
			"is_submittable": 1,
			"show_name_in_global_search": 1,
			"fields": [
				{"fieldname": "naming_series", "fieldtype": "Select", "label": "Series", "options": "TRF-.YYYY.-.#####", "hidden": 1, "default": "TRF-.YYYY.-.#####"},
				{"fieldname": "sec_overview", "fieldtype": "Section Break", "label": "Transfer Route & Schedule"},
				{"fieldname": "origin_location", "fieldtype": "Data", "label": "Origin Location", "reqd": 1, "default": "Main Fulfillment Center", "in_list_view": 1},
				{"fieldname": "destination_location", "fieldtype": "Data", "label": "Destination Location", "reqd": 1, "default": "Retail Outlet 1", "in_list_view": 1},
				{"fieldname": "col_1", "fieldtype": "Column Break"},
				{"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Draft\nIn Transit\nPartially Received\nCompleted\nCancelled", "default": "Draft", "in_list_view": 1},
				{"fieldname": "transfer_date", "fieldtype": "Date", "label": "Transfer Date", "default": "Today", "reqd": 1},
				{"fieldname": "expected_arrival", "fieldtype": "Date", "label": "Expected Arrival Date"},
				{"fieldname": "sec_logistics", "fieldtype": "Section Break", "label": "Logistics & Tracking"},
				{"fieldname": "carrier", "fieldtype": "Data", "label": "Shipping Carrier / Fleet"},
				{"fieldname": "tracking_number", "fieldtype": "Data", "label": "Tracking Number"},
				{"fieldname": "col_2", "fieldtype": "Column Break"},
				{"fieldname": "notes", "fieldtype": "Small Text", "label": "Transfer Notes"},
				{"fieldname": "sec_items", "fieldtype": "Section Break", "label": "Transferred Items"},
				{"fieldname": "items", "fieldtype": "Table", "label": "Products to Transfer", "options": "Store Inventory Transfer Item", "reqd": 1},
				{"fieldname": "amended_from", "fieldtype": "Link", "label": "Amended From", "options": "Store Inventory Transfer", "read_only": 1, "no_copy": 1, "print_hide": 1}
			],
			"permissions": [
				{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "submit": 1, "cancel": 1, "amend": 1}
			]
		})
		doc.insert(ignore_permissions=True)
		print("Created DocType: Store Inventory Transfer")

	# 5. Store Gift Card
	if not frappe.db.exists("DocType", "Store Gift Card"):
		doc = frappe.get_doc({
			"doctype": "DocType",
			"name": "Store Gift Card",
			"module": "Ecommerce Store",
			"custom": 0,
			"autoname": "field:card_code",
			"show_name_in_global_search": 1,
			"fields": [
				{"fieldname": "sec_card", "fieldtype": "Section Break", "label": "Gift Card Details"},
				{"fieldname": "card_code", "fieldtype": "Data", "label": "Gift Card Code", "reqd": 1, "unique": 1, "in_list_view": 1},
				{"fieldname": "initial_value", "fieldtype": "Currency", "label": "Initial Balance", "reqd": 1, "in_list_view": 1},
				{"fieldname": "current_balance", "fieldtype": "Currency", "label": "Current Balance", "reqd": 1, "in_list_view": 1},
				{"fieldname": "col_1", "fieldtype": "Column Break"},
				{"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Active\nPartially Used\nRedeemed\nExpired\nDisabled", "default": "Active", "in_list_view": 1},
				{"fieldname": "currency", "fieldtype": "Data", "label": "Currency", "default": "PKR"},
				{"fieldname": "expiry_date", "fieldtype": "Date", "label": "Expiry Date"},
				{"fieldname": "sec_recipient", "fieldtype": "Section Break", "label": "Recipient & Customer"},
				{"fieldname": "customer", "fieldtype": "Link", "label": "Customer", "options": "Store Customer"},
				{"fieldname": "recipient_email", "fieldtype": "Data", "label": "Recipient Email", "in_list_view": 1},
				{"fieldname": "col_2", "fieldtype": "Column Break"},
				{"fieldname": "personal_message", "fieldtype": "Small Text", "label": "Personal Greeting Message"},
				{"fieldname": "notes", "fieldtype": "Small Text", "label": "Internal Notes"}
			],
			"permissions": [
				{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}
			]
		})
		doc.insert(ignore_permissions=True)
		print("Created DocType: Store Gift Card")

	# 6. Create sample Purchase Order
	prod = frappe.db.get_value("Product", {}, ["name", "price"], as_dict=True)
	if prod and not frappe.db.exists("Store Purchase Order", {"supplier_name": "Apex Tech Global Distribution"}):
		po = frappe.get_doc({
			"doctype": "Store Purchase Order",
			"supplier_name": "Apex Tech Global Distribution",
			"order_date": frappe.utils.today(),
			"status": "Ordered",
			"destination_location": "Main Karachi Warehouse",
			"payment_terms": "Net 30",
			"tracking_number": "TCS-98124510",
			"shipping_carrier": "TCS Freight",
			"items": [
				{
					"product": prod.name,
					"quantity_ordered": 50,
					"quantity_received": 0,
					"unit_cost": float(prod.price or 4000) * 0.7,
					"total_cost": (float(prod.price or 4000) * 0.7) * 50
				}
			],
			"total_quantity": 50,
			"total_cost": (float(prod.price or 4000) * 0.7) * 50
		})
		po.insert(ignore_permissions=True)
		print("Created sample Purchase Order.")

	# 7. Create sample Inventory Transfer
	if prod and not frappe.db.exists("Store Inventory Transfer", {"origin_location": "Main Karachi Warehouse"}):
		trf = frappe.get_doc({
			"doctype": "Store Inventory Transfer",
			"origin_location": "Main Karachi Warehouse",
			"destination_location": "Lahore Mall Retail Outlet",
			"status": "In Transit",
			"transfer_date": frappe.utils.today(),
			"carrier": "Internal Logistics Van #4",
			"tracking_number": "TRF-LHR-001",
			"items": [
				{
					"product": prod.name,
					"quantity_to_transfer": 15,
					"quantity_received": 0
				}
			]
		})
		trf.insert(ignore_permissions=True)
		print("Created sample Inventory Transfer.")

	# 8. Create sample Gift Card
	if not frappe.db.exists("Store Gift Card", "GIFT-5000-ECOM-PRO"):
		gc = frappe.get_doc({
			"doctype": "Store Gift Card",
			"card_code": "GIFT-5000-ECOM-PRO",
			"initial_value": 5000,
			"current_balance": 5000,
			"currency": "PKR",
			"status": "Active",
			"recipient_email": "vip.shopper@example.com",
			"personal_message": "Happy Birthday! Enjoy Rs. 5000 off your next order."
		})
		gc.insert(ignore_permissions=True)
		print("Created sample Gift Card.")

	frappe.db.commit()
	print("Sub-options setup completed successfully!")

if __name__ == "__main__":
	setup()
