import frappe
from frappe import _
import uuid
from frappe.utils import today

def _recalculate_cart(cart):
    subtotal = 0.0
    for item in cart.items:
        item.total = round(float(item.price) * item.quantity, 2)
        subtotal += item.total
        
    discount = 0.0
    if cart.coupon_code and frappe.db.exists("Store Coupon", cart.coupon_code):
        coupon = frappe.get_doc("Store Coupon", cart.coupon_code)
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
                    discount = (subtotal * coupon.discount_value) / 100.0
                    if coupon.max_discount_amount and discount > coupon.max_discount_amount:
                        discount = coupon.max_discount_amount
                else:
                    discount = coupon.discount_value
        else:
            cart.coupon_code = ""
                    
    discount = min(discount, subtotal)
    cart.subtotal = round(subtotal, 2)
    cart.discount_amount = round(discount, 2)
    cart.total = round(max(0.0, subtotal - discount), 2)
    cart.save(ignore_permissions=True)

@frappe.whitelist(allow_guest=True)
def get_cart(cart_id):
    """
    Returns the current cart details by cart_id.
    """
    if not cart_id:
        return {"status": "error", "message": _("Cart ID is required")}
        
    if not frappe.db.exists("Store Cart", cart_id):
        # Create empty cart
        cart = frappe.get_doc({
            "doctype": "Store Cart",
            "cart_id": cart_id,
            "subtotal": 0,
            "discount_amount": 0,
            "total": 0,
            "items": []
        })
        cart.insert(ignore_permissions=True)
    else:
        cart = frappe.get_doc("Store Cart", cart_id)
        
    items = []
    for item in cart.items:
        prod = frappe.db.get_value("Product", item.product, ["primary_image", "route_slug"], as_dict=True) or {}
        items.append({
            "name": item.name,
            "product": item.product,
            "product_name": item.product_name,
            "route_slug": prod.get("route_slug"),
            "image": prod.get("primary_image"),
            "image_url": frappe.utils.get_url(prod.get("primary_image")) if prod.get("primary_image") else None,
            "price": item.price,
            "quantity": item.quantity,
            "total": item.total,
            "attributes_summary": item.attributes_summary
        })
        
    return {
        "status": "success",
        "data": {
            "cart_id": cart.cart_id,
            "subtotal": cart.subtotal,
            "discount_amount": cart.discount_amount,
            "coupon_code": cart.coupon_code,
            "total": cart.total,
            "item_count": sum(i["quantity"] for i in items),
            "items": items
        }
    }

