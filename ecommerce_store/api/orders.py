import frappe
from frappe import _
import json
from frappe.utils import today

@frappe.whitelist(allow_guest=True)
def create_order(
    customer_name,
    customer_email,
    customer_phone,
    shipping_address,
    shipping_city,
    shipping_postal_code=None,
    shipping_country="Pakistan",
    payment_method="Cash on Delivery",
    payment_id=None,
    customer_notes=None,
    cart_id=None,
    items=None
):
    """
    Creates an order from cart_id or direct JSON items array.
    Deducts stock, links/creates customer, applies shipping/taxes, and returns order doc.
    """
    try:
        customer_name = (customer_name or "").strip()
        customer_email = (customer_email or "").strip().lower()
        customer_phone = (customer_phone or "").strip()
        shipping_address = (shipping_address or "").strip()
        shipping_city = (shipping_city or "").strip()

        if not customer_name or not customer_email or not customer_phone:
            return {"status": "error", "message": _("Customer name, email and phone are required")}
        if not shipping_address or not shipping_city:
            return {"status": "error", "message": _("Shipping address and city are required")}

        # 1. Get Store Settings & Verify Policies
        settings = frappe.get_single("Store Settings")
        
        # Check guest checkout policy
        if not settings.allow_guest_checkout and frappe.session.user == "Guest":
            return {"status": "error", "message": _("Guest checkout is disabled. Please log in or create an account to proceed.")}

        # Check Payment Method validity
        if payment_method == "Cash on Delivery" and not settings.allow_cod:
            return {"status": "error", "message": _("Cash on Delivery is currently disabled by store policy.")}

        default_shipping_fee = float(settings.default_shipping_fee or 0)
        free_shipping_threshold = float(settings.free_shipping_threshold or 0)
        tax_percentage = float(settings.tax_percentage or 0)

        # 2. Resolve Items
        order_items = []
        coupon_code = None
        cart = None
        
        if cart_id and frappe.db.exists("Store Cart", cart_id):
            cart = frappe.get_doc("Store Cart", cart_id)
            coupon_code = cart.coupon_code
            for it in cart.items:
                order_items.append({
                    "product": it.product,
                    "quantity": it.quantity,
                    "attributes_summary": it.attributes_summary
                })
        elif items:
            if isinstance(items, str):
                items = json.loads(items)
            order_items = items

        if not order_items:
            return {"status": "error", "message": _("Cannot create an empty order")}

        # 3. Process each line item & check stock
        subtotal = 0.0
        final_items = []
        for it in order_items:
            prod_id = it.get("product")
            qty = max(1, int(it.get("quantity", 1)))
            
            if not frappe.db.exists("Product", prod_id):
                return {"status": "error", "message": _("Product {0} does not exist").format(prod_id)}
                
            prod = frappe.get_doc("Product", prod_id)
            if not prod.is_active:
                return {"status": "error", "message": _("Product '{0}' is not currently available").format(prod.title)}
                
            if prod.track_inventory and prod.stock_quantity < qty:
                return {"status": "error", "message": _("Product '{0}' has insufficient stock (Only {1} left in stock)").format(prod.title, prod.stock_quantity)}

            line_total = round(float(prod.price) * qty, 2)
            subtotal += line_total
            
            final_items.append({
                "product": prod.name,
                "product_name": prod.title,
                "sku": prod.sku,
                "price": prod.price,
                "quantity": qty,
                "total": line_total,
                "attributes_summary": it.get("attributes_summary") or ""
            })

        subtotal = round(subtotal, 2)

        # 4. Calculate Discounts & Verify Coupon
        discount_amount = 0.0
        if coupon_code and frappe.db.exists("Store Coupon", coupon_code):
            coupon = frappe.get_doc("Store Coupon", coupon_code)
            curr_date = today()
            is_valid = coupon.is_active
            if coupon.valid_from and str(coupon.valid_from) > curr_date:
                is_valid = False
            if coupon.valid_upto and str(coupon.valid_upto) < curr_date:
                is_valid = False
            if coupon.usage_limit and coupon.times_used >= coupon.usage_limit:
                is_valid = False

            if is_valid:
                if not coupon.min_order_amount or subtotal >= coupon.min_order_amount:
                    if coupon.discount_type == "Percentage":
                        discount_amount = (subtotal * coupon.discount_value) / 100.0
                        if coupon.max_discount_amount and discount_amount > coupon.max_discount_amount:
                            discount_amount = coupon.max_discount_amount
                    else:
                        discount_amount = coupon.discount_value
            else:
                coupon_code = None

        discount_amount = round(min(discount_amount, subtotal), 2)
        discounted_subtotal = round(subtotal - discount_amount, 2)

        # 5. Calculate Shipping & Taxes
        shipping_fee = default_shipping_fee
        if free_shipping_threshold > 0 and discounted_subtotal >= free_shipping_threshold:
            shipping_fee = 0.0
        shipping_fee = round(shipping_fee, 2)

        tax_amount = round((discounted_subtotal * tax_percentage) / 100.0, 2) if tax_percentage > 0 else 0.0
        grand_total = round(discounted_subtotal + shipping_fee + tax_amount, 2)

        # 6. Resolve Customer Profile
        customer_id = None
        if frappe.db.exists("Store Customer", {"email": customer_email}):
            customer_id = frappe.db.get_value("Store Customer", {"email": customer_email}, "name")
            cust = frappe.get_doc("Store Customer", customer_id)
            cust.total_orders_placed = (cust.total_orders_placed or 0) + 1
            cust.total_spent = round((cust.total_spent or 0) + grand_total, 2)
            cust.save(ignore_permissions=True)
        else:
            cust = frappe.get_doc({
                "doctype": "Store Customer",
                "customer_name": customer_name,
                "email": customer_email,
                "phone": customer_phone,
                "total_orders_placed": 1,
                "total_spent": grand_total
            })
            cust.insert(ignore_permissions=True)
            customer_id = cust.name

        # 7. Create Store Order Doc
        order = frappe.get_doc({
            "doctype": "Store Order",
            "naming_series": "ORD-.YYYY.-.#####",
            "order_status": "Pending",
            "payment_status": "Unpaid" if payment_method == "Cash on Delivery" else "Paid" if payment_id else "Unpaid",
            "payment_method": payment_method,
            "payment_id": payment_id or "",
            "customer": customer_id,
            "customer_name": customer_name,
            "customer_email": customer_email,
            "customer_phone": customer_phone,
            "shipping_address": shipping_address,
            "shipping_city": shipping_city,
            "shipping_postal_code": shipping_postal_code or "",
            "shipping_country": shipping_country,
            "subtotal": subtotal,
            "discount_amount": discount_amount,
            "coupon_code": coupon_code or "",
            "shipping_fee": shipping_fee,
            "tax_amount": tax_amount,
            "grand_total": grand_total,
            "customer_notes": customer_notes or "",
            "items": final_items
        })
        order.insert(ignore_permissions=True)

        # 8. Deduct Product Inventory
        for it in final_items:
            prod = frappe.get_doc("Product", it["product"])
            if prod.track_inventory:
                prod.stock_quantity = max(0, prod.stock_quantity - it["quantity"])
                if prod.stock_quantity <= 0:
                    prod.is_in_stock = 0
                prod.save(ignore_permissions=True)

        # 9. Update Coupon Usage Count
        if coupon_code and frappe.db.exists("Store Coupon", coupon_code):
            c_doc = frappe.get_doc("Store Coupon", coupon_code)
            c_doc.times_used = (c_doc.times_used or 0) + 1
            c_doc.save(ignore_permissions=True)

        # 10. Clear Cart if order created from cart
        if cart:
            cart.items = []
            cart.coupon_code = ""
            cart.subtotal = 0
            cart.discount_amount = 0
            cart.total = 0
            cart.save(ignore_permissions=True)

        frappe.db.commit()

        return {
            "status": "success",
            "message": _("Order placed successfully"),
            "data": {
                "order_id": order.name,
                "order_status": order.order_status,
                "payment_status": order.payment_status,
                "payment_method": order.payment_method,
                "grand_total": order.grand_total,
                "currency": settings.currency or "PKR",
                "currency_symbol": settings.currency_symbol or "Rs."
            }
        }
    except Exception as e:
        frappe.log_error("create_order error", str(e))
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def get_order_detail(order_id):
    """
    Returns order details including items, statuses and totals.
    """
    try:
        if not frappe.db.exists("Store Order", order_id):
            return {"status": "error", "message": _("Order not found")}
            
        order = frappe.get_doc("Store Order", order_id)
        items = []
        for it in order.items:
            items.append({
                "product": it.product,
                "product_name": it.product_name,
                "sku": it.sku,
                "price": it.price,
                "quantity": it.quantity,
                "total": it.total,
                "attributes_summary": it.attributes_summary
            })
            
        settings = frappe.get_single("Store Settings")
        
        return {
            "status": "success",
            "data": {
                "order_id": order.name,
                "order_date": order.order_date,
                "order_status": order.order_status,
                "payment_status": order.payment_status,
                "payment_method": order.payment_method,
                "payment_id": order.payment_id,
                "customer_name": order.customer_name,
                "customer_email": order.customer_email,
                "customer_phone": order.customer_phone,
                "shipping_address": order.shipping_address,
                "shipping_city": order.shipping_city,
                "shipping_postal_code": order.shipping_postal_code,
                "shipping_country": order.shipping_country,
                "subtotal": order.subtotal,
                "shipping_fee": order.shipping_fee,
                "tax_amount": order.tax_amount,
                "discount_amount": order.discount_amount,
                "coupon_code": order.coupon_code,
                "grand_total": order.grand_total,
                "tracking_courier": order.tracking_courier,
                "tracking_number": order.tracking_number,
                "currency": settings.currency or "PKR",
                "currency_symbol": settings.currency_symbol or "Rs.",
                "items": items
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def get_customer_orders(email):
    """
    Returns list of past orders for a customer by email.
    """
    try:
        if not email:
            return {"status": "error", "message": _("Email is required")}
            
        orders = frappe.get_all(
            "Store Order",
            filters={"customer_email": email.strip().lower()},
            fields=["name", "order_date", "order_status", "payment_status", "payment_method", "grand_total"],
            order_by="creation desc"
        )
        return {"status": "success", "data": orders}
    except Exception as e:
        return {"status": "error", "message": str(e)}
