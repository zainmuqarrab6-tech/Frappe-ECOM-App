import frappe

def setup_operations():
    print("Setting up Stock Adjustment, Cancellation Restock, and Print Formats...")

    # 1. Create Stock Adjustment Item (Child Table)
    dt_stock_item = {
        "doctype": "DocType",
        "name": "Stock Adjustment Item",
        "module": "Ecommerce Store",
        "custom": 0,
        "istable": 1,
        "fields": [
            {"fieldname": "product", "fieldtype": "Link", "label": "Product", "options": "Product", "reqd": 1, "in_list_view": 1},
            {"fieldname": "product_name", "fieldtype": "Data", "label": "Product Name", "fetch_from": "product.title", "read_only": 1, "in_list_view": 1},
            {"fieldname": "current_stock", "fieldtype": "Int", "label": "Current Stock", "fetch_from": "product.stock_quantity", "read_only": 1, "in_list_view": 1},
            {"fieldname": "action_type", "fieldtype": "Select", "label": "Adjustment Type", "options": "Add Stock (Restock)\nSubtract Stock (Damage/Loss)\nSet Exact Stock", "default": "Add Stock (Restock)", "reqd": 1, "in_list_view": 1},
            {"fieldname": "quantity", "fieldtype": "Int", "label": "Quantity", "default": "1", "reqd": 1, "in_list_view": 1}
        ],
        "permissions": []
    }

    if frappe.db.exists("DocType", "Stock Adjustment Item"):
        doc = frappe.get_doc("DocType", "Stock Adjustment Item")
        doc.update(dt_stock_item)
        doc.save()
    else:
        frappe.get_doc(dt_stock_item).insert()
    print("Stock Adjustment Item created/updated.")

    # 2. Create Stock Adjustment DocType (Submittable)
    dt_stock_adj = {
        "doctype": "DocType",
        "name": "Stock Adjustment",
        "module": "Ecommerce Store",
        "custom": 0,
        "is_submittable": 1,
        "autoname": "naming_series:",
        "fields": [
            {"fieldname": "naming_series", "fieldtype": "Select", "label": "Series", "options": "STK-ADJ-.YYYY.-.#####", "default": "STK-ADJ-.YYYY.-.#####", "hidden": 1},
            {"fieldname": "sec_overview", "fieldtype": "Section Break", "label": "Adjustment Overview"},
            {"fieldname": "adjustment_date", "fieldtype": "Date", "label": "Date", "default": "Today", "reqd": 1, "in_list_view": 1},
            {"fieldname": "reason", "fieldtype": "Select", "label": "Reason for Adjustment", "options": "New Supplier Delivery / Restock\nDamaged Goods\nInventory Count Correction\nCustomer Return Restock\nOther", "default": "New Supplier Delivery / Restock", "reqd": 1, "in_list_view": 1},
            {"fieldname": "col_overview", "fieldtype": "Column Break"},
            {"fieldname": "reference_note", "fieldtype": "Data", "label": "Supplier / Invoice Reference #"},
            {"fieldname": "notes", "fieldtype": "Small Text", "label": "Internal Notes"},
            {"fieldname": "sec_items", "fieldtype": "Section Break", "label": "Adjusted Products"},
            {"fieldname": "items", "fieldtype": "Table", "label": "Products", "options": "Stock Adjustment Item", "reqd": 1}
        ],
        "permissions": [
            {"role": "System Manager", "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 1, "delete": 1}
        ]
    }

    if frappe.db.exists("DocType", "Stock Adjustment"):
        doc = frappe.get_doc("DocType", "Stock Adjustment")
        doc.update(dt_stock_adj)
        doc.save()
    else:
        frappe.get_doc(dt_stock_adj).insert()
    print("Stock Adjustment created/updated.")

    # 3. Create Print Format: Commercial Tax Invoice
    invoice_html = """
<div style="font-family: Arial, sans-serif; color: #1e293b; max-width: 800px; margin: auto; padding: 20px; font-size: 13px;">
    <!-- Header -->
    <table style="width: 100%; border-bottom: 2px solid #0f172a; padding-bottom: 15px; margin-bottom: 20px;">
        <tr>
            <td style="vertical-align: top;">
                <h1 style="margin: 0; font-size: 24px; color: #0f172a; font-weight: bold;">{{ frappe.db.get_single_value('Store Settings', 'store_name') or 'ProStore Ecommerce' }}</h1>
                <p style="margin: 4px 0 0 0; color: #64748b; font-size: 12px;">{{ frappe.db.get_single_value('Store Theme Settings', 'store_tagline') or 'Official E-Commerce Store' }}</p>
                <p style="margin: 2px 0 0 0; color: #64748b; font-size: 12px;">Phone: {{ frappe.db.get_single_value('Store Settings', 'store_phone') or 'Support' }} | Email: {{ frappe.db.get_single_value('Store Settings', 'store_email') or '' }}</p>
            </td>
            <td style="text-align: right; vertical-align: top;">
                <span style="display: inline-block; background: #0284c7; color: #ffffff; padding: 4px 12px; font-weight: bold; border-radius: 4px; font-size: 12px; letter-spacing: 0.5px;">TAX INVOICE</span>
                <h3 style="margin: 8px 0 0 0; font-size: 16px; color: #0f172a;">{{ doc.name }}</h3>
                <p style="margin: 2px 0 0 0; color: #64748b; font-size: 12px;">Date: {{ frappe.utils.format_datetime(doc.order_date, "medium") if doc.order_date else frappe.utils.format_datetime(doc.creation, "medium") }}</p>
            </td>
        </tr>
    </table>

    <!-- Addresses & Order Meta -->
    <table style="width: 100%; margin-bottom: 20px; font-size: 12px;">
        <tr>
            <td style="width: 50%; vertical-align: top; padding-right: 15px;">
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 12px; border-radius: 6px;">
                    <strong style="color: #0f172a; font-size: 13px;">DELIVER TO / CONSIGNEE:</strong>
                    <div style="font-weight: bold; font-size: 14px; margin-top: 6px; color: #0f172a;">{{ doc.customer_name }}</div>
                    <div style="color: #334155; margin-top: 2px;">{{ doc.shipping_address }}</div>
                    <div style="color: #334155;">{{ doc.shipping_city }}{% if doc.shipping_postal_code %}, {{ doc.shipping_postal_code }}{% endif %}</div>
                    <div style="color: #334155; font-weight: 500;">Phone: <strong>{{ doc.customer_phone }}</strong></div>
                    <div style="color: #64748b;">Email: {{ doc.customer_email }}</div>
                </div>
            </td>
            <td style="width: 50%; vertical-align: top; padding-left: 15px;">
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 12px; border-radius: 6px;">
                    <strong style="color: #0f172a; font-size: 13px;">PAYMENT & ORDER STATUS:</strong>
                    <div style="margin-top: 6px;">
                        <span>Payment Method:</span>
                        <strong style="color: #0f172a;">{{ doc.payment_method }}</strong>
                    </div>
                    <div style="margin-top: 3px;">
                        <span>Payment Status:</span>
                        <strong style="color: {% if doc.payment_status == 'Paid' %}#15803d{% else %}#b45309{% endif %};">{{ doc.payment_status }}</strong>
                    </div>
                    <div style="margin-top: 3px;">
                        <span>Order Status:</span>
                        <strong style="color: #0284c7;">{{ doc.order_status }}</strong>
                    </div>
                    {% if doc.tracking_courier or doc.tracking_number %}
                    <div style="margin-top: 3px;">
                        <span>Courier / Tracking:</span>
                        <strong>{{ doc.tracking_courier or 'Courier' }} - {{ doc.tracking_number or '' }}</strong>
                    </div>
                    {% endif %}
                </div>
            </td>
        </tr>
    </table>

    <!-- Line Items Table -->
    <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 12px;">
        <thead>
            <tr style="background: #0f172a; color: #ffffff;">
                <th style="padding: 10px; text-align: left; border: 1px solid #0f172a;">#</th>
                <th style="padding: 10px; text-align: left; border: 1px solid #0f172a;">Item Description</th>
                <th style="padding: 10px; text-align: left; border: 1px solid #0f172a;">SKU / Options</th>
                <th style="padding: 10px; text-align: right; border: 1px solid #0f172a;">Price</th>
                <th style="padding: 10px; text-align: center; border: 1px solid #0f172a;">Qty</th>
                <th style="padding: 10px; text-align: right; border: 1px solid #0f172a;">Total</th>
            </tr>
        </thead>
        <tbody>
            {% for item in doc.items %}
            <tr style="border-bottom: 1px solid #e2e8f0; {% if loop.index % 2 == 0 %}background: #f8fafc;{% endif %}">
                <td style="padding: 10px; border: 1px solid #e2e8f0;">{{ loop.index }}</td>
                <td style="padding: 10px; border: 1px solid #e2e8f0; font-weight: bold; color: #0f172a;">{{ item.product_name }}</td>
                <td style="padding: 10px; border: 1px solid #e2e8f0; color: #64748b;">{{ item.sku or '-' }}{% if item.attributes_summary %} ({{ item.attributes_summary }}){% endif %}</td>
                <td style="padding: 10px; border: 1px solid #e2e8f0; text-align: right;">Rs. {{ "{:,.2f}".format(item.price) }}</td>
                <td style="padding: 10px; border: 1px solid #e2e8f0; text-align: center; font-weight: bold;">{{ item.quantity }}</td>
                <td style="padding: 10px; border: 1px solid #e2e8f0; text-align: right; font-weight: bold;">Rs. {{ "{:,.2f}".format(item.total) }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    <!-- Totals Summary -->
    <table style="width: 100%; margin-bottom: 25px;">
        <tr>
            <td style="width: 60%; vertical-align: top;">
                {% if doc.customer_notes %}
                <div style="background: #fffbeb; border: 1px solid #fef3c7; padding: 10px; border-radius: 6px; font-size: 11.5px;">
                    <strong>Customer Order Note:</strong>
                    <p style="margin: 3px 0 0 0; color: #92400e;">{{ doc.customer_notes }}</p>
                </div>
                {% endif %}
            </td>
            <td style="width: 40%; vertical-align: top;">
                <table style="width: 100%; font-size: 12.5px; border-collapse: collapse;">
                    <tr>
                        <td style="padding: 4px 8px; color: #64748b;">Subtotal:</td>
                        <td style="padding: 4px 8px; text-align: right; font-weight: 500;">Rs. {{ "{:,.2f}".format(doc.subtotal) }}</td>
                    </tr>
                    {% if doc.discount_amount > 0 %}
                    <tr>
                        <td style="padding: 4px 8px; color: #16a34a;">Discount ({{ doc.coupon_code or 'Promo' }}):</td>
                        <td style="padding: 4px 8px; text-align: right; color: #16a34a; font-weight: bold;">- Rs. {{ "{:,.2f}".format(doc.discount_amount) }}</td>
                    </tr>
                    {% endif %}
                    <tr>
                        <td style="padding: 4px 8px; color: #64748b;">Shipping Fee:</td>
                        <td style="padding: 4px 8px; text-align: right;">{% if doc.shipping_fee > 0 %}Rs. {{ "{:,.2f}".format(doc.shipping_fee) }}{% else %}<span style="color:#16a34a; font-weight:bold;">FREE</span>{% endif %}</td>
                    </tr>
                    {% if doc.tax_amount > 0 %}
                    <tr>
                        <td style="padding: 4px 8px; color: #64748b;">Sales Tax:</td>
                        <td style="padding: 4px 8px; text-align: right;">Rs. {{ "{:,.2f}".format(doc.tax_amount) }}</td>
                    </tr>
                    {% endif %}
                    <tr style="border-top: 2px solid #0f172a; font-size: 15px;">
                        <td style="padding: 8px 8px; font-weight: bold; color: #0f172a;">Grand Total:</td>
                        <td style="padding: 8px 8px; text-align: right; font-weight: bold; color: #0284c7;">Rs. {{ "{:,.2f}".format(doc.grand_total) }}</td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>

    <!-- Invoice Footer -->
    <div style="border-top: 1px solid #e2e8f0; padding-top: 15px; text-align: center; font-size: 11px; color: #64748b;">
        <p style="margin: 0; font-weight: bold; color: #0f172a;">Thank you for shopping with {{ frappe.db.get_single_value('Store Settings', 'store_name') or 'us' }}!</p>
        <p style="margin: 4px 0 0 0;">For returns, replacements, or delivery inquiries, contact our WhatsApp Support at <strong>{{ frappe.db.get_single_value('Store Theme Settings', 'social_whatsapp') or '+923001234567' }}</strong>.</p>
    </div>
</div>
"""

    if frappe.db.exists("Print Format", "Commercial Tax Invoice"):
        pf = frappe.get_doc("Print Format", "Commercial Tax Invoice")
        pf.html = invoice_html
        pf.save(ignore_permissions=True)
    else:
        frappe.get_doc({
            "doctype": "Print Format",
            "name": "Commercial Tax Invoice",
            "doc_type": "Store Order",
            "module": "Ecommerce Store",
            "standard": "Yes",
            "custom_format": 1,
            "print_format_type": "Jinja",
            "html": invoice_html
        }).insert(ignore_permissions=True)
    print("Print Format 'Commercial Tax Invoice' created.")

    # 4. Create Print Format: Thermal Courier Shipping Label (4x6 format)
    label_html = """
<div style="font-family: Arial, sans-serif; width: 380px; max-width: 100%; border: 3px solid #000000; padding: 12px; margin: auto; background: #ffffff; color: #000000;">
    <!-- Courier Header -->
    <table style="width: 100%; border-bottom: 2px solid #000000; padding-bottom: 6px; margin-bottom: 8px;">
        <tr>
            <td style="font-size: 18px; font-weight: 900; letter-spacing: 1px;">PARCEL SHIPPING LABEL</td>
            <td style="text-align: right; font-size: 13px; font-weight: bold;">{{ doc.tracking_courier or 'EXPRESS' }}</td>
        </tr>
    </table>

    <!-- Tracking & Order Reference Barcode Area -->
    <div style="border: 2px dashed #000000; padding: 6px; text-align: center; margin-bottom: 10px; background: #fafafa;">
        <div style="font-size: 11px; font-weight: bold; text-transform: uppercase;">Tracking / Order Airway Bill</div>
        <div style="font-family: monospace; font-size: 18px; font-weight: 900; letter-spacing: 2px; margin: 3px 0;">* {{ doc.tracking_number or doc.name }} *</div>
        <div style="font-size: 10px; color: #333;">Order Ref: {{ doc.name }} | Date: {{ frappe.utils.format_date(doc.order_date or doc.creation) }}</div>
    </div>

    <!-- Receiver / Consignee Details (Most prominent) -->
    <div style="border: 2px solid #000000; padding: 10px; margin-bottom: 10px; border-radius: 4px;">
        <div style="font-size: 11px; font-weight: 900; text-transform: uppercase; background: #000000; color: #ffffff; display: inline-block; padding: 2px 6px;">DELIVER TO / SHIP TO:</div>
        <div style="font-size: 17px; font-weight: 900; margin-top: 6px; text-transform: uppercase;">{{ doc.customer_name }}</div>
        <div style="font-size: 16px; font-weight: 900; margin: 4px 0; color: #000000;">TEL: {{ doc.customer_phone }}</div>
        <div style="font-size: 13px; line-height: 1.35; margin-top: 4px;">
            {{ doc.shipping_address }}<br/>
            <strong>CITY: {{ doc.shipping_city|upper }}</strong>{% if doc.shipping_postal_code %}, {{ doc.shipping_postal_code }}{% endif %}<br/>
            {{ doc.shipping_country|upper }}
        </div>
    </div>

    <!-- COD Amount Box (Giant Bold Box for Courier Driver) -->
    <div style="border: 3px solid #000000; padding: 8px; text-align: center; margin-bottom: 10px; background: #000000; color: #ffffff;">
        <div style="font-size: 12px; font-weight: 900; letter-spacing: 0.5px;">CASH ON DELIVERY (COD) TO COLLECT:</div>
        <div style="font-size: 26px; font-weight: 900; margin-top: 2px;">
            {% if doc.payment_status == 'Paid' %}
                PAID - DO NOT COLLECT COD
            {% else %}
                Rs. {{ "{:,.0f}".format(doc.grand_total) }}
            {% endif %}
        </div>
    </div>

    <!-- Shipper / Sender Return Info -->
    <table style="width: 100%; border-top: 1px solid #000000; padding-top: 6px; font-size: 10.5px; line-height: 1.3;">
        <tr>
            <td style="vertical-align: top;">
                <strong>RETURN IF UNDELIVERED TO:</strong><br/>
                {{ frappe.db.get_single_value('Store Settings', 'store_name') or 'ProStore' }} Fulfillment Center<br/>
                Helpline: {{ frappe.db.get_single_value('Store Settings', 'store_phone') or '' }}<br/>
                Pakistan
            </td>
            <td style="text-align: right; vertical-align: bottom;">
                <strong>PIECES: {{ doc.items|length }}</strong><br/>
                <span style="font-size: 9px;">Standard Delivery</span>
            </td>
        </tr>
    </table>
</div>
"""

    if frappe.db.exists("Print Format", "Thermal Courier Shipping Label"):
        pf = frappe.get_doc("Print Format", "Thermal Courier Shipping Label")
        pf.html = label_html
        pf.save(ignore_permissions=True)
    else:
        frappe.get_doc({
            "doctype": "Print Format",
            "name": "Thermal Courier Shipping Label",
            "doc_type": "Store Order",
            "module": "Ecommerce Store",
            "standard": "Yes",
            "custom_format": 1,
            "print_format_type": "Jinja",
            "html": label_html
        }).insert(ignore_permissions=True)
    print("Print Format 'Thermal Courier Shipping Label' created.")

    frappe.db.commit()
    print("Setup Operations completed successfully!")

if __name__ == "__main__":
    setup_operations()

