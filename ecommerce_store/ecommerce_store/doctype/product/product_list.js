frappe.listview_settings['Product'] = {
    add_fields: ['price', 'is_in_stock', 'stock_quantity', 'track_inventory'],
    get_indicator: function(doc) {
        if (!doc.is_in_stock || (doc.track_inventory && doc.stock_quantity <= 0)) {
            return [__("Out of Stock"), "red", "is_in_stock,=,0"];
        } else if (doc.track_inventory && doc.stock_quantity <= 5) {
            return [__("Low Stock ({0})", [doc.stock_quantity]), "orange", "stock_quantity,<=,5"];
        } else {
            return [__("In Stock ({0})", [doc.stock_quantity]), "green", "is_in_stock,=,1"];
        }
    }
};

