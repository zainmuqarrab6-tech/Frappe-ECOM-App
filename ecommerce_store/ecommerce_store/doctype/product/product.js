// Copyright (c) 2026, Zain and contributors
// For license information, please see license.txt

frappe.ui.form.on("Product", {
    refresh(frm) {
        // 1. Shopify-style Status Banners
        if (frm.doc.status === "Draft") {
            frm.dashboard.set_headline_alert(__("This product is a Draft and not visible in the storefront"), "yellow");
        } else if (frm.doc.status === "Archived") {
            frm.dashboard.set_headline_alert(__("This product is Archived"), "gray");
        } else if (frm.doc.track_inventory && frm.doc.stock_quantity <= (frm.doc.low_stock_threshold || 3)) {
            frm.dashboard.set_headline_alert(
                __("Low Stock Alert: Only {0} units remaining in stock!", [frm.doc.stock_quantity]),
                frm.doc.stock_quantity <= 0 ? "red" : "orange"
            );
        }

        // 2. Generate Variants Button (Shopify Matrix)
        if (frm.doc.has_variants && !frm.is_new()) {
            frm.add_custom_button(__("Generate Variants Matrix"), () => {
                if (!frm.doc.options || frm.doc.options.length === 0) {
                    frappe.msgprint(__("Please add at least one Option (e.g. Size or Color) with comma-separated values first."));
                    return;
                }

                frappe.confirm(
                    __("Generate / update all variant combinations from options? Existing customized prices and SKUs will be preserved."),
                    () => {
                        frappe.call({
                            method: "generate_variants_matrix",
                            doc: frm.doc,
                            freeze: true,
                            freeze_message: __("Generating Shopify Variants..."),
                            callback: function(r) {
                                if (!r.exc) {
                                    frappe.show_alert({
                                        message: __("{0} Variants generated successfully!", [r.message.count]),
                                        indicator: "green"
                                    });
                                    frm.reload_doc();
                                }
                            }
                        });
                    }
                );
            }, __("Variants")).addClass("btn-primary");
        }

        // 3. Quick Actions
        if (!frm.is_new()) {
            frm.add_custom_button(__("View in Storefront API"), () => {
                window.open(`/api/method/ecommerce_store.api.products.get_product_detail?slug_or_id=${frm.doc.route_slug || frm.doc.name}`, "_blank");
            }, __("Preview"));

            if (!frm.doc.has_variants) {
                frm.add_custom_button(__("Quick Stock Update"), () => {
                    frappe.prompt({
                        fieldname: "new_stock",
                        fieldtype: "Int",
                        label: __("New Available Stock Quantity"),
                        default: frm.doc.stock_quantity,
                        reqd: 1
                    }, (val) => {
                        frm.set_value("stock_quantity", val.new_stock);
                        frm.set_value("is_in_stock", val.new_stock > 0 ? 1 : 0);
                        frm.save();
                    }, __("Update Stock"), __("Save"));
                }, __("Inventory"));
            }
        }
    },

    title(frm) {
        // Auto-generate URL slug from title if new or empty
        if ((frm.is_new() || !frm.doc.route_slug) && frm.doc.title) {
            let slug = frm.doc.title.toLowerCase()
                .replace(/[^\w\s-]/g, '')
                .trim()
                .replace(/[-\s]+/g, '-');
            frm.set_value("route_slug", slug);
        }

        if (!frm.doc.seo_meta_title && frm.doc.title) {
            frm.set_value("seo_meta_title", frm.doc.title);
        }
    },

    price(frm) {
        calculate_profit_and_margin(frm);
    },

    cost_price(frm) {
        calculate_profit_and_margin(frm);
    },

    has_variants(frm) {
        if (frm.doc.has_variants && (!frm.doc.options || frm.doc.options.length === 0)) {
            // Suggest default Option 1: Size
            let row = frm.add_child("options");
            row.option_name = "Size";
            row.option_values = "Small, Medium, Large";
            frm.refresh_field("options");
        }
    }
});

function calculate_profit_and_margin(frm) {
    let price = flt(frm.doc.price);
    let cost = flt(frm.doc.cost_price);
    if (price > 0 && cost > 0) {
        let profit = price - cost;
        let margin = (profit / price) * 100;
        frm.set_value("profit", profit);
        frm.set_value("margin_percent", margin);
    } else {
        frm.set_value("profit", 0);
        frm.set_value("margin_percent", 0);
    }
}
