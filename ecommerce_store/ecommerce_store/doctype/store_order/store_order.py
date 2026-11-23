# Copyright (c) 2026, Zain and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class StoreOrder(Document):
    def after_insert(self):
        # Auto-deduct inventory across all channels (Desk UI & Headless APIs)
        if self.order_status != "Cancelled":
            self.deduct_inventory()

    def before_save(self):
        # Auto-detect transition to Cancelled (handles both Desk UI save and cancel_order API)
        if not self.is_new():
            old_status = frappe.db.get_value("Store Order", self.name, "order_status")
            if old_status and old_status != "Cancelled" and self.order_status == "Cancelled":
                self.restore_inventory_and_stats(reason=getattr(self, "_cancellation_reason", None) or "Order status set to Cancelled")

    def deduct_inventory(self):
        """
        Deducts stock from Product or individual Product Variant when an order is created.
        """
        for item in self.items:
            if not item.product or not frappe.db.exists("Product", item.product):
                continue

            prod = frappe.get_doc("Product", item.product)
            if not prod.track_inventory:
                continue

            qty_to_deduct = int(item.quantity or 1)
            deducted_from_variant = False

            # Check if this item matches a product variant
            if prod.has_variants and prod.variants:
                for v in prod.variants:
                    if (item.sku and v.sku == item.sku) or (item.attributes_summary and v.title == item.attributes_summary):
                        v.stock_quantity = max(0, int(v.stock_quantity or 0) - qty_to_deduct)
                        deducted_from_variant = True
                        break

            if not deducted_from_variant:
                prod.stock_quantity = max(0, int(prod.stock_quantity or 0) - qty_to_deduct)

            # Update stock status
            if prod.stock_quantity <= 0 and not prod.continue_selling_out_of_stock:
                prod.is_in_stock = 0

            prod.save(ignore_permissions=True)
            prod.add_comment(
                "Info",
                _("Deducted {0} unit(s) for Order {1}. Remaining stock: {2}").format(
                    qty_to_deduct,
                    f"<a href='/app/store-order/{self.name}'><b>{self.name}</b></a>",
                    prod.stock_quantity
                )
            )

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
        Supports both standalone products and variant stock restorations.
        """
        # 1. Restore product inventory
        for item in self.items:
            if not item.product or not frappe.db.exists("Product", item.product):
                continue

            prod = frappe.get_doc("Product", item.product)
            if not prod.track_inventory:
                continue

            restore_qty = int(item.quantity or 1)
            old_stock = int(prod.stock_quantity or 0)
            restored_to_variant = False

            if prod.has_variants and prod.variants:
                for v in prod.variants:
                    if (item.sku and v.sku == item.sku) or (item.attributes_summary and v.title == item.attributes_summary):
                        v.stock_quantity = int(v.stock_quantity or 0) + restore_qty
                        restored_to_variant = True
                        break

            if not restored_to_variant:
                prod.stock_quantity = old_stock + restore_qty

            prod.is_in_stock = 1
            prod.save(ignore_permissions=True)

            prod.add_comment(
                "Info",
                _("Restored {0} unit(s) due to Order Cancellation {1} ({2}). Stock: {3} &rarr; {4}").format(
                    restore_qty,
                    f"<a href='/app/store-order/{self.name}'><b>{self.name}</b></a>",
                    reason or "Cancelled",
                    old_stock,
                    prod.stock_quantity
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
