// Copyright (c) 2026, Zain and contributors
// For license information, please see license.txt

frappe.ui.form.on("Store Theme Settings", {
	refresh(frm) {
		render_themes_dashboard(frm);
	}
});

function render_themes_dashboard(frm) {
	// Inject styling for Shopify-style Themes Dashboard
	const style_id = "shopify-themes-dashboard-styles";
	if (!document.getElementById(style_id)) {
		const css = `
			.shopify-themes-dashboard {
				margin-bottom: 24px;
				font-family: var(--font-family, inherit);
			}
			.active-theme-card {
				background: #14171d;
				border: 1px solid #282d38;
				border-radius: 12px;
				padding: 24px;
				margin-bottom: 30px;
				display: flex;
				flex-direction: column;
				gap: 16px;
				box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
			}
			.active-theme-top {
				display: flex;
				justify-content: space-between;
				align-items: center;
				flex-wrap: wrap;
				gap: 12px;
			}
			.active-theme-info h3 {
				margin: 0 0 4px 0;
				font-size: 19px;
				font-weight: 700;
				color: #ffffff;
				display: flex;
				align-items: center;
				gap: 8px;
			}
			.badge-published {
				background: #108043;
				color: #ffffff;
				font-size: 11px;
				font-weight: 600;
				padding: 2px 8px;
				border-radius: 12px;
				display: inline-flex;
				align-items: center;
				gap: 4px;
			}
			.active-theme-sub {
				color: #9da5b4;
				font-size: 13px;
			}
			.active-theme-actions {
				display: flex;
				gap: 10px;
			}
			.btn-customize-theme {
				background: #388bfd !important;
				color: #ffffff !important;
				font-weight: 600 !important;
				border: none !important;
				border-radius: 8px !important;
				padding: 8px 18px !important;
				display: flex;
				align-items: center;
				gap: 6px;
				cursor: pointer;
				transition: background 0.15s;
			}
			.btn-customize-theme:hover {
				background: #2563eb !important;
			}
			.btn-preview-theme {
				background: #21262d !important;
				color: #f1f3f7 !important;
				border: 1px solid #30363d !important;
				border-radius: 8px !important;
				padding: 8px 16px !important;
				cursor: pointer;
			}
			.active-theme-preview-box {
				background: #1a1e26;
				border: 1px solid #2d3340;
				border-radius: 10px;
				padding: 16px;
				display: grid;
				grid-template-columns: 280px 1fr;
				gap: 20px;
				align-items: center;
			}
			@media (max-width: 768px) {
				.active-theme-preview-box {
					grid-template-columns: 1fr;
				}
			}
			.mini-mockup-frame {
				background: #0f1115;
				border: 1px solid #30363d;
				border-radius: 8px;
				overflow: hidden;
				box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
			}
			.mockup-header-bar {
				height: 22px;
				background: #1c2128;
				display: flex;
				align-items: center;
				padding: 0 8px;
				gap: 4px;
			}
			.mockup-dot {
				width: 7px;
				height: 7px;
				border-radius: 50%;
				background: #484f58;
			}
			.mockup-dot.red { background: #ea4a5a; }
			.mockup-dot.yellow { background: #f1b343; }
			.mockup-dot.green { background: #34d058; }
			.mockup-body {
				padding: 14px;
				min-height: 120px;
				display: flex;
				flex-direction: column;
				gap: 8px;
			}
			.mockup-nav {
				height: 14px;
				background: rgba(255, 255, 255, 0.1);
				border-radius: 3px;
				width: 80%;
			}
			.mockup-hero {
				height: 50px;
				border-radius: 4px;
				display: flex;
				align-items: center;
				justify-content: center;
				font-size: 11px;
				font-weight: 700;
				color: #ffffff;
			}
			.mockup-cards {
				display: flex;
				gap: 6px;
			}
			.mockup-card-item {
				flex: 1;
				height: 35px;
				background: rgba(255, 255, 255, 0.08);
				border-radius: 4px;
			}
			.active-theme-details {
				display: flex;
				flex-direction: column;
				gap: 12px;
			}
			.theme-meta-row {
				display: flex;
				gap: 20px;
				flex-wrap: wrap;
			}
			.theme-meta-pill {
				font-size: 12px;
				color: #9da5b4;
			}
			.theme-meta-pill strong {
				color: #f1f3f7;
				display: block;
				font-size: 13px;
			}
			.swatch-group {
				display: flex;
				gap: 6px;
				align-items: center;
				margin-top: 4px;
			}
			.color-circle {
				width: 20px;
				height: 20px;
				border-radius: 50%;
				border: 1px solid rgba(255, 255, 255, 0.2);
				display: inline-block;
			}
			/* Theme Library Grid */
			.library-header {
				margin-bottom: 16px;
			}
			.library-header h4 {
				font-size: 17px;
				font-weight: 700;
				color: #ffffff;
				margin: 0 0 4px 0;
			}
			.library-header p {
				font-size: 13px;
				color: #8b949e;
				margin: 0;
			}
			.filter-pills-bar {
				display: flex;
				gap: 8px;
				margin-bottom: 20px;
				overflow-x: auto;
				padding-bottom: 6px;
			}
			.filter-pill {
				background: #1e222b;
				color: #9da5b4;
				border: 1px solid #2a2f3b;
				padding: 5px 14px;
				border-radius: 20px;
				font-size: 12px;
				font-weight: 500;
				cursor: pointer;
				white-space: nowrap;
				transition: all 0.15s;
			}
			.filter-pill:hover,
			.filter-pill.active {
				background: #388bfd;
				border-color: #388bfd;
				color: #ffffff;
			}
			.themes-grid {
				display: grid;
				grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
				gap: 20px;
			}
			.theme-template-card {
				background: #14171d;
				border: 1px solid #262b36;
				border-radius: 10px;
				overflow: hidden;
				display: flex;
				flex-direction: column;
				transition: transform 0.18s, border-color 0.18s, box-shadow 0.18s;
			}
			.theme-template-card:hover {
				transform: translateY(-2px);
				border-color: #3b82f6;
				box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
			}
			.theme-template-card.is-active-theme {
				border: 2px solid #108043;
			}
			.card-preview-area {
				background: #1a1e27;
				padding: 18px;
				border-bottom: 1px solid #252a35;
			}
			.card-content-area {
				padding: 16px;
				display: flex;
				flex-direction: column;
				flex: 1;
				gap: 12px;
			}
			.card-header-row {
				display: flex;
				justify-content: space-between;
				align-items: flex-start;
			}
			.card-title {
				font-size: 16px;
				font-weight: 700;
				color: #ffffff;
				margin: 0;
			}
			.card-category {
				font-size: 11px;
				color: #8b949e;
				text-transform: uppercase;
				letter-spacing: 0.5px;
			}
			.card-badge {
				background: #252b36;
				color: #60a5fa;
				font-size: 11px;
				font-weight: 600;
				padding: 2px 8px;
				border-radius: 10px;
				border: 1px solid #303746;
			}
			.card-desc {
				font-size: 12px;
				color: #8b949e;
				line-height: 1.5;
				margin: 0;
				display: -webkit-box;
				-webkit-line-clamp: 2;
				-webkit-box-orient: vertical;
				overflow: hidden;
			}
			.card-specs-row {
				display: flex;
				justify-content: space-between;
				align-items: center;
				padding: 8px 10px;
				background: #1b1f29;
				border-radius: 6px;
				font-size: 11px;
			}
			.card-buttons-row {
				display: flex;
				gap: 8px;
				margin-top: auto;
				padding-top: 6px;
			}
			.btn-publish-theme {
				flex: 1;
				background: #108043 !important;
				color: #ffffff !important;
				border: none !important;
				border-radius: 6px !important;
				padding: 7px 12px !important;
				font-weight: 600 !important;
				font-size: 12px !important;
				cursor: pointer;
				transition: background 0.15s;
			}
			.btn-publish-theme:hover {
				background: #0d6937 !important;
			}
			.btn-card-customize {
				background: #252a35 !important;
				color: #e4e7ec !important;
				border: 1px solid #353c4b !important;
				border-radius: 6px !important;
				padding: 7px 12px !important;
				font-size: 12px !important;
				cursor: pointer;
			}
			.btn-card-customize:hover {
				background: #313847 !important;
				color: #ffffff !important;
			}
		`;
		const style = document.createElement("style");
		style.id = style_id;
		style.innerHTML = css;
		document.head.appendChild(style);
	}

	const $wrapper = frm.fields_dict.theme_library_html?.$wrapper;
	if (!$wrapper) return;

	$wrapper.html(`<div class="text-muted p-4">Loading store templates...</div>`);

	frappe.call({
		method: "ecommerce_store.ecommerce_store.doctype.store_theme.store_theme.get_theme_library",
		callback: function (r) {
			if (r && r.message) {
				build_dashboard_dom(frm, $wrapper, r.message);
			}
		}
	});
}

