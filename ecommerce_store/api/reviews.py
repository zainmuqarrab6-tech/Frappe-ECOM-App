import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def get_product_reviews(product_id):
    """
    Returns approved customer reviews, average star rating, and breakdown for a product.
    """
    try:
        if not product_id:
            return {"status": "error", "message": _("Product ID is required")}

        # Check if product exists by id or slug
        real_prod_id = product_id
        if not frappe.db.exists("Product", product_id):
            real_prod_id = frappe.db.get_value("Product", {"route_slug": product_id}, "name")

        if not real_prod_id:
            return {"status": "error", "message": _("Product not found")}

        reviews = frappe.get_all(
            "Product Review",
            filters={"product": real_prod_id, "status": "Approved"},
            fields=["name", "customer_name", "rating", "title", "review_text", "is_verified_buyer", "creation"],
            order_by="creation desc"
        )

        total_reviews = len(reviews)
        avg_rating = 0.0
        rating_breakdown = {"5": 0, "4": 0, "3": 0, "2": 0, "1": 0}

        if total_reviews > 0:
            total_stars = 0
            for r in reviews:
                r_val = str(r["rating"])
                rating_breakdown[r_val] = rating_breakdown.get(r_val, 0) + 1
                total_stars += int(r["rating"])
            avg_rating = round(total_stars / float(total_reviews), 1)

        return {
            "status": "success",
            "data": {
                "product_id": real_prod_id,
                "average_rating": avg_rating,
                "total_reviews": total_reviews,
                "breakdown": rating_breakdown,
                "reviews": reviews
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def submit_review(product_id, customer_name, customer_email, rating, review_text, title=None):
    """
    Submits a new customer review for a product.
    """
    try:
        customer_name = (customer_name or "").strip()
        customer_email = (customer_email or "").strip().lower()
        review_text = (review_text or "").strip()

        if not product_id or not customer_name or not customer_email or not review_text:
            return {"status": "error", "message": _("Product, name, email and review text are required")}

        real_prod_id = product_id
        if not frappe.db.exists("Product", product_id):
            real_prod_id = frappe.db.get_value("Product", {"route_slug": product_id}, "name")

        if not real_prod_id:
            return {"status": "error", "message": _("Product not found")}

        rating = str(max(1, min(5, int(rating))))

        # Check if customer has verified purchase
        is_verified = 0
        if frappe.db.exists("Store Order", {"customer_email": customer_email, "order_status": ["in", ["Confirmed", "Shipped", "Delivered"]]}):
            is_verified = 1

        review = frappe.get_doc({
            "doctype": "Product Review",
            "product": real_prod_id,
            "customer_name": customer_name,
            "customer_email": customer_email,
            "rating": rating,
            "title": title or "",
            "review_text": review_text,
            "is_verified_buyer": is_verified,
            "status": "Approved"  # Auto-approve (or set to Pending if strict moderation desired)
        })
        review.insert(ignore_permissions=True)
        frappe.db.commit()

        return {
            "status": "success",
            "message": _("Thank you! Your review has been submitted."),
            "review_id": review.name
        }
    except Exception as e:
        frappe.log_error("submit_review error", str(e))
        return {"status": "error", "message": str(e)}
