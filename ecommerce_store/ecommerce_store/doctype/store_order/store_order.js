// Copyright (c) 2026, Zain and contributors
// For license information, please see license.txt

frappe.ui.form.on("Store Order", {
    refresh(frm) {
        // Visual indicator banners
        if (frm.doc.order_status === "Pending") {
            frm.dashboard.set_headline_alert(__("This order is Pending Confirmation"), "orange");
        } else if (frm.doc.order_status === "Confirmed" || frm.doc.order_status === "Processing") {
            frm.dashboard.set_headline_alert(__("This order is being processed for fulfillment"), "blue");
        } else if (frm.doc.order_status === "Shipped") {
            frm.dashboard.set_headline_alert(__("This order is in transit with courier"), "purple");
        } else if (frm.doc.order_status === "Delivered") {
            frm.dashboard.set_headline_alert(__("This order has been Delivered"), "green");
        } else if (frm.doc.order_status === "Cancelled") {
            frm.dashboard.set_headline_alert(__("This order is Cancelled & Inventory has been restored"), "red");
        }

        // Print Formats Shortcuts
        if (!frm.is_new()) {
            frm.add_custom_button(__("Tax Invoice (A4)"), () => {
                const print_url = `/printview?doctype=Store+Order&name=${encodeURIComponent(frm.doc.name)}&format=Commercial+Tax+Invoice`;
                window.open(print_url, "_blank");
            }, __("Print"));

            frm.add_custom_button(__("Shipping Label (4x6)"), () => {
                const print_url = `/printview?doctype=Store+Order&name=${encodeURIComponent(frm.doc.name)}&format=Thermal+Courier+Shipping+Label`;
                window.open(print_url, "_blank");
            }, __("Print"));
        }

        // Action Buttons for Order Lifecycle
        if (frm.doc.order_status === "Pending") {
            frm.add_custom_button(__("Confirm Order"), () => {
                frm.set_value("order_status", "Confirmed");
                frm.save();
            }).addClass("btn-primary");
        }

        if (frm.doc.order_status === "Confirmed" || frm.doc.order_status === "Processing") {
            frm.add_custom_button(__("Mark as Shipped"), () => {
                frappe.prompt([
                    {
                        fieldname: "tracking_courier",
                        fieldtype: "Data",
                        label: __("Courier (e.g. TCS, Leopards, PostEx, Trax, DHL)"),
                        default: frm.doc.tracking_courier || "TCS"
                    },
                    {
                        fieldname: "tracking_number",
                        fieldtype: "Data",
                        label: __("Tracking / Waybill Number"),
                        default: frm.doc.tracking_number || ""
                    }
                ], (values) => {
                    frm.set_value("order_status", "Shipped");
                    if (values.tracking_courier) frm.set_value("tracking_courier", values.tracking_courier);
                    if (values.tracking_number) frm.set_value("tracking_number", values.tracking_number);
                    frm.save();
                }, __("Courier Shipping Details"), __("Confirm & Ship"));
            }).addClass("btn-info");
        }

        if (frm.doc.order_status === "Shipped") {
            frm.add_custom_button(__("Mark as Delivered"), () => {
                frappe.confirm(__("Mark this order as Delivered? If Cash on Delivery, payment status will be marked Paid."), () => {
                    frm.set_value("order_status", "Delivered");
                    if (frm.doc.payment_method === "Cash on Delivery" && frm.doc.payment_status === "Unpaid") {
                        frm.set_value("payment_status", "Paid");
                    }
                    frm.save();
                });
            }).addClass("btn-success");
        }

        if (frm.doc.order_status !== "Cancelled" && frm.doc.order_status !== "Delivered" && !frm.is_new()) {
            frm.add_custom_button(__("Cancel Order"), () => {
                frappe.prompt([
                    {
                        fieldname: "reason",
                        fieldtype: "Small Text",
                        label: __("Reason for Cancellation"),
                        default: "Customer requested cancellation"
                    }
                ], (values) => {
                    frappe.call({
                        method: "cancel_order",
                        doc: frm.doc,
                        args: {
                            reason: values.reason
                        },
                        freeze: true,
                        freeze_message: __("Cancelling order and restoring inventory..."),
                        callback: function(r) {
                            if (!r.exc) {
                                frm.reload_doc();
                            }
                        }
                    });
                }, __("Cancel Order & Restock"), __("Confirm Cancellation"));
            }, __("Manage"));
        }

        // Payment status toggle button
        if (frm.doc.payment_status !== "Paid" && frm.doc.order_status !== "Cancelled" && !frm.is_new()) {
            frm.add_custom_button(__("Mark as Paid"), () => {
                frm.set_value("payment_status", "Paid");
                frm.save();
            }, __("Payment"));
        }
    }
});
