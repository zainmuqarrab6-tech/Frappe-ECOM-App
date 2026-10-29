// Copyright (c) 2026, Zain and contributors
// For license information, please see license.txt

frappe.ui.form.on("Product", {
    refresh(frm) {
        if (!frm.is_new()) {
            if (frm.doc.track_inventory && frm.doc.stock_quantity <= (frm.doc.low_stock_threshold || 3)) {
                frm.dashboard.set_headline_alert(
                    __("Low Stock Warning: Only {0} units remaining!", [frm.doc.stock_quantity]),
                    frm.doc.stock_quantity <= 0 ? "red" : "orange"
                );
            }

            // Quick Stock Update button
            frm.add_custom_button(__("Quick Stock Update"), () => {
                frappe.prompt({
                    fieldname: "new_stock",
                    fieldtype: "Int",
                    label: __("New Stock Quantity"),
                    default: frm.doc.stock_quantity,
                    reqd: 1
                }, (val) => {
                    frm.set_value("stock_quantity", val.new_stock);
                    frm.set_value("is_in_stock", val.new_stock > 0 ? 1 : 0);
                    frm.save();
                }, __("Update Inventory"), __("Update"));
            }, __("Inventory"));

            // Preview in API
            frm.add_custom_button(__("View API Response"), () => {
                window.open(`/api/method/ecommerce_store.api.products.get_product_detail?slug_or_id=${frm.doc.route_slug || frm.doc.name}`, "_blank");
            }, __("API"));
        }
    }
});
