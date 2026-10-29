frappe.listview_settings['Store Order'] = {
    add_fields: ['order_status', 'payment_status', 'grand_total', 'customer_name'],
    get_indicator: function(doc) {
        if (doc.order_status === "Delivered") {
            return [__("Delivered"), "green", "order_status,=,Delivered"];
        } else if (doc.order_status === "Cancelled") {
            return [__("Cancelled"), "red", "order_status,=,Cancelled"];
        } else if (doc.order_status === "Shipped") {
            return [__("Shipped"), "blue", "order_status,=,Shipped"];
        } else if (doc.order_status === "Confirmed" || doc.order_status === "Processing") {
            return [__(doc.order_status), "orange", "order_status,=," + doc.order_status];
        } else {
            return [__("Pending"), "yellow", "order_status,=,Pending"];
        }
    }
};

