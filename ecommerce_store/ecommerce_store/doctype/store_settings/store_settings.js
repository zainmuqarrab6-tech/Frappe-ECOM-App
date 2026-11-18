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
			const domain = frm.doc.custom_domain || frm.doc.primary_domain || window.location.origin;
			const url = domain.startsWith("http") ? domain : `http://${domain}`;
			window.open(url, "_blank");
		});
	}
});
