// Copyright (c) 2026, Zain and contributors
// For license information, please see license.txt

frappe.ui.form.on("Store Theme Settings", {
	refresh(frm) {
		render_shopify_theme_manager(frm);
	}
});

function render_shopify_theme_manager(frm) {
	const style_id = "shopify-theme-manager-styles";
	if (!document.getElementById(style_id)) {
		const css = `
			.theme-manager-container {
				margin-bottom: 24px;
				font-family: var(--font-stack, inherit);
			}

			/* Top Action Bar */
			.theme-top-actions {
				display: flex;
				justify-content: space-between;
				align-items: center;
				margin-bottom: 24px;
				padding-bottom: 16px;
				border-bottom: 1px solid var(--border-color, #e2e8f0);
				flex-wrap: wrap;
				gap: 12px;
			}
			.theme-header-titles h2 {
				margin: 0 0 4px 0;
				font-size: 22px;
				font-weight: 800;
				color: var(--text-color, #1e293b);
			}
			.theme-header-titles p {
				margin: 0;
				font-size: 13px;
				color: var(--text-muted, #64748b);
			}
			.theme-header-btns {
				display: flex;
				gap: 10px;
				align-items: center;
			}
			.btn-github-deploy {
				background: #181717 !important;
				color: #ffffff !important;
				font-weight: 600 !important;
				padding: 8px 16px !important;
				border-radius: 8px !important;
				display: inline-flex !important;
				align-items: center !important;
				gap: 8px !important;
				border: 1px solid rgba(255, 255, 255, 0.15) !important;
				transition: transform 0.15s, opacity 0.15s !important;
			}
			.btn-github-deploy:hover {
				opacity: 0.95;
				transform: translateY(-1px);
			}
			.btn-view-store {
				background: var(--btn-default-bg, #ffffff) !important;
				color: var(--text-color, #1e293b) !important;
				border: 1px solid var(--border-color, #cbd5e1) !important;
				font-weight: 600 !important;
				padding: 8px 16px !important;
				border-radius: 8px !important;
				display: inline-flex !important;
				align-items: center !important;
				gap: 6px !important;
			}
			.btn-view-store:hover {
				background: var(--bg-color, #f8fafc) !important;
			}

			/* Active Hero Theme Card */
			.active-theme-card {
				background: var(--card-bg, #ffffff);
				border: 1px solid var(--border-color, #e2e8f0);
				border-radius: 12px;
				padding: 24px;
				margin-bottom: 32px;
				box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
				transition: box-shadow 0.2s;
			}
			.active-theme-top {
				display: flex;
				justify-content: space-between;
				align-items: flex-start;
				margin-bottom: 20px;
				flex-wrap: wrap;
				gap: 12px;
			}
			.active-theme-info h3 {
				margin: 0 0 6px 0;
				font-size: 19px;
				font-weight: 700;
				color: var(--text-color, #1e293b);
				display: flex;
				align-items: center;
				gap: 8px;
			}
			.badge-published {
				background: #10b981;
				color: #ffffff;
				font-size: 11px;
				font-weight: 700;
				padding: 3px 10px;
				border-radius: 12px;
				display: inline-flex;
				align-items: center;
				gap: 4px;
				letter-spacing: 0.3px;
			}
			.active-theme-sub {
				color: var(--text-muted, #64748b);
				font-size: 13px;
			}
			.active-theme-actions {
				display: flex;
				gap: 10px;
			}
			.btn-customize-active {
				background: var(--primary, #0284c7) !important;
				color: #ffffff !important;
				font-weight: 700 !important;
				border: none !important;
				border-radius: 8px !important;
				padding: 9px 20px !important;
				cursor: pointer;
				transition: opacity 0.15s;
				box-shadow: 0 2px 6px rgba(2, 132, 199, 0.3);
			}
			.btn-customize-active:hover {
				opacity: 0.9;
			}
			.btn-duplicate-active {
				background: var(--btn-default-bg, #f1f5f9) !important;
				color: var(--text-color, #1e293b) !important;
				border: 1px solid var(--border-color, #cbd5e1) !important;
				border-radius: 8px !important;
				padding: 9px 16px !important;
				font-weight: 600 !important;
				cursor: pointer;
			}

			/* Mini Preview Browser Frame */
			.active-theme-preview-box {
				background: var(--bg-color, #f8fafc);
				border: 1px solid var(--border-color, #e2e8f0);
				border-radius: 10px;
				padding: 20px;
				display: grid;
				grid-template-columns: 290px 1fr;
				gap: 24px;
				align-items: center;
			}
			@media (max-width: 800px) {
				.active-theme-preview-box {
					grid-template-columns: 1fr;
				}
			}
			.mini-mockup-frame {
				background: #ffffff;
				border: 1px solid var(--border-color, #cbd5e1);
				border-radius: 8px;
				overflow: hidden;
				box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
			}
			.mockup-header-bar {
				height: 24px;
				background: #f1f5f9;
				display: flex;
				align-items: center;
				padding: 0 10px;
				gap: 5px;
				border-bottom: 1px solid #e2e8f0;
			}
			.mockup-dot {
				width: 8px;
				height: 8px;
				border-radius: 50%;
			}
			.mockup-dot.red { background: #ef4444; }
			.mockup-dot.yellow { background: #f59e0b; }
			.mockup-dot.green { background: #10b981; }
			.mockup-body {
				padding: 16px;
				min-height: 130px;
				display: flex;
				flex-direction: column;
				gap: 10px;
				background: var(--mockup-bg, #ffffff);
			}
			.mockup-nav {
				height: 14px;
				background: rgba(0, 0, 0, 0.08);
				border-radius: 3px;
				width: 75%;
			}
			.mockup-hero {
				height: 54px;
				border-radius: 6px;
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
				height: 38px;
				background: rgba(0, 0, 0, 0.06);
				border-radius: 4px;
			}

			.active-theme-details {
				display: flex;
				flex-direction: column;
				gap: 14px;
			}
			.theme-meta-row {
				display: flex;
				gap: 24px;
				flex-wrap: wrap;
			}
			.theme-meta-pill {
				font-size: 12px;
				color: var(--text-muted, #64748b);
			}
			.theme-meta-pill strong {
				color: var(--text-color, #1e293b);
				display: block;
				font-size: 13px;
				margin-top: 2px;
			}
			.color-circle {
				width: 20px;
				height: 20px;
				border-radius: 50%;
				border: 1px solid rgba(0, 0, 0, 0.15);
				display: inline-block;
				vertical-align: middle;
			}
			.swatch-group {
				display: flex;
				gap: 6px;
				align-items: center;
				margin-top: 4px;
			}

			/* Theme Library Section */
			.library-section {
				margin-top: 36px;
			}
			.library-header {
				display: flex;
				justify-content: space-between;
				align-items: flex-end;
				margin-bottom: 20px;
				flex-wrap: wrap;
				gap: 12px;
			}
			.library-header h4 {
				font-size: 18px;
				font-weight: 800;
				color: var(--text-color, #1e293b);
				margin: 0 0 4px 0;
			}
			.library-header p {
				font-size: 13px;
				color: var(--text-muted, #64748b);
				margin: 0;
			}
			.filter-pills-bar {
				display: flex;
				gap: 8px;
				margin-bottom: 24px;
				overflow-x: auto;
				padding-bottom: 4px;
			}
			.filter-pill {
				padding: 6px 14px;
				border-radius: 20px;
				background: var(--btn-default-bg, #f1f5f9);
				color: var(--text-color, #475569);
				font-size: 12px;
				font-weight: 600;
				cursor: pointer;
				border: 1px solid transparent;
				transition: all 0.15s;
				white-space: nowrap;
			}
			.filter-pill:hover, .filter-pill.active {
				background: var(--primary, #0284c7);
				color: #ffffff;
			}

			/* Grid of Theme Templates */
			.themes-grid {
				display: grid;
				grid-template-columns: repeat(auto-fill, minmax(310px, 1fr));
				gap: 24px;
			}
			.theme-template-card {
				background: var(--card-bg, #ffffff);
				border: 1px solid var(--border-color, #e2e8f0);
				border-radius: 12px;
				overflow: hidden;
				display: flex;
				flex-direction: column;
				transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
			}
			.theme-template-card:hover {
				transform: translateY(-3px);
				box-shadow: 0 10px 24px rgba(0, 0, 0, 0.08);
				border-color: #cbd5e1;
			}
			.card-mockup-area {
				background: #f8fafc;
				padding: 20px 16px 16px 16px;
				border-bottom: 1px solid var(--border-color, #e2e8f0);
			}
			.card-content-area {
				padding: 18px 20px;
				display: flex;
				flex-direction: column;
				flex: 1;
			}
			.card-header-row {
				display: flex;
				justify-content: space-between;
				align-items: flex-start;
				margin-bottom: 8px;
			}
			.card-category {
				font-size: 11px;
				font-weight: 700;
				text-transform: uppercase;
				color: var(--primary, #0284c7);
				letter-spacing: 0.5px;
			}
			.card-title {
				font-size: 16px;
				font-weight: 700;
				color: var(--text-color, #1e293b);
				margin: 2px 0 0 0;
			}
			.card-badge {
				background: #f1f5f9;
				color: #334155;
				font-size: 11px;
				font-weight: 700;
				padding: 3px 8px;
				border-radius: 6px;
			}
			.card-desc {
				font-size: 12px;
				color: var(--text-muted, #64748b);
				line-height: 1.5;
				margin-bottom: 14px;
				flex: 1;
			}
			.card-specs-row {
				display: flex;
				justify-content: space-between;
				align-items: center;
				font-size: 12px;
				color: var(--text-muted, #64748b);
				margin-bottom: 16px;
				padding-top: 10px;
				border-top: 1px solid var(--border-color, #f1f5f9);
			}
			.card-buttons-row {
				display: flex;
				gap: 8px;
			}
			.btn-publish-theme {
				flex: 1;
				background: #10b981 !important;
				color: #ffffff !important;
				font-weight: 700 !important;
				border: none !important;
				border-radius: 6px !important;
				padding: 8px 12px !important;
				font-size: 12px !important;
				cursor: pointer;
				transition: opacity 0.15s;
			}
			.btn-publish-theme:hover {
				opacity: 0.9;
			}
			.btn-card-customize {
				background: var(--btn-default-bg, #f1f5f9) !important;
				color: var(--text-color, #1e293b) !important;
				border: 1px solid var(--border-color, #cbd5e1) !important;
				border-radius: 6px !important;
				padding: 8px 12px !important;
				font-size: 12px !important;
				font-weight: 600 !important;
				cursor: pointer;
			}
		`;
		const style = document.createElement("style");
		style.id = style_id;
		style.innerHTML = css;
		document.head.appendChild(style);
	}

	const $wrapper = frm.fields_dict.theme_dashboard_html?.$wrapper;
	if (!$wrapper || !$wrapper.length) return;

	frappe.call({
		method: "ecommerce_store.ecommerce_store.doctype.store_theme.store_theme.get_theme_library",
		callback: function (r) {
			const themes = r.message || [];
			render_dashboard_html(frm, $wrapper, themes);
		}
	});
}

