import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def get_products(category=None, brand=None, search=None, sort_by="recent", min_price=None, max_price=None, is_featured=None, page=1, limit=20):
    """
    Returns filtered and paginated list of active products for frontend store.
    """
    try:
        page = int(page)
        limit = min(int(limit), 100)
        start = (page - 1) * limit
        
        filters = {"is_active": 1}
        
        if is_featured in [1, "1", True, "true"]:
            filters["is_featured"] = 1
        if category:
            filters["category"] = category
        if brand:
            filters["brand"] = brand
        if min_price:
            filters["price"] = [">=", float(min_price)]
        if max_price:
            if "price" in filters:
                filters["price"] = ["between", [float(min_price), float(max_price)]]
            else:
                filters["price"] = ["<=", float(max_price)]
                
        or_filters = []
        if search:
            search_pattern = f"%{search}%"
            or_filters = [
                ["title", "like", search_pattern],
                ["sku", "like", search_pattern],
                ["short_description", "like", search_pattern]
            ]
            
        order_by_map = {
            "recent": "creation desc",
            "price_low_to_high": "price asc",
            "price_high_to_low": "price desc",
            "title_asc": "title asc",
            "title_desc": "title desc"
        }
        order_by = order_by_map.get(sort_by, "creation desc")
        
        fields = [
            "name", "title", "route_slug", "sku", "category", "brand", 
            "price", "compare_at_price", "is_in_stock", "stock_quantity", 
            "primary_image", "short_description", "is_featured"
        ]
        
        products = frappe.get_all(
            "Product",
            filters=filters,
            or_filters=or_filters if or_filters else None,
            fields=fields,
            order_by=order_by,
            start=start,
            page_length=limit
        )
        
        if or_filters:
            total_count = len(frappe.get_all(
                "Product",
                filters=filters,
                or_filters=or_filters,
                pluck="name"
            ))
        else:
            total_count = frappe.db.count("Product", filters=filters)
        
        # Attach full image URLs if needed
        for p in products:
            if p.get("primary_image"):
                p["primary_image_url"] = frappe.utils.get_url(p["primary_image"])
            else:
                p["primary_image_url"] = None
                
        return {
            "status": "success",
            "data": products,
            "pagination": {
                "page": page,
                "limit": limit,
                "total_items": total_count,
                "total_pages": (total_count + limit - 1) // limit if total_count > 0 else 1
            }
        }
    except Exception as e:
        frappe.log_error("get_products error", str(e))
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def get_product_detail(slug_or_id):
    """
    Returns full product details, gallery images, and attributes by slug or name/ID.
    """
    try:
        product_name = None
        if frappe.db.exists("Product", slug_or_id):
            product_name = slug_or_id
        else:
            product_name = frappe.db.get_value("Product", {"route_slug": slug_or_id, "is_active": 1}, "name")
            
        if not product_name:
            return {"status": "error", "message": _("Product not found"), "code": 404}
            
        doc = frappe.get_doc("Product", product_name)
        
        images = []
        if doc.primary_image:
            images.append({
                "image": doc.primary_image,
                "url": frappe.utils.get_url(doc.primary_image),
                "alt_text": doc.title,
                "is_primary": 1
            })
            
        for img in doc.images:
            images.append({
                "image": img.image,
                "url": frappe.utils.get_url(img.image),
                "alt_text": img.alt_text or doc.title,
                "is_primary": img.is_primary
            })
            
        attributes = []
        for attr in doc.attributes:
            attributes.append({
                "attribute_name": attr.attribute_name,
                "attribute_value": attr.attribute_value
            })
            
        product_data = {
            "id": doc.name,
            "title": doc.title,
            "route_slug": doc.route_slug,
            "sku": doc.sku,
            "barcode": doc.barcode,
            "category": doc.category,
            "brand": doc.brand,
            "price": doc.price,
            "compare_at_price": doc.compare_at_price,
            "is_in_stock": doc.is_in_stock,
            "stock_quantity": doc.stock_quantity if doc.track_inventory else 999,
            "primary_image": doc.primary_image,
            "primary_image_url": frappe.utils.get_url(doc.primary_image) if doc.primary_image else None,
            "images": images,
            "attributes": attributes,
            "short_description": doc.short_description,
            "description": doc.description,
            "is_featured": doc.is_featured
        }
        
        return {"status": "success", "data": product_data}
    except Exception as e:
        frappe.log_error("get_product_detail error", str(e))
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def get_categories():
    """
    Returns list of all active categories.
    """
    try:
        categories = frappe.get_all(
            "Product Category",
            filters={"is_active": 1},
            fields=["name", "category_name", "route_slug", "category_image", "parent_category", "description"],
            order_by="sort_order asc, category_name asc"
        )
        for cat in categories:
            if cat.get("category_image"):
                cat["category_image_url"] = frappe.utils.get_url(cat["category_image"])
            else:
                cat["category_image_url"] = None
        return {"status": "success", "data": categories}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def get_brands():
    """
    Returns list of all active brands.
    """
    try:
        brands = frappe.get_all(
            "Product Brand",
            filters={"is_active": 1},
            fields=["name", "brand_name", "route_slug", "logo", "description"],
            order_by="brand_name asc"
        )
        for b in brands:
            if b.get("logo"):
                b["logo_url"] = frappe.utils.get_url(b["logo"])
            else:
                b["logo_url"] = None
        return {"status": "success", "data": brands}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def get_featured_products(limit=8):
    """
    Returns featured products for homepage sliders/grids.
    """
    return get_products(page=1, limit=limit, is_featured=1, sort_by="recent")
