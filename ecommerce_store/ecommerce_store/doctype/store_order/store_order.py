# Copyright (c) 2026, Zain and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class StoreOrder(Document):
    def before_save(self):
        # Auto-detect transition to Cancelled (handles both Desk UI save and cancel_order API)
        if not self.is_new():
            old_status = frappe.db.get_value("Store Order", self.name, "order_status")
            if old_status and old_status != "Cancelled" and self.order_status == "Cancelled":
                self.restore_inventory_and_stats(reason=getattr(self, "_cancellation_reason", None) or "Order status set to Cancelled")

    @frappe.whitelist()
    def cancel_order(self, reason=None):
        """
        Manually trigger cancellation of an order:
        Restores stock quantities, decrements coupon usage, and adjusts customer stats.
        """
        if self.order_status == "Cancelled":
            frappe.throw(_("This order is already cancelled."))

        self._cancellation_reason = reason or "Admin cancelled order"
        self.order_status = "Cancelled"
        if reason:
            self.customer_notes = ((self.customer_notes or "") + f"\n[Cancellation Reason: {reason}]").strip()

        # self.save() will invoke before_save, which calls restore_inventory_and_stats once
        self.save(ignore_permissions=True)
        frappe.msgprint(_("Order {0} has been cancelled. Product inventory has been automatically restored.").format(self.name))
        return {"status": "success", "order_status": "Cancelled"}

    def restore_inventory_and_stats(self, reason=None):
        """
        Reverts stock deductions, adjusts customer lifetime stats, and decrements coupon usage count.
        """
        # 1. Restore product inventory
        for item in self.items:
            if not item.product:
                continue
            if not frappe.db.exists("Product", item.product):
                continue

            prod = frappe.get_doc("Product", item.product)
            if prod.track_inventory:
                old_stock = int(prod.stock_quantity or 0)
                restore_qty = int(item.quantity or 1)
                new_stock = old_stock + restore_qty

                prod.stock_quantity = new_stock
                prod.is_in_stock = 1
                prod.save(ignore_permissions=True)

                prod.add_comment(
                    "Info",
                    _("Restored {0} unit(s) due to Order Cancellation {1} ({2}). Stock: {3} &rarr; {4}").format(
                        restore_qty,
                        f"<a href='/app/store-order/{self.name}'><b>{self.name}</b></a>",
                        reason or "Cancelled",
                        old_stock,
                        new_stock
                    )
                )

        # 2. Adjust Customer Lifetime Stats
        customer_doc = None
        if self.customer and frappe.db.exists("Store Customer", self.customer):
            customer_doc = frappe.get_doc("Store Customer", self.customer)
        elif self.customer_email:
            cust_name = frappe.db.get_value("Store Customer", {"email": self.customer_email.lower().strip()})
            if cust_name:
                customer_doc = frappe.get_doc("Store Customer", cust_name)

        if customer_doc:
            customer_doc.total_orders_placed = max(0, int(customer_doc.total_orders_placed or 1) - 1)
            customer_doc.total_spent = max(0.0, float(customer_doc.total_spent or 0) - float(self.grand_total or 0))
            customer_doc.save(ignore_permissions=True)

        # 3. Revert coupon usage count
        if self.coupon_code and frappe.db.exists("Store Coupon", self.coupon_code):
            c_doc = frappe.get_doc("Store Coupon", self.coupon_code)
            c_doc.times_used = max(0, int(c_doc.times_used or 1) - 1)
            c_doc.save(ignore_permissions=True)

        # 4. Add audit comment on the order itself
        self.add_comment(
            "Info",
            _("Order cancelled. Inventory restored for all line items. Reason: {0}").format(reason or "N/A")
        )