@frappe.whitelist(allow_guest=True)
def add_to_cart(cart_id=None, product_id=None, quantity=1, attributes_summary=None):
    """
    Adds an item to the cart or increments quantity if already present.
    If cart_id is missing, creates a new one.
    """
    try:
        quantity = max(1, int(quantity))
        if not cart_id:
            cart_id = str(uuid.uuid4())
            
        if not frappe.db.exists("Product", product_id):
            return {"status": "error", "message": _("Invalid product")}
            
        prod = frappe.get_doc("Product", product_id)
        if not prod.is_active:
            return {"status": "error", "message": _("This product is currently inactive")}
            
        if prod.track_inventory and prod.stock_quantity < quantity:
            return {"status": "error", "message": _("Insufficient stock available (Only {0} left in stock)").format(prod.stock_quantity)}
            
        if not frappe.db.exists("Store Cart", cart_id):
            cart = frappe.get_doc({
                "doctype": "Store Cart",
                "cart_id": cart_id,
                "items": []
            })
            cart.insert(ignore_permissions=True)
        else:
            cart = frappe.get_doc("Store Cart", cart_id)
            
        # Check if item exists in cart
        matched_item = None
        for item in cart.items:
            if item.product == product_id and (item.attributes_summary or "") == (attributes_summary or ""):
                matched_item = item
                break
                
        if matched_item:
            new_qty = matched_item.quantity + quantity
            if prod.track_inventory and prod.stock_quantity < new_qty:
                return {
                    "status": "error",
                    "message": _("Cannot add {0} more units. Only {1} total units available in stock (You already have {2} in your cart).").format(quantity, prod.stock_quantity, matched_item.quantity)
                }
            matched_item.quantity = new_qty
            matched_item.total = matched_item.price * matched_item.quantity
        else:
            cart.append("items", {
                "product": prod.name,
                "product_name": prod.title,
                "price": prod.price,
                "quantity": quantity,
                "total": prod.price * quantity,
                "attributes_summary": attributes_summary or ""
            })
            
        _recalculate_cart(cart)
        return get_cart(cart_id)
    except Exception as e:
        frappe.log_error("add_to_cart error", str(e))
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def update_cart_item(cart_id, item_name, quantity):
    """
    Updates the quantity of a specific cart item row or removes it if quantity <= 0.
    """
    try:
        quantity = int(quantity)
        if not frappe.db.exists("Store Cart", cart_id):
            return {"status": "error", "message": _("Cart not found")}
            
        cart = frappe.get_doc("Store Cart", cart_id)
        if quantity <= 0:
            cart.items = [i for i in cart.items if i.name != item_name]
        else:
            for item in cart.items:
                if item.name == item_name:
                    prod = frappe.get_doc("Product", item.product)
                    if prod.track_inventory and prod.stock_quantity < quantity:
                        return {
                            "status": "error",
                            "message": _("Only {0} units available in stock").format(prod.stock_quantity)
                        }
                    item.quantity = quantity
                    item.total = item.price * quantity
                    break
                    
        _recalculate_cart(cart)
        return get_cart(cart_id)
    except Exception as e:
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def remove_from_cart(cart_id, item_name):
    """
    Removes a specific line item from the cart.
    """
    return update_cart_item(cart_id, item_name, 0)

@frappe.whitelist(allow_guest=True)
def clear_cart(cart_id):
    """
    Clears all items in the cart.
    """
    try:
        if frappe.db.exists("Store Cart", cart_id):
            cart = frappe.get_doc("Store Cart", cart_id)
            cart.items = []
            cart.coupon_code = ""
            cart.subtotal = 0
            cart.discount_amount = 0
            cart.total = 0
            cart.save(ignore_permissions=True)
        return get_cart(cart_id)
    except Exception as e:
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def apply_coupon(cart_id, coupon_code):
    """
    Applies a valid coupon to the cart.
    """
    try:
        if not frappe.db.exists("Store Cart", cart_id):
            return {"status": "error", "message": _("Cart not found")}
            
        cart = frappe.get_doc("Store Cart", cart_id)
        if not coupon_code:
            cart.coupon_code = ""
            _recalculate_cart(cart)
            return get_cart(cart_id)
            
        if not frappe.db.exists("Store Coupon", coupon_code):
            return {"status": "error", "message": _("Invalid coupon code")}
            
        coupon = frappe.get_doc("Store Coupon", coupon_code)
        if not coupon.is_active:
            return {"status": "error", "message": _("This coupon is no longer active")}
            
        current_date = today()
        if coupon.valid_from and str(coupon.valid_from) > current_date:
            return {"status": "error", "message": _("This coupon is not valid yet")}
        if coupon.valid_upto and str(coupon.valid_upto) < current_date:
            return {"status": "error", "message": _("This coupon has expired")}
            
        if coupon.usage_limit and coupon.times_used >= coupon.usage_limit:
            return {"status": "error", "message": _("Coupon usage limit exceeded")}
            
        if coupon.min_order_amount and cart.subtotal < coupon.min_order_amount:
            return {"status": "error", "message": _("Minimum order amount of {0} required for this coupon").format(coupon.min_order_amount)}
            
        cart.coupon_code = coupon.coupon_code
        _recalculate_cart(cart)
        return get_cart(cart_id)
    except Exception as e:
        return {"status": "error", "message": str(e)}