function render_dashboard_html(frm, $wrapper, themes) {
	const active_name = frm.doc.active_theme_name || "Modern Flagship";
	const active_theme = themes.find(t => t.theme_name === active_name) || themes[0] || {};

	const p_color = frm.doc.primary_color || active_theme.primary_color || "#0284c7";
	const s_color = frm.doc.secondary_color || active_theme.secondary_color || "#0f172a";
	const a_color = frm.doc.accent_color || active_theme.accent_color || "#f59e0b";
	const bg_color = frm.doc.bg_color || active_theme.bg_color || "#ffffff";
	const font_h = frm.doc.font_heading || active_theme.font_heading || "Plus Jakarta Sans";
	const font_b = frm.doc.font_body || active_theme.font_body || "Inter";

	const html = $(`
		<div class="theme-manager-container">
			<!-- 1. Top Action Bar -->
			<div class="theme-top-actions">
				<div class="theme-header-titles">
					<h2>Store Themes & Deployment</h2>
					<p>Choose an official store template, customize visual styling, or deploy directly from a GitHub repository.</p>
				</div>
				<div class="theme-header-btns">
					<button type="button" class="btn-github-deploy" id="btn-deploy-github">
						<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
							<path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
						</svg>
						Deploy from GitHub
					</button>
					<button type="button" class="btn-view-store" id="btn-view-live-store">
						<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
						View Store
					</button>
				</div>
			</div>

			<!-- 2. Current Published Theme Card -->
			<div class="active-theme-card">
				<div class="active-theme-top">
					<div class="active-theme-info">
						<h3>
							<span>${frappe.utils.escape_html(active_name)}</span>
							<span class="badge-published">✓ Current Theme</span>
						</h3>
						<div class="active-theme-sub">This theme is live on your customer storefront. Visitors see this layout and color scheme.</div>
					</div>
					<div class="active-theme-actions">
						<button type="button" class="btn-customize-active" id="btn-scroll-to-customizer">
							🎨 Customize Theme
						</button>
						<button type="button" class="btn-duplicate-active" id="btn-duplicate-active">
							Duplicate
						</button>
					</div>
				</div>

				<div class="active-theme-preview-box">
					<div class="mini-mockup-frame">
						<div class="mockup-header-bar">
							<span class="mockup-dot red"></span>
							<span class="mockup-dot yellow"></span>
							<span class="mockup-dot green"></span>
						</div>
						<div class="mockup-body" style="--mockup-bg: ${bg_color};">
							<div class="mockup-nav" style="background: ${s_color}; opacity: 0.85;"></div>
							<div class="mockup-hero" style="background: ${p_color}; font-family: '${font_h}';">
								Live Storefront Banner
							</div>
							<div class="mockup-cards">
								<div class="mockup-card-item" style="border-top: 3px solid ${a_color};"></div>
								<div class="mockup-card-item" style="border-top: 3px solid ${a_color};"></div>
								<div class="mockup-card-item" style="border-top: 3px solid ${a_color};"></div>
							</div>
						</div>
					</div>

					<div class="active-theme-details">
						<div class="theme-meta-row">
							<div class="theme-meta-pill">
								<span>Active Colors</span>
								<div class="swatch-group">
									<span class="color-circle" style="background: ${p_color};" title="Primary: ${p_color}"></span>
									<span class="color-circle" style="background: ${s_color};" title="Secondary: ${s_color}"></span>
									<span class="color-circle" style="background: ${a_color};" title="Accent: ${a_color}"></span>
								</div>
							</div>
							<div class="theme-meta-pill">
								<span>Typography</span>
								<strong>${font_h} / ${font_b}</strong>
							</div>
							<div class="theme-meta-pill">
								<span>Header Style</span>
								<strong>${frm.doc.header_style || "Minimal Top Bar"}</strong>
							</div>
							<div class="theme-meta-pill">
								<span>Cart Experience</span>
								<strong>${frm.doc.cart_type || "Slide-out Drawer Cart"}</strong>
							</div>
						</div>
					</div>
				</div>
			</div>

			<!-- 3. Theme Library -->
			<div class="library-section">
				<div class="library-header">
					<div>
						<h4>Official Theme Library</h4>
						<p>Select from ready-made, high-converting templates or switch instantly with one click.</p>
					</div>
				</div>

				<div class="filter-pills-bar">
					<span class="filter-pill active" data-cat="all">All Templates (${themes.length})</span>
					<span class="filter-pill" data-cat="General & Multipurpose">General & Retail</span>
					<span class="filter-pill" data-cat="Electronics & Tech">Electronics & Tech</span>
					<span class="filter-pill" data-cat="Fashion & Apparel">Fashion & Apparel</span>
					<span class="filter-pill" data-cat="Grocery & Food">Grocery & Organic</span>
				</div>

				<div class="themes-grid" id="themes-grid-container"></div>
			</div>
		</div>
	`);

	// Render Library Grid
	const $grid = html.find("#themes-grid-container");
	themes.forEach(theme => {
		const is_this_active = theme.theme_name === active_name;
		const $card = $(`
			<div class="theme-template-card" data-category="${frappe.utils.escape_html(theme.category)}">
				<div class="card-mockup-area">
					<div class="mini-mockup-frame">
						<div class="mockup-header-bar">
							<span class="mockup-dot red"></span>
							<span class="mockup-dot yellow"></span>
							<span class="mockup-dot green"></span>
						</div>
						<div class="mockup-body" style="--mockup-bg: ${theme.bg_color || '#ffffff'};">
							<div class="mockup-nav" style="background: ${theme.secondary_color || '#0f172a'};"></div>
							<div class="mockup-hero" style="background: ${theme.primary_color || '#0284c7'}; font-family: '${theme.font_heading || 'Inter'}';">
								${frappe.utils.escape_html(theme.theme_name)}
							</div>
							<div class="mockup-cards">
								<div class="mockup-card-item" style="border-top: 2px solid ${theme.accent_color || '#f59e0b'};"></div>
								<div class="mockup-card-item" style="border-top: 2px solid ${theme.accent_color || '#f59e0b'};"></div>
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

					<p class="card-desc">${frappe.utils.escape_html(theme.description || "Production-ready ecommerce template.")}</p>

					<div class="card-specs-row">
						<div>
							<span class="color-circle" style="background: ${theme.primary_color}; width: 14px; height: 14px; margin-right: 3px;"></span>
							<span class="color-circle" style="background: ${theme.accent_color}; width: 14px; height: 14px;"></span>
						</div>
						<div>${theme.font_heading || "Inter"}</div>
					</div>

					<div class="card-buttons-row">
						${is_this_active ? `
							<button type="button" class="btn-publish-theme" style="background: #94a3b8 !important; cursor: default;" disabled>
								✓ Live Active
							</button>
						` : `
							<button type="button" class="btn-publish-theme" data-publish="${frappe.utils.escape_html(theme.theme_name)}">
								Publish Template
							</button>
						`}
						<button type="button" class="btn-card-customize" data-customize="${frappe.utils.escape_html(theme.theme_name)}">
							Customize
						</button>
					</div>
				</div>
			</div>
		`);

		// Publish click
		$card.find("[data-publish]").on("click", function () {
			const target_name = $(this).attr("data-publish");
			frappe.confirm(`Publish '${target_name}' as your active website template?`, function () {
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

		// Customize click
		$card.find("[data-customize]").on("click", function () {
			apply_template_to_customizer(frm, theme);
		});

		$grid.append($card);
	});

	// Filter tabs
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

	// Deploy from GitHub button
	html.find("#btn-deploy-github").on("click", function () {
		open_github_deploy_modal(frm);
	});

	// View store button
	html.find("#btn-view-live-store").on("click", function () {
		window.open("/", "_blank");
	});

	// Scroll to customizer button
	html.find("#btn-scroll-to-customizer").on("click", function () {
		const target = $('[data-fieldname="sec_brand"]').length ? $('[data-fieldname="sec_brand"]') : $('[data-fieldname="sec_colors"]');
		if (target.length) {
			$('html, body').animate({ scrollTop: target.offset().top - 80 }, 400);
		}
	});

	// Duplicate active button
	html.find("#btn-duplicate-active").on("click", function () {
		frappe.prompt(
			[{ fieldname: "new_name", fieldtype: "Data", label: "New Template Name", reqd: 1, default: `${active_name} Custom` }],
			function (values) {
				frappe.call({
					method: "ecommerce_store.ecommerce_store.doctype.store_theme.store_theme.duplicate_theme",
					args: { theme_name: active_name, new_name: values.new_name },
					freeze: true,
					freeze_message: "Duplicating template...",
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

function open_github_deploy_modal(frm) {
	const d = new frappe.ui.Dialog({
		title: __("Deploy Theme from GitHub"),
		fields: [
			{
				fieldname: "repo_url",
				fieldtype: "Data",
				label: __("GitHub Repository URL"),
				reqd: 1,
				placeholder: "https://github.com/username/my-frappe-theme.git",
				description: __("Public or private repository with theme layout and styling")
			},
			{
				fieldname: "branch",
				fieldtype: "Data",
				label: __("Git Branch"),
				default: "main"
			},
			{
				fieldname: "theme_name",
				fieldtype: "Data",
				label: __("Theme Name (Optional)"),
				placeholder: "e.g. My Custom Brand Theme"
			},
			{
				fieldname: "publish_now",
				fieldtype: "Check",
				label: __("Publish and activate this theme immediately"),
				default: 1
			}
		],
		primary_action_label: __("Deploy Theme"),
		primary_action(values) {
			frappe.call({
				method: "ecommerce_store.ecommerce_store.doctype.store_theme.store_theme.deploy_theme_from_github",
				args: values,
				freeze: true,
				freeze_message: __("Cloning repository and deploying theme..."),
				callback(r) {
					if (r.message && r.message.status === "success") {
						frappe.show_alert({ message: r.message.message, indicator: "green" });
						d.hide();
						frm.reload_doc();
					}
				}
			});
		}
	});

	d.show();
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

	const target = $('[data-fieldname="sec_colors"]').length ? $('[data-fieldname="sec_colors"]') : $('[data-fieldname="sec_brand"]');
	if (target.length) {
		$('html, body').animate({ scrollTop: target.offset().top - 80 }, 400);
	}
}
