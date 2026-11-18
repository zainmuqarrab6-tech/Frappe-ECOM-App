// Copyright (c) 2026, Zain and contributors
// For license information, please see license.txt

frappe.ui.form.on("Store Settings", {
	refresh(frm) {
		// Remove any lingering custom shopify style tag if present in DOM
		const old_style = document.getElementById("shopify-settings-custom-styles");
		if (old_style) {
			old_style.remove();
		}

		// Native Frappe action button
		frm.add_custom_button(__("Visit Store"), function () {
			if (frm.doc.custom_domain) {
				const url = frm.doc.custom_domain.startsWith("http") ? frm.doc.custom_domain : `http://${frm.doc.custom_domain}`;
				window.open(url, "_blank");
			} else {
				window.open("/store", "_blank");
			}
		});
	}
});