function build_dashboard_dom(frm, $wrapper, themes) {
	const active_name = frm.doc.active_theme_name || frm.doc.active_theme || "Dawn";
	const active_theme = themes.find(t => t.theme_name === active_name) || themes[0] || {};

	const html = $(`
		<div class="shopify-themes-dashboard">
			<!-- Active Theme Hero Card -->
			<div class="active-theme-card">
				<div class="active-theme-top">
					<div class="active-theme-info">
						<h3>
							<span>${frappe.utils.escape_html(active_theme.theme_name || "Dawn")}</span>
							<span class="badge-published">✓ Published Active</span>
						</h3>
						<div class="active-theme-sub">
							Category: <strong>${frappe.utils.escape_html(active_theme.category || "Fashion & Apparel")}</strong> • Version: ${active_theme.version || "1.0.0"}
						</div>
					</div>
					<div class="active-theme-actions">
						<button class="btn-customize-theme" type="button" id="btn-scroll-to-customizer">
							<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 20h9"></path><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"></path></svg>
							Customize Theme
						</button>
						<button class="btn-preview-theme" type="button" id="btn-duplicate-active">
							Duplicate
						</button>
					</div>
				</div>

				<div class="active-theme-preview-box">
					<div class="mini-mockup-frame">
						<div class="mockup-header-bar">
							<div class="mockup-dot red"></div>
							<div class="mockup-dot yellow"></div>
							<div class="mockup-dot green"></div>
						</div>
						<div class="mockup-body" style="background: ${active_theme.bg_color || '#ffffff'}; color: ${active_theme.text_color || '#121212'};">
							<div class="mockup-nav"></div>
							<div class="mockup-hero" style="background: ${active_theme.primary_color || '#121212'}; color: #ffffff;">
								${frappe.utils.escape_html(active_theme.theme_name)} Hero
							</div>
							<div class="mockup-cards">
								<div class="mockup-card-item"></div>
								<div class="mockup-card-item"></div>
								<div class="mockup-card-item"></div>
							</div>
						</div>
					</div>

					<div class="active-theme-details">
						<div class="theme-meta-row">
							<div class="theme-meta-pill">
								<span>Color Palette</span>
								<div class="swatch-group">
									<span class="color-circle" style="background: ${active_theme.primary_color || '#121212'};" title="Primary: ${active_theme.primary_color}"></span>
									<span class="color-circle" style="background: ${active_theme.secondary_color || '#f4f4f4'};" title="Secondary: ${active_theme.secondary_color}"></span>
									<span class="color-circle" style="background: ${active_theme.accent_color || '#000000'};" title="Accent: ${active_theme.accent_color}"></span>
									<span class="color-circle" style="background: ${active_theme.bg_color || '#ffffff'};" title="Background: ${active_theme.bg_color}"></span>
								</div>
							</div>
							<div class="theme-meta-pill">
								<span>Typography</span>
								<strong>${active_theme.font_heading || 'Plus Jakarta Sans'} / ${active_theme.font_body || 'Inter'}</strong>
							</div>
							<div class="theme-meta-pill">
								<span>Header & Cart</span>
								<strong>${active_theme.header_style || 'Centered Logo'} • ${active_theme.cart_type || 'Drawer Cart'}</strong>
							</div>
							<div class="theme-meta-pill">
								<span>Card Style</span>
								<strong>${active_theme.product_card_style || 'Minimal Compact'}</strong>
							</div>
						</div>
						<p style="margin: 0; font-size: 13px; color: #8b949e;">${frappe.utils.escape_html(active_theme.description || "")}</p>
					</div>
				</div>
			</div>

			<!-- Theme Library Grid -->
			<div class="library-header">
				<h4>Theme Library (Choose a Template)</h4>
				<p>Choose from our pre-designed templates tailored for specific industries. Switch templates anytime with 1-click or customize below.</p>
			</div>

			<!-- Category Filter Bar -->
			<div class="filter-pills-bar">
				<button type="button" class="filter-pill active" data-cat="all">All Templates (7)</button>
				<button type="button" class="filter-pill" data-cat="Fashion & Apparel">Fashion & Apparel</button>
				<button type="button" class="filter-pill" data-cat="Beauty & Cosmetics">Beauty & Cosmetics</button>
				<button type="button" class="filter-pill" data-cat="Electronics & Tech">Electronics & Tech</button>
				<button type="button" class="filter-pill" data-cat="Home & Furniture">Home & Furniture</button>
				<button type="button" class="filter-pill" data-cat="Grocery & Food">Grocery & Food</button>
				<button type="button" class="filter-pill" data-cat="Jewelry & Luxury">Jewelry & Luxury</button>
			</div>

			<!-- Themes Grid -->
			<div class="themes-grid"></div>
		</div>
	`);

	const $grid = html.find(".themes-grid");

	themes.forEach(theme => {
		const is_this_active = theme.theme_name === active_name;
		const $card = $(`
			<div class="theme-template-card ${is_this_active ? "is-active-theme" : ""}" data-category="${theme.category}">
				<div class="card-preview-area">
					<div class="mini-mockup-frame">
						<div class="mockup-header-bar">
							<div class="mockup-dot red"></div>
							<div class="mockup-dot yellow"></div>
							<div class="mockup-dot green"></div>
						</div>
						<div class="mockup-body" style="background: ${theme.bg_color || '#ffffff'}; color: ${theme.text_color || '#121212'};">
							<div class="mockup-nav"></div>
							<div class="mockup-hero" style="background: ${theme.primary_color || '#121212'}; color: #ffffff;">
								${frappe.utils.escape_html(theme.theme_name)}
							</div>
							<div class="mockup-cards">
								<div class="mockup-card-item"></div>
								<div class="mockup-card-item"></div>
								<div class="mockup-card-item"></div>
							</div>
						</div>
					</div>
				</div>

				<div class="card-content-area">
					<div class="card-header-row">
						<div>
							<div class="card-category">${frappe.utils.escape_html(theme.category)}</div>
							<h5 class="card-title">${frappe.utils.escape_html(theme.theme_name)}</h5>
						</div>
						${theme.badge_text ? `<span class="card-badge">${frappe.utils.escape_html(theme.badge_text)}</span>` : ""}
					</div>

					<p class="card-desc">${frappe.utils.escape_html(theme.description || "")}</p>

					<div class="card-specs-row">
						<div>
							<span style="color: #8b949e;">Colors:</span>
							<span class="color-circle" style="background: ${theme.primary_color}; width: 14px; height: 14px; vertical-align: middle; margin-left: 4px;"></span>
							<span class="color-circle" style="background: ${theme.accent_color}; width: 14px; height: 14px; vertical-align: middle;"></span>
						</div>
						<div style="color: #cbd5e1;">
							${theme.font_heading} / ${theme.font_body}
						</div>
					</div>

					<div class="card-buttons-row">
						${is_this_active ? `
							<button type="button" class="btn-publish-theme" style="background: #232833 !important; cursor: default;" disabled>
								✓ Active Template
							</button>
						` : `
							<button type="button" class="btn-publish-theme" data-publish="${theme.theme_name}">
								Publish Template
							</button>
						`}
						<button type="button" class="btn-card-customize" data-customize="${theme.theme_name}">
							Customize
						</button>
					</div>
				</div>
			</div>
		`);

		// Publish click handler
		$card.find("[data-publish]").on("click", function () {
			const target_name = $(this).attr("data-publish");
			frappe.confirm(`Publish '${target_name}' as your active store template?`, function () {
				frappe.call({
					method: "ecommerce_store.ecommerce_store.doctype.store_theme.store_theme.publish_theme",
					args: { theme_name: target_name },
					freeze: true,
					freeze_message: "Publishing template...",
					callback: function (r) {
						if (r && r.message && r.message.status === "success") {
							frappe.show_alert({ message: r.message.message, indicator: "green" });
							frm.reload_doc();
						}
					}
				});
			});
		});

		// Customize click handler
		$card.find("[data-customize]").on("click", function () {
			const target_name = $(this).attr("data-customize");
			// Copy this template's values to form inputs so user can edit them
			apply_template_to_customizer(frm, theme);
		});

		$grid.append($card);
	});

	// Filter tabs handler
	html.find(".filter-pill").on("click", function () {
		html.find(".filter-pill").removeClass("active");
		$(this).addClass("active");
		const cat = $(this).attr("data-cat");
		if (cat === "all") {
			$grid.find(".theme-template-card").show();
		} else {
			$grid.find(".theme-template-card").each(function () {
				$(this).toggle($(this).attr("data-category") === cat);
			});
		}
	});

	// Scroll to customizer button
	html.find("#btn-scroll-to-customizer").on("click", function () {
		$('html, body').animate({
			scrollTop: $('[data-fieldname="sec_brand"]').offset().top - 80
		}, 400);
	});

	// Duplicate button
	html.find("#btn-duplicate-active").on("click", function () {
		frappe.prompt(
			[{ fieldname: "new_name", fieldtype: "Data", label: "New Template Name", reqd: 1, default: `${active_name} Custom` }],
			function (values) {
				frappe.call({
					method: "ecommerce_store.ecommerce_store.doctype.store_theme.store_theme.duplicate_theme",
					args: { theme_name: active_name, new_name: values.new_name },
					callback: function (r) {
						if (r && r.message) {
							frappe.show_alert({ message: r.message.message, indicator: "green" });
							frm.reload_doc();
						}
					}
				});
			},
			"Duplicate Template"
		);
	});

	$wrapper.html(html);
}

function apply_template_to_customizer(frm, theme) {
	frm.set_value("active_theme_name", theme.theme_name);
	frm.set_value("primary_color", theme.primary_color);
	frm.set_value("secondary_color", theme.secondary_color);
	frm.set_value("accent_color", theme.accent_color);
	frm.set_value("bg_color", theme.bg_color);
	frm.set_value("text_color", theme.text_color);
	frm.set_value("font_heading", theme.font_heading);
	frm.set_value("font_body", theme.font_body);
	frm.set_value("header_style", theme.header_style);
	frm.set_value("hero_banner_style", theme.hero_banner_style);
	frm.set_value("product_card_style", theme.product_card_style);
	frm.set_value("cart_type", theme.cart_type);
	frm.set_value("footer_style", theme.footer_style);

	frappe.show_alert({
		message: `Loaded '${theme.theme_name}' into customizer. Tweak settings below and click Save!`,
		indicator: "blue"
	});

	$('html, body').animate({
		scrollTop: $('[data-fieldname="sec_colors"]').offset().top - 80
	}, 400);
}
