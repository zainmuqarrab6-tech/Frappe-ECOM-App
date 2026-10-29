# Copyright (c) 2026, Zain and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class StockAdjustment(Document):
    def validate(self):
        if not self.items:
            frappe.throw(_("Please add at least one product to adjust."))

        for item in self.items:
            if not item.product:
                frappe.throw(_("Row #{0}: Product is required").format(item.idx))
            if item.quantity is None or item.quantity < 0:
                frappe.throw(_("Row #{0}: Quantity cannot be negative").format(item.idx))
            if item.action_type != "Set Exact Stock" and item.quantity == 0:
                frappe.throw(_("Row #{0}: Quantity must be greater than zero for '{1}'").format(item.idx, item.action_type))

            current_prod_stock = frappe.db.get_value("Product", item.product, "stock_quantity") or 0
            item.current_stock = current_prod_stock

            if item.action_type == "Subtract Stock (Damage/Loss)":
                if current_prod_stock < item.quantity:
                    frappe.throw(
                        _("Row #{0}: Cannot subtract {1} from '{2}'. Current available stock is only {3}.").format(
                            item.idx, item.quantity, item.product_name or item.product, current_prod_stock
                        )
                    )

    def on_submit(self):
        for item in self.items:
            prod = frappe.get_doc("Product", item.product)
            old_stock = int(prod.stock_quantity or 0)

            # Record exact current stock in child table for audit
            item.db_set("current_stock", old_stock)

            if item.action_type == "Add Stock (Restock)":
                new_stock = old_stock + int(item.quantity)
            elif item.action_type == "Subtract Stock (Damage/Loss)":
                new_stock = max(0, old_stock - int(item.quantity))
            elif item.action_type == "Set Exact Stock":
                new_stock = int(item.quantity)
            else:
                new_stock = old_stock

            prod.stock_quantity = new_stock
            prod.is_in_stock = 1 if new_stock > 0 else 0
            prod.save(ignore_permissions=True)

            # Audit comment on Product document
            prod.add_comment(
                "Info",
                _("Stock adjusted by Stock Adjustment {0} [{1}]: {2} &rarr; {3} (Reason: {4})").format(
                    f"<a href='/app/stock-adjustment/{self.name}'><b>{self.name}</b></a>",
                    item.action_type,
                    old_stock,
                    new_stock,
                    self.reason
                )
            )

    def on_cancel(self):
        for item in self.items:
            prod = frappe.get_doc("Product", item.product)
            old_stock = int(prod.stock_quantity or 0)

            if item.action_type == "Add Stock (Restock)":
                new_stock = max(0, old_stock - int(item.quantity))
            elif item.action_type == "Subtract Stock (Damage/Loss)":
                new_stock = old_stock + int(item.quantity)
            elif item.action_type == "Set Exact Stock":
                new_stock = int(item.current_stock or 0)
            else:
                new_stock = old_stock

            prod.stock_quantity = new_stock
            prod.is_in_stock = 1 if new_stock > 0 else 0
            prod.save(ignore_permissions=True)

            prod.add_comment(
                "Info",
                _("Stock Adjustment {0} was CANCELLED: Stock reverted from {1} &rarr; {2}").format(
                    f"<a href='/app/stock-adjustment/{self.name}'><b>{self.name}</b></a>",
                    old_stock,
                    new_stock
                )
            )
