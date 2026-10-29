// Copyright (c) 2026, Zain and contributors
// For license information, please see license.txt

frappe.ui.form.on("Stock Adjustment", {
    refresh(frm) {
        if (frm.doc.docstatus === 1) {
            frm.dashboard.set_headline_alert(__("Stock Adjustment submitted & applied to product stock."), "green");
        } else if (frm.doc.docstatus === 2) {
            frm.dashboard.set_headline_alert(__("Stock Adjustment cancelled. Inventory has been reverted."), "red");
        }
    }
});

frappe.ui.form.on("Stock Adjustment Item", {
    product: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.product) {
            frappe.db.get_value("Product", row.product, ["title", "stock_quantity"], function(r) {
                if (r) {
                    frappe.model.set_value(cdt, cdn, "product_name", r.title);
                    frappe.model.set_value(cdt, cdn, "current_stock", r.stock_quantity || 0);
                }
            });
        }
    }
});
