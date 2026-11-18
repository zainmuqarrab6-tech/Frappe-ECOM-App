// Copyright (c) 2026, Zain and contributors
// For license information, please see license.txt

frappe.ui.form.on("Store Settings", {
	refresh(frm) {
		setup_shopify_settings_view(frm);
	},
	store_name(frm) {
		update_store_card(frm);
	},
	primary_domain(frm) {
		update_store_card(frm);
	},
	custom_domain(frm) {
		update_store_card(frm);
	}
});

function update_store_card(frm) {
	const site_name = frappe.boot?.sitename || "frappe-ecom.local";
	const store_name = frm.doc.store_name || "Frappe ECom";
	const domain = frm.doc.primary_domain || frm.doc.custom_domain || site_name;
	const initials = store_name.split(" ").filter(Boolean).map(w => w[0]).join("").substring(0, 2).toUpperCase() || "FE";

	$(".shopify-store-badge").text(initials);
	$(".shopify-store-name").text(store_name);
	$(".shopify-store-domain").text(domain);
}

function setup_shopify_settings_view(frm) {
	// Inject styling for Shopify Settings Layout
	const style_id = "shopify-settings-custom-styles";
	if (!document.getElementById(style_id)) {
		const css = `
			.shopify-settings-wrapper {
				display: flex;
				min-height: calc(100vh - 120px);
				background: var(--bg-color, #0f1115);
				border-radius: 8px;
				overflow: hidden;
				margin-top: -15px;
			}
			.shopify-settings-sidebar {
				width: 310px;
				min-width: 310px;
				background: #14171d;
				border-right: 1px solid #232731;
				padding: 16px 12px;
				display: flex;
				flex-direction: column;
				height: calc(100vh - 120px);
				position: sticky;
				top: 60px;
				overflow-y: auto;
			}
			.shopify-settings-header {
				margin-bottom: 12px;
			}
			.shopify-title-bar {
				display: flex;
				align-items: center;
				gap: 10px;
				margin-bottom: 14px;
				cursor: pointer;
				padding: 4px 6px;
				border-radius: 6px;
				transition: background 0.15s;
			}
			.shopify-title-bar:hover {
				background: #1e222b;
			}
			.shopify-title-bar svg {
				stroke: #a0a6b5;
			}
			.shopify-title-bar h3 {
				margin: 0;
				font-size: 17px;
				font-weight: 700;
				color: #e4e7ec;
			}
			.shopify-search-wrap {
				position: relative;
				margin-bottom: 12px;
			}
			.shopify-search-wrap svg {
				position: absolute;
				left: 12px;
				top: 50%;
				transform: translateY(-50%);
				stroke: #667085;
				pointer-events: none;
			}
			.shopify-search-input {
				width: 100%;
				background: #1e222b;
				border: 1px solid #2a2f3b;
				border-radius: 8px;
				padding: 7px 12px 7px 34px;
				font-size: 13px;
				color: #f1f3f7;
				outline: none;
				transition: border-color 0.15s;
			}
			.shopify-search-input:focus {
				border-color: #388bfd;
			}
			.shopify-store-card {
				display: flex;
				align-items: center;
				gap: 10px;
				padding: 8px 10px;
				background: #1e222b;
				border: 1px solid #282d38;
				border-radius: 8px;
				margin-bottom: 14px;
			}
			.shopify-store-badge {
				width: 32px;
				height: 32px;
				border-radius: 6px;
				background: #108043;
				color: #fff;
				font-weight: 700;
				font-size: 12px;
				display: flex;
				align-items: center;
				justify-content: center;
			}
			.shopify-store-meta {
				flex: 1;
				min-width: 0;
			}
			.shopify-store-name {
				font-size: 13px;
				font-weight: 600;
				color: #f1f3f7;
				white-space: nowrap;
				overflow: hidden;
				text-overflow: ellipsis;
			}
			.shopify-store-domain {
				font-size: 11px;
				color: #8b949e;
				white-space: nowrap;
				overflow: hidden;
				text-overflow: ellipsis;
			}
			.shopify-store-dots {
				color: #8b949e;
				font-size: 16px;
				letter-spacing: 1px;
			}
			.shopify-nav-list {
				list-style: none;
				padding: 0;
				margin: 0;
				display: flex;
				flex-direction: column;
				gap: 2px;
			}
			.shopify-nav-item {
				display: flex;
				align-items: center;
				gap: 12px;
				padding: 8px 12px;
				border-radius: 6px;
				color: #b0b7c3;
				font-size: 13px;
				font-weight: 500;
				cursor: pointer;
				transition: background 0.12s, color 0.12s;
			}
			.shopify-nav-item:hover {
				background: #1c2029;
				color: #ffffff;
			}
			.shopify-nav-item.active {
				background: #252b36;
				color: #ffffff;
				font-weight: 600;
			}
			.shopify-nav-item svg {
				stroke: #8b949e;
				flex-shrink: 0;
			}
			.shopify-nav-item:hover svg,
			.shopify-nav-item.active svg {
				stroke: #ffffff;
			}
			.shopify-content-panel {
				flex: 1;
				min-width: 0;
				padding: 24px 32px;
				background: #0f1115;
				overflow-y: auto;
			}
			/* Hide native horizontal tabs bar since custom sidebar replaces it */
			.form-tabs-list {
				display: none !important;
			}
			/* Shopify Polaris Card styling for Form Sections */
			.form-tab-content .section-break {
				background: #14171d;
				border: 1px solid #232731;
				border-radius: 10px;
				padding: 20px 24px;
				margin-bottom: 20px;
			}
			.form-tab-content .section-head {
				font-size: 15px;
				font-weight: 600;
				color: #f1f3f7;
				margin-bottom: 16px;
				border-bottom: 1px solid #1f242e;
				padding-bottom: 10px;
			}
			.form-tab-content .form-group {
				margin-bottom: 14px;
			}
			.form-tab-content label {
				font-size: 12px;
				color: #9da5b4;
				margin-bottom: 5px;
			}
			.form-tab-content input.form-control,
			.form-tab-content select.form-control,
			.form-tab-content textarea.form-control {
				background: #1b1e26 !important;
				border: 1px solid #2b303d !important;
				color: #f1f3f7 !important;
				border-radius: 6px !important;
			}
			.form-tab-content input.form-control:focus,
			.form-tab-content select.form-control:focus,
			.form-tab-content textarea.form-control:focus {
				border-color: #388bfd !important;
				box-shadow: 0 0 0 2px rgba(56, 139, 253, 0.2) !important;
			}
		`;
		const style = document.createElement("style");
		style.id = style_id;
		style.innerHTML = css;
		document.head.appendChild(style);
	}

	const $layout = frm.layout.page;
	if (!$layout.find(".shopify-settings-sidebar").length) {
		const items = [
			{ key: "tab_plan", label: "Plan", icon: `<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="16" rx="2"></rect><line x1="7" y1="8" x2="17" y2="8"></line><line x1="7" y1="12" x2="17" y2="12"></line><line x1="7" y1="16" x2="13" y2="16"></line></svg>` },
			{ key: "tab_billing", label: "Billing", icon: `<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="5" width="20" height="14" rx="2"></rect><line x1="2" y1="10" x2="22" y2="10"></line><circle cx="7" cy="15" r="1"></circle><path d="M14 14h3"></path></svg>` },
			{ key: "tab_users", label: "Users", icon: `<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>` },
			{ key: "tab_payments", label: "Payments", icon: `<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12V7H5a2 2 0 0 1 0-4h14v4"></path><path d="M3 5v14a2 2 0 0 0 2 2h16v-5"></path><path d="M18 12a2 2 0 0 0 0 4h4v-4Z"></path></svg>` },
			{ key: "tab_checkout", label: "Checkout", icon: `<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path></svg>` },
			{ key: "tab_customer_accounts", label: "Customer accounts", icon: `<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>` },
			{ key: "tab_shipping", label: "Shipping and delivery", icon: `<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="3" width="15" height="13"></rect><polygon points="16 8 20 8 23 11 23 16 16 16 8"></polygon><circle cx="5.5" cy="18.5" r="2.5"></circle><circle cx="18.5" cy="18.5" r="2.5"></circle></svg>` },
			{ key: "tab_taxes", label: "Taxes and duties", icon: `<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="M16 8l-8 8"></path><circle cx="9" cy="9" r="1.5"></circle><circle cx="15" cy="15" r="1.5"></circle></svg>` },
			{ key: "tab_locations", label: "Locations", icon: `<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>` },
			{ key: "tab_markets", label: "Markets", icon: `<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>` },
			{ key: "tab_apps", label: "Apps", icon: `<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>` },
			{ key: "tab_sales_channels", label: "Sales channels", icon: `<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"></circle><circle cx="6" cy="12" r="3"></circle><circle cx="18" cy="19" r="3"></circle><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line></svg>` },
			{ key: "tab_domains", label: "Domains", icon: `<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"></rect><line x1="2" y1="9" x2="22" y2="9"></line><line x1="15" y1="14" x2="19" y2="14"></line></svg>` },
			{ key: "tab_customer_events", label: "Customer events", icon: `<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>` },
			{ key: "tab_notifications", label: "Notifications", icon: `<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>` },
			{ key: "tab_metafields", label: "Metafields and metaobjects", icon: `<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path></svg>` },
			{ key: "tab_languages", label: "Languages", icon: `<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="M2 12h20"></path><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1 4-10z"></path></svg>` },
			{ key: "tab_customer_privacy", label: "Customer privacy", icon: `<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>` },
			{ key: "tab_policies", label: "Policies", icon: `<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg>` }
		];

		const site_name = frappe.boot?.sitename || "frappe-ecom.local";
		const store_name = frm.doc.store_name || "Frappe ECom";
		const primary_domain = frm.doc.primary_domain || frm.doc.custom_domain || site_name;
		const initials = store_name.split(" ").filter(Boolean).map(w => w[0]).join("").substring(0, 2).toUpperCase() || "FE";

		const $content = $layout.find(".form-tab-content");
		const $wrapper = $(`<div class="shopify-settings-wrapper"></div>`);
		const $sidebar = $(`
			<div class="shopify-settings-sidebar">
				<div class="shopify-settings-header">
					<div class="shopify-title-bar">
						<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
						<h3>Settings</h3>
					</div>
					<div class="shopify-search-wrap">
						<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
						<input type="text" class="shopify-search-input" placeholder="Search settings" />
					</div>
					<div class="shopify-store-card">
						<div class="shopify-store-badge">${initials}</div>
						<div class="shopify-store-meta">
							<div class="shopify-store-name">${frappe.utils.escape_html(store_name)}</div>
							<div class="shopify-store-domain">${frappe.utils.escape_html(primary_domain)}</div>
						</div>
						<div class="shopify-store-dots">•••</div>
					</div>
				</div>
				<ul class="shopify-nav-list"></ul>
			</div>
		`);

		const $list = $sidebar.find(".shopify-nav-list");
		items.forEach((item, index) => {
			const $li = $(`
				<li class="shopify-nav-item ${index === 0 ? "active" : ""}" data-tab="${item.key}">
					${item.icon}
					<span>${item.label}</span>
				</li>
			`);
			$li.on("click", function() {
				$list.find(".shopify-nav-item").removeClass("active");
				$(this).addClass("active");
				activate_form_tab(frm, item.key);
			});
			$list.append($li);
		});

		// Real-time search filter
		$sidebar.find(".shopify-search-input").on("input", function() {
			const query = $(this).val().toLowerCase().trim();
			$list.find(".shopify-nav-item").each(function() {
				const label = $(this).find("span").text().toLowerCase();
				$(this).toggle(label.includes(query));
			});
		});

		// Back button handler
		$sidebar.find(".shopify-title-bar").on("click", function() {
			frappe.set_route("workspace", "Ecommerce Store");
		});

		// Wrap content
		$content.addClass("shopify-content-panel");
		$content.before($wrapper);
		$wrapper.append($sidebar);
		$wrapper.append($content);

		// Activate initial tab
		activate_form_tab(frm, "tab_plan");
	}
}

function activate_form_tab(frm, tab_fieldname) {
	if (!frm || !frm.layout) return;

	const tab = frm.layout.tabs?.find(t => t.df && t.df.fieldname === tab_fieldname);
	if (tab && typeof tab.set_active === "function") {
		tab.set_active();
	} else {
		const selector = `#store-settings-${tab_fieldname}`;
		$(".form-tab-content .tab-pane").removeClass("show active");
		$(selector).addClass("show active");
	}
}
