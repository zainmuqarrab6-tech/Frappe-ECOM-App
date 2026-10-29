// Copyright (c) 2026, Zain and contributors
// For license information, please see license.txt

frappe.ui.form.on("Store Order", {
    refresh(frm) {
        // Quick visual indicators
        if (frm.doc.order_status === "Pending") {
            frm.dashboard.set_headline_alert(__("This order is Pending Confirmation"), "orange");
        } else if (frm.doc.order_status === "Delivered") {
            frm.dashboard.set_headline_alert(__("This order has been Delivered"), "green");
        } else if (frm.doc.order_status === "Cancelled") {
            frm.dashboard.set_headline_alert(__("This order is Cancelled"), "red");
        }

        // Action Buttons for Order Status Workflow
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
                        label: __("Courier Company (e.g. TCS, Leopards, DHL)"),
                        default: frm.doc.tracking_courier || ""
                    },
                    {
                        fieldname: "tracking_number",
                        fieldtype: "Data",
                        label: __("Tracking / Airway Bill Number"),
                        default: frm.doc.tracking_number || ""
                    }
                ], (values) => {
                    frm.set_value("order_status", "Shipped");
                    if (values.tracking_courier) frm.set_value("tracking_courier", values.tracking_courier);
                    if (values.tracking_number) frm.set_value("tracking_number", values.tracking_number);
                    frm.save();
                }, __("Enter Shipping Details"), __("Confirm & Ship"));
            }).addClass("btn-info");
        }

        if (frm.doc.order_status === "Shipped") {
            frm.add_custom_button(__("Mark as Delivered"), () => {
                frm.set_value("order_status", "Delivered");
                if (frm.doc.payment_method === "Cash on Delivery" && frm.doc.payment_status === "Unpaid") {
                    frm.set_value("payment_status", "Paid");
                }
                frm.save();
            }).addClass("btn-success");
        }

        if (frm.doc.order_status !== "Cancelled" && frm.doc.order_status !== "Delivered") {
            frm.add_custom_button(__("Cancel Order"), () => {
                frappe.confirm(__("Are you sure you want to cancel this order?"), () => {
                    frm.set_value("order_status", "Cancelled");
                    frm.save();
                });
            }, __("Manage"));
        }

        // Payment status button
        if (frm.doc.payment_status !== "Paid" && frm.doc.order_status !== "Cancelled") {
            frm.add_custom_button(__("Mark as Paid"), () => {
                frm.set_value("payment_status", "Paid");
                frm.save();
            }, __("Payment"));
        }
    }
});
