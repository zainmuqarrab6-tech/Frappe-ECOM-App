import frappe

def create_doctypes():
    print("Starting DocType creation for Ecommerce Store...")

    doctypes = [
        # 1. Product Image Item (Child Table)
        {
            "doctype": "DocType",
            "name": "Product Image Item",
            "module": "Ecommerce Store",
            "custom": 0,
            "istable": 1,
            "fields": [
                {"fieldname": "image", "fieldtype": "Attach Image", "label": "Image", "reqd": 1},
                {"fieldname": "alt_text", "fieldtype": "Data", "label": "Alt Text", "in_list_view": 1},
                {"fieldname": "is_primary", "fieldtype": "Check", "label": "Primary Image", "default": "0", "in_list_view": 1}
            ],
            "permissions": []
        },

        # 2. Product Attribute Option (Child Table)
        {
            "doctype": "DocType",
            "name": "Product Attribute Option",
            "module": "Ecommerce Store",
            "custom": 0,
            "istable": 1,
            "fields": [
                {"fieldname": "attribute_name", "fieldtype": "Data", "label": "Attribute Name (e.g. Size)", "reqd": 1, "in_list_view": 1},
                {"fieldname": "attribute_value", "fieldtype": "Data", "label": "Attribute Value (e.g. XL)", "reqd": 1, "in_list_view": 1}
            ],
            "permissions": []
        },

        # 3. Product Category
        {
            "doctype": "DocType",
            "name": "Product Category",
            "module": "Ecommerce Store",
            "custom": 0,
            "autoname": "field:route_slug",
            "show_name_in_global_search": 1,
            "fields": [
                {"fieldname": "category_name", "fieldtype": "Data", "label": "Category Name", "reqd": 1, "unique": 1, "in_list_view": 1},
                {"fieldname": "route_slug", "fieldtype": "Data", "label": "URL Slug", "reqd": 1, "unique": 1, "in_list_view": 1},
                {"fieldname": "parent_category", "fieldtype": "Link", "label": "Parent Category", "options": "Product Category"},
                {"fieldname": "column_break_1", "fieldtype": "Column Break"},
                {"fieldname": "category_image", "fieldtype": "Attach Image", "label": "Category Image"},
                {"fieldname": "sort_order", "fieldtype": "Int", "label": "Sort Order", "default": "0"},
                {"fieldname": "is_active", "fieldtype": "Check", "label": "Is Active", "default": "1", "in_list_view": 1},
                {"fieldname": "section_desc", "fieldtype": "Section Break", "label": "Description"},
                {"fieldname": "description", "fieldtype": "Small Text", "label": "Description"}
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "Guest", "read": 1}
            ]
        },

        # 4. Product Brand
        {
            "doctype": "DocType",
            "name": "Product Brand",
            "module": "Ecommerce Store",
            "custom": 0,
            "autoname": "field:route_slug",
            "fields": [
                {"fieldname": "brand_name", "fieldtype": "Data", "label": "Brand Name", "reqd": 1, "unique": 1, "in_list_view": 1},
                {"fieldname": "route_slug", "fieldtype": "Data", "label": "URL Slug", "reqd": 1, "unique": 1, "in_list_view": 1},
                {"fieldname": "column_break_1", "fieldtype": "Column Break"},
                {"fieldname": "logo", "fieldtype": "Attach Image", "label": "Brand Logo"},
                {"fieldname": "is_active", "fieldtype": "Check", "label": "Is Active", "default": "1", "in_list_view": 1},
                {"fieldname": "section_desc", "fieldtype": "Section Break", "label": "Description"},
                {"fieldname": "description", "fieldtype": "Small Text", "label": "Description"}
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "Guest", "read": 1}
            ]
        },

        # 5. Product
        {
            "doctype": "DocType",
            "name": "Product",
            "module": "Ecommerce Store",
            "custom": 0,
            "autoname": "PROD-.#####",
            "title_field": "title",
            "image_field": "primary_image",
            "search_fields": "sku,title,category,brand",
            "show_name_in_global_search": 1,
            "fields": [
                {"fieldname": "sec_overview", "fieldtype": "Section Break", "label": "Overview"},
                {"fieldname": "title", "fieldtype": "Data", "label": "Product Title", "reqd": 1, "in_list_view": 1, "in_global_search": 1},
                {"fieldname": "route_slug", "fieldtype": "Data", "label": "URL Slug", "reqd": 1, "unique": 1},
                {"fieldname": "sku", "fieldtype": "Data", "label": "SKU", "reqd": 1, "unique": 1, "in_list_view": 1},
                {"fieldname": "barcode", "fieldtype": "Data", "label": "Barcode"},
                {"fieldname": "col_overview", "fieldtype": "Column Break"},
                {"fieldname": "category", "fieldtype": "Link", "label": "Category", "options": "Product Category", "in_list_view": 1, "in_standard_filter": 1},
                {"fieldname": "brand", "fieldtype": "Link", "label": "Brand", "options": "Product Brand", "in_standard_filter": 1},
                {"fieldname": "is_active", "fieldtype": "Check", "label": "Is Active", "default": "1", "in_list_view": 1, "in_standard_filter": 1},
                {"fieldname": "is_featured", "fieldtype": "Check", "label": "Is Featured", "default": "0", "in_standard_filter": 1},

                {"fieldname": "sec_pricing", "fieldtype": "Section Break", "label": "Pricing & Inventory"},
                {"fieldname": "price", "fieldtype": "Currency", "label": "Price", "reqd": 1, "in_list_view": 1},
                {"fieldname": "compare_at_price", "fieldtype": "Currency", "label": "Compare-at Price (Original)"},
                {"fieldname": "cost_price", "fieldtype": "Currency", "label": "Cost Price"},
                {"fieldname": "col_pricing", "fieldtype": "Column Break"},
                {"fieldname": "track_inventory", "fieldtype": "Check", "label": "Track Inventory", "default": "1"},
                {"fieldname": "is_in_stock", "fieldtype": "Check", "label": "In Stock", "default": "1", "in_list_view": 1},
                {"fieldname": "stock_quantity", "fieldtype": "Int", "label": "Stock Quantity", "default": "10"},
                {"fieldname": "low_stock_threshold", "fieldtype": "Int", "label": "Low Stock Threshold", "default": "3"},

                {"fieldname": "sec_media", "fieldtype": "Section Break", "label": "Media"},
                {"fieldname": "primary_image", "fieldtype": "Attach Image", "label": "Primary Image"},
                {"fieldname": "images", "fieldtype": "Table", "label": "Gallery Images", "options": "Product Image Item"},

                {"fieldname": "sec_variants", "fieldtype": "Section Break", "label": "Attributes"},
                {"fieldname": "attributes", "fieldtype": "Table", "label": "Attributes & Options", "options": "Product Attribute Option"},

                {"fieldname": "sec_desc", "fieldtype": "Section Break", "label": "Descriptions"},
                {"fieldname": "short_description", "fieldtype": "Small Text", "label": "Short Summary"},
                {"fieldname": "description", "fieldtype": "Text Editor", "label": "Detailed Description"}
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "Guest", "read": 1}
            ]
        },

        # 6. Store Customer
        {
            "doctype": "DocType",
            "name": "Store Customer",
            "module": "Ecommerce Store",
            "custom": 0,
            "autoname": "CUST-.#####",
            "title_field": "customer_name",
            "search_fields": "email,phone",
            "fields": [
                {"fieldname": "customer_name", "fieldtype": "Data", "label": "Full Name", "reqd": 1, "in_list_view": 1},
                {"fieldname": "email", "fieldtype": "Data", "label": "Email", "reqd": 1, "unique": 1, "options": "Email", "in_list_view": 1},
                {"fieldname": "phone", "fieldtype": "Data", "label": "Phone", "in_list_view": 1},
                {"fieldname": "col_cust", "fieldtype": "Column Break"},
                {"fieldname": "user", "fieldtype": "Link", "label": "Frappe User Account", "options": "User"},
                {"fieldname": "is_active", "fieldtype": "Check", "label": "Is Active", "default": "1"},
                {"fieldname": "total_orders_placed", "fieldtype": "Int", "label": "Total Orders Placed", "default": "0", "read_only": 1},
                {"fieldname": "total_spent", "fieldtype": "Currency", "label": "Total Spent", "default": "0", "read_only": 1}
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}
            ]
        },

        # 7. Store Customer Address
        {
            "doctype": "DocType",
            "name": "Store Customer Address",
            "module": "Ecommerce Store",
            "custom": 0,
            "fields": [
                {"fieldname": "customer", "fieldtype": "Link", "label": "Customer", "options": "Store Customer", "reqd": 1, "in_list_view": 1},
                {"fieldname": "address_title", "fieldtype": "Data", "label": "Address Title", "default": "Home", "in_list_view": 1},
                {"fieldname": "phone", "fieldtype": "Data", "label": "Contact Phone"},
                {"fieldname": "address_line1", "fieldtype": "Data", "label": "Address Line 1", "reqd": 1},
                {"fieldname": "address_line2", "fieldtype": "Data", "label": "Address Line 2"},
                {"fieldname": "col_addr", "fieldtype": "Column Break"},
                {"fieldname": "city", "fieldtype": "Data", "label": "City", "reqd": 1, "in_list_view": 1},
                {"fieldname": "state", "fieldtype": "Data", "label": "State / Province"},
                {"fieldname": "postal_code", "fieldtype": "Data", "label": "Postal Code"},
                {"fieldname": "country", "fieldtype": "Data", "label": "Country", "default": "Pakistan"},
                {"fieldname": "is_default", "fieldtype": "Check", "label": "Default Address", "default": "0"}
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}
            ]
        },

        # 8. Store Cart Item (Child Table)
        {
            "doctype": "DocType",
            "name": "Store Cart Item",
            "module": "Ecommerce Store",
            "custom": 0,
            "istable": 1,
            "fields": [
                {"fieldname": "product", "fieldtype": "Link", "label": "Product", "options": "Product", "reqd": 1, "in_list_view": 1},
                {"fieldname": "product_name", "fieldtype": "Data", "label": "Product Name", "in_list_view": 1},
                {"fieldname": "price", "fieldtype": "Currency", "label": "Price", "in_list_view": 1},
                {"fieldname": "quantity", "fieldtype": "Int", "label": "Quantity", "default": "1", "in_list_view": 1},
                {"fieldname": "total", "fieldtype": "Currency", "label": "Total", "in_list_view": 1},
                {"fieldname": "attributes_summary", "fieldtype": "Data", "label": "Selected Attributes"}
            ],
            "permissions": []
        },

        # 9. Store Cart
        {
            "doctype": "DocType",
            "name": "Store Cart",
            "module": "Ecommerce Store",
            "custom": 0,
            "autoname": "field:cart_id",
            "fields": [
                {"fieldname": "cart_id", "fieldtype": "Data", "label": "Cart ID / Session", "reqd": 1, "unique": 1, "in_list_view": 1},
                {"fieldname": "customer", "fieldtype": "Link", "label": "Customer", "options": "Store Customer"},
                {"fieldname": "coupon_code", "fieldtype": "Data", "label": "Coupon Code"},
                {"fieldname": "col_cart", "fieldtype": "Column Break"},
                {"fieldname": "subtotal", "fieldtype": "Currency", "label": "Subtotal", "default": "0", "in_list_view": 1},
                {"fieldname": "discount_amount", "fieldtype": "Currency", "label": "Discount Amount", "default": "0"},
                {"fieldname": "total", "fieldtype": "Currency", "label": "Total", "default": "0", "in_list_view": 1},
                {"fieldname": "sec_items", "fieldtype": "Section Break", "label": "Items"},
                {"fieldname": "items", "fieldtype": "Table", "label": "Items", "options": "Store Cart Item"}
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "Guest", "read": 1, "write": 1, "create": 1}
            ]
        },

        # 10. Store Order Item (Child Table)
        {
            "doctype": "DocType",
            "name": "Store Order Item",
            "module": "Ecommerce Store",
            "custom": 0,
            "istable": 1,
            "fields": [
                {"fieldname": "product", "fieldtype": "Link", "label": "Product", "options": "Product", "in_list_view": 1},
                {"fieldname": "product_name", "fieldtype": "Data", "label": "Product Name", "reqd": 1, "in_list_view": 1},
                {"fieldname": "sku", "fieldtype": "Data", "label": "SKU"},
                {"fieldname": "price", "fieldtype": "Currency", "label": "Unit Price", "reqd": 1, "in_list_view": 1},
                {"fieldname": "quantity", "fieldtype": "Int", "label": "Quantity", "default": "1", "reqd": 1, "in_list_view": 1},
                {"fieldname": "total", "fieldtype": "Currency", "label": "Line Total", "reqd": 1, "in_list_view": 1},
                {"fieldname": "attributes_summary", "fieldtype": "Data", "label": "Selected Attributes"}
            ],
            "permissions": []
        },

        # 11. Store Order
        {
            "doctype": "DocType",
            "name": "Store Order",
            "module": "Ecommerce Store",
            "custom": 0,
            "autoname": "naming_series:",
            "search_fields": "customer_name,customer_email,customer_phone,order_status",
            "fields": [
                {"fieldname": "naming_series", "fieldtype": "Select", "label": "Series", "options": "ORD-.YYYY.-.#####", "default": "ORD-.YYYY.-.#####"},
                {"fieldname": "sec_summary", "fieldtype": "Section Break", "label": "Order Summary"},
                {"fieldname": "order_date", "fieldtype": "Datetime", "label": "Order Date", "default": "Now", "in_list_view": 1},
                {"fieldname": "order_status", "fieldtype": "Select", "label": "Order Status", "options": "Pending\nConfirmed\nProcessing\nShipped\nDelivered\nCancelled", "default": "Pending", "reqd": 1, "in_list_view": 1, "in_standard_filter": 1},
                {"fieldname": "payment_status", "fieldtype": "Select", "label": "Payment Status", "options": "Unpaid\nPaid\nFailed\nRefunded", "default": "Unpaid", "reqd": 1, "in_list_view": 1, "in_standard_filter": 1},
                {"fieldname": "col_summary", "fieldtype": "Column Break"},
                {"fieldname": "payment_method", "fieldtype": "Select", "label": "Payment Method", "options": "Cash on Delivery\nBank Transfer\nCard / Online\nEasyPaisa / JazzCash", "default": "Cash on Delivery", "reqd": 1, "in_standard_filter": 1},
                {"fieldname": "payment_id", "fieldtype": "Data", "label": "Payment / Transaction ID"},

                {"fieldname": "sec_cust", "fieldtype": "Section Break", "label": "Customer & Shipping"},
                {"fieldname": "customer", "fieldtype": "Link", "label": "Store Customer", "options": "Store Customer"},
                {"fieldname": "customer_name", "fieldtype": "Data", "label": "Customer Name", "reqd": 1, "in_list_view": 1},
                {"fieldname": "customer_email", "fieldtype": "Data", "label": "Customer Email", "reqd": 1, "options": "Email"},
                {"fieldname": "customer_phone", "fieldtype": "Data", "label": "Customer Phone", "reqd": 1, "in_list_view": 1},
                {"fieldname": "col_cust_addr", "fieldtype": "Column Break"},
                {"fieldname": "shipping_address", "fieldtype": "Small Text", "label": "Shipping Address", "reqd": 1},
                {"fieldname": "shipping_city", "fieldtype": "Data", "label": "Shipping City", "reqd": 1},
                {"fieldname": "shipping_postal_code", "fieldtype": "Data", "label": "Postal Code"},
                {"fieldname": "shipping_country", "fieldtype": "Data", "label": "Country", "default": "Pakistan"},

                {"fieldname": "sec_items", "fieldtype": "Section Break", "label": "Order Items"},
                {"fieldname": "items", "fieldtype": "Table", "label": "Items", "options": "Store Order Item", "reqd": 1},

                {"fieldname": "sec_totals", "fieldtype": "Section Break", "label": "Order Totals"},
                {"fieldname": "subtotal", "fieldtype": "Currency", "label": "Subtotal", "reqd": 1, "default": "0"},
                {"fieldname": "shipping_fee", "fieldtype": "Currency", "label": "Shipping Fee", "default": "0"},
                {"fieldname": "discount_amount", "fieldtype": "Currency", "label": "Discount Amount", "default": "0"},
                {"fieldname": "tax_amount", "fieldtype": "Currency", "label": "Tax Amount", "default": "0"},
                {"fieldname": "col_totals", "fieldtype": "Column Break"},
                {"fieldname": "coupon_code", "fieldtype": "Data", "label": "Coupon Code Used"},
                {"fieldname": "grand_total", "fieldtype": "Currency", "label": "Grand Total", "reqd": 1, "default": "0", "in_list_view": 1},

                {"fieldname": "sec_fulfillment", "fieldtype": "Section Break", "label": "Fulfillment"},
                {"fieldname": "tracking_courier", "fieldtype": "Data", "label": "Courier Name"},
                {"fieldname": "tracking_number", "fieldtype": "Data", "label": "Tracking / Airway Bill #"},
                {"fieldname": "customer_notes", "fieldtype": "Small Text", "label": "Customer Order Notes"}
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}
            ]
        },

        # 12. Store Coupon
        {
            "doctype": "DocType",
            "name": "Store Coupon",
            "module": "Ecommerce Store",
            "custom": 0,
            "autoname": "field:coupon_code",
            "fields": [
                {"fieldname": "coupon_code", "fieldtype": "Data", "label": "Coupon Code", "reqd": 1, "unique": 1, "in_list_view": 1},
                {"fieldname": "discount_type", "fieldtype": "Select", "label": "Discount Type", "options": "Percentage\nFlat Amount", "default": "Percentage", "reqd": 1, "in_list_view": 1},
                {"fieldname": "discount_value", "fieldtype": "Float", "label": "Discount Value", "reqd": 1, "in_list_view": 1},
                {"fieldname": "col_coupon", "fieldtype": "Column Break"},
                {"fieldname": "is_active", "fieldtype": "Check", "label": "Is Active", "default": "1", "in_list_view": 1},
                {"fieldname": "min_order_amount", "fieldtype": "Currency", "label": "Min Order Amount", "default": "0"},
                {"fieldname": "max_discount_amount", "fieldtype": "Currency", "label": "Max Discount Cap", "default": "0"},
                {"fieldname": "sec_dates", "fieldtype": "Section Break", "label": "Validity & Limits"},
                {"fieldname": "valid_from", "fieldtype": "Date", "label": "Valid From"},
                {"fieldname": "valid_upto", "fieldtype": "Date", "label": "Valid Upto"},
                {"fieldname": "col_usage", "fieldtype": "Column Break"},
                {"fieldname": "usage_limit", "fieldtype": "Int", "label": "Usage Limit (0 for unlimited)", "default": "0"},
                {"fieldname": "times_used", "fieldtype": "Int", "label": "Times Used", "default": "0", "read_only": 1},
                {"fieldname": "description", "fieldtype": "Small Text", "label": "Description"}
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}
            ]
        },

        # 13. Store Settings (Single)
        {
            "doctype": "DocType",
            "name": "Store Settings",
            "module": "Ecommerce Store",
            "custom": 0,
            "issingle": 1,
            "fields": [
                {"fieldname": "sec_store", "fieldtype": "Section Break", "label": "Store Details"},
                {"fieldname": "store_name", "fieldtype": "Data", "label": "Store Name", "default": "My E-Commerce Store"},
                {"fieldname": "store_email", "fieldtype": "Data", "label": "Support Email", "options": "Email"},
                {"fieldname": "store_phone", "fieldtype": "Data", "label": "Store Phone"},
                {"fieldname": "col_store", "fieldtype": "Column Break"},
                {"fieldname": "currency", "fieldtype": "Data", "label": "Currency Code", "default": "PKR"},
                {"fieldname": "currency_symbol", "fieldtype": "Data", "label": "Currency Symbol", "default": "Rs."},
                {"fieldname": "order_prefix", "fieldtype": "Data", "label": "Order Prefix", "default": "ORD-"},

                {"fieldname": "sec_checkout", "fieldtype": "Section Break", "label": "Checkout, Shipping & Taxes"},
                {"fieldname": "default_shipping_fee", "fieldtype": "Currency", "label": "Default Shipping Fee", "default": "200"},
                {"fieldname": "free_shipping_threshold", "fieldtype": "Currency", "label": "Free Shipping Minimum Order", "default": "3000"},
                {"fieldname": "tax_percentage", "fieldtype": "Percent", "label": "Sales Tax (%)", "default": "0"},
                {"fieldname": "col_checkout", "fieldtype": "Column Break"},
                {"fieldname": "allow_guest_checkout", "fieldtype": "Check", "label": "Allow Guest Checkout", "default": "1"},
                {"fieldname": "allow_cod", "fieldtype": "Check", "label": "Enable Cash on Delivery", "default": "1"},
                {"fieldname": "allow_online_payment", "fieldtype": "Check", "label": "Enable Online Payment", "default": "0"}
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1}
            ]
        }
    ]

    for dt_data in doctypes:
        name = dt_data["name"]
        if frappe.db.exists("DocType", name):
            print(f"Updating existing DocType: {name}")
            doc = frappe.get_doc("DocType", name)
            doc.update(dt_data)
            doc.save()
        else:
            print(f"Creating DocType: {name}")
            doc = frappe.get_doc(dt_data)
            doc.insert()

    frappe.db.commit()
    print("All DocTypes created and committed successfully!")
