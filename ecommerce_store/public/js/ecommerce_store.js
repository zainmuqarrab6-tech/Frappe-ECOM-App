// Copyright (c) 2026, Zain and contributors
// Shopify-style Left Sidebar Hierarchy and Sub-menus

(function () {
	let isNestingSubmenu = false;

	const SUB_ITEMS = [
		{ name: "Collections", route: "product-category" },
		{ name: "Inventory", route: "stock-adjustment" },
		{ name: "Purchase orders", route: "store-purchase-order" },
		{ name: "Transfers", route: "store-inventory-transfer" },
		{ name: "Gift cards", route: "store-gift-card" }
	];

	function setupShopifyProductSubmenu() {
		if (isNestingSubmenu) return;
		const $sidebar = $(".body-sidebar .sidebar-items");
		if (!$sidebar.length) return;

		const $productItem = $sidebar.find('.sidebar-item-container[item-name="Products"]');
		if (!$productItem.length) return;

		isNestingSubmenu = true;

		// 1. Ensure nested sub-container exists inside Products item
		let $nested = $productItem.find('> .shopify-product-subitems');
		if (!$nested.length) {
			$nested = $('<div class="sidebar-child-item nested-container shopify-product-subitems"></div>');
			$productItem.append($nested);
		}

		// 2. Add chevron toggle button to Products item if not already present
		const $anchor = $productItem.find('> .standard-sidebar-item > .item-anchor');
		if ($anchor.length && !$productItem.find('.shopify-product-chevron').length) {
			const $chevron = $(`
				<button type="button" class="btn-reset shopify-product-chevron" title="Toggle sub-options" aria-label="Toggle sub-options">
					<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
						<polyline points="6 9 12 15 18 9"></polyline>
					</svg>
				</button>
			`);

			$chevron.on("click", function (e) {
				e.preventDefault();
				e.stopPropagation();
				$nested.toggleClass("collapsed");
				$chevron.toggleClass("collapsed");
			});

			$anchor.append($chevron);
		}

		// 3. Move each sub-item physically inside the Products nested container
		SUB_ITEMS.forEach(sub => {
			const $subItem = $sidebar.find(`.sidebar-item-container[item-name="${sub.name}"]`);
			if ($subItem.length && !$nested.has($subItem).length) {
				$nested.append($subItem);
			}
		});

		// 4. Determine current active route state
		const currentPath = (window.location.pathname || "").toLowerCase() + (window.location.hash || "").toLowerCase();
		const currentRoute = (frappe.get_route_str ? frappe.get_route_str() : "").toLowerCase();
		const fullRoute = currentPath + " " + currentRoute;

		const isProductActive = fullRoute.includes("/product") || fullRoute.includes("product");
		let isAnySubActive = false;

		SUB_ITEMS.forEach(sub => {
			const $subItem = $nested.find(`.sidebar-item-container[item-name="${sub.name}"]`);
			const isThisSubActive = fullRoute.includes(sub.route) || fullRoute.includes(sub.name.toLowerCase().replace(/ /g, "-"));
			if (isThisSubActive) {
				isAnySubActive = true;
				$subItem.addClass("active-subitem");
			} else {
				$subItem.removeClass("active-subitem");
			}
		});

		const $chevron = $productItem.find(".shopify-product-chevron");
		if (isProductActive || isAnySubActive) {
			// Expand submenu when on any product or sub-option page
			$nested.removeClass("collapsed");
			$chevron.removeClass("collapsed");
			if (!isAnySubActive && isProductActive) {
				$productItem.addClass("shopify-parent-active");
			} else {
				$productItem.removeClass("shopify-parent-active");
			}
		}

		isNestingSubmenu = false;
	}

	function pinSettingsAtEnd() {
		// 1. Sidebar: Ensure Settings item is placed at the very end of .sidebar-items
		const $sidebarItems = $(".body-sidebar .sidebar-items");
		const $settingsItem = $sidebarItems.find('.sidebar-item-container[item-name="Settings"]');
		if ($settingsItem.length) {
			$sidebarItems.append($settingsItem);
			$settingsItem.css({
				"margin-top": "auto",
				"padding-top": "10px",
				"border-top": "1px solid var(--outline-gray-1, rgba(255, 255, 255, 0.08))",
				"margin-bottom": "6px"
			});
		}

		// 2. Dock: Ensure Settings gear button is at the end of the dock icons (above user avatar)
		const $dock = $("#desk-dock");
		if ($dock.length && !$dock.find(".dock-item-settings-bottom").length) {
			const $user = $dock.find(".dock-user");
			const $dockSettings = $(`
				<button class="dock-item dock-item-settings-bottom" aria-label="Settings" title="Settings">
					<span class="dock-item-icon">
						<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
							<circle cx="12" cy="12" r="3"></circle>
							<path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
						</svg>
					</span>
					<span class="dock-item-label">Settings</span>
				</button>
			`);

			$dockSettings.on("click", function () {
				frappe.set_route("Form", "Store Settings");
			});

			if ($user.length) {
				$dockSettings.insertBefore($user);
			} else {
				$dock.append($dockSettings);
			}
		}
	}

	function runAllSidebarEnhancements() {
		setupShopifyProductSubmenu();
		pinSettingsAtEnd();
	}

	$(document).ready(function () {
		setTimeout(runAllSidebarEnhancements, 200);
		setTimeout(runAllSidebarEnhancements, 800);
		setTimeout(runAllSidebarEnhancements, 1800);
	});

	$(document).on("sidebar_setup", function () {
		setTimeout(runAllSidebarEnhancements, 100);
	});

	if (window.frappe && frappe.router) {
		frappe.router.on("change", function () {
			setTimeout(runAllSidebarEnhancements, 150);
		});
	}

	// Observe sidebar mutations so any dynamic re-rendering automatically nests sub-items
	const observer = new MutationObserver(function (mutations) {
		if (isNestingSubmenu) return;
		for (const m of mutations) {
			if (m.addedNodes.length > 0) {
				setTimeout(runAllSidebarEnhancements, 50);
				break;
			}
		}
	});

	function attachObserver() {
		const target = document.querySelector(".body-sidebar .sidebar-items");
		if (target) {
			observer.observe(target, { childList: true });
		} else {
			setTimeout(attachObserver, 500);
		}
	}
	attachObserver();
})();
