// Copyright (c) 2026, Zain and contributors
// Shopify-style Left Sidebar Hierarchy and Clean Navigation

(function () {
	let isNestingSubmenu = false;
	let isPinningSettings = false;

	const SUB_ITEMS = [
		{ name: "Collections", route: "product-category" },
		{ name: "Inventory", route: "stock-adjustment" },
		{ name: "Purchase orders", route: "store-purchase-order" },
		{ name: "Transfers", route: "store-inventory-transfer" },
		{ name: "Gift cards", route: "store-gift-card" }
	];

	function findSidebarItem(label) {
		let $el = $(`.body-sidebar .sidebar-items .sidebar-item-container[item-name="${label}"]`);
		if ($el.length) return $el;
		$el = $(`.body-sidebar .sidebar-items .sidebar-item-container[data-id="${label}"]`);
		if ($el.length) return $el;
		$el = $(`.body-sidebar .body-sidebar-bottom .sidebar-item-container[item-name="${label}"]`);
		if ($el.length) return $el;
		$(`.body-sidebar .sidebar-item-container`).each(function () {
			if ($(this).find(".sidebar-item-label").first().text().trim() === label) {
				$el = $(this);
				return false;
			}
		});
		return $el;
	}

	function removeDockSettings() {
		const $dock = $("#desk-dock, .dock");
		if (!$dock.length) return;

		$dock.find(".dock-item-settings-bottom").remove();

		$dock.find(".dock-item, button, a").each(function () {
			const $btn = $(this);
			if ($btn.hasClass("dock-user-button") || $btn.closest(".dock-user").length) return;
			if ($btn.closest(".dock-logo").length) return;

			const label = (
				$btn.attr("aria-label") ||
				$btn.attr("title") ||
				$btn.attr("data-id") ||
				$btn.attr("data-name") ||
				$btn.text() ||
				""
			).trim().toLowerCase();

			if (label.includes("setting")) {
				$btn.remove();
				return;
			}

			if (
				$btn.find("svg.icon-settings, [data-icon*='setting'], [item-icon*='setting']").length ||
				$btn.find("use[href*='setting'], svg [href*='setting']").length ||
				$btn.find("svg path[d*='19.4 15']").length
			) {
				$btn.remove();
			}
		});
	}

	function setupShopifyProductSubmenu() {
		if (isNestingSubmenu) return;
		const $sidebar = $(".body-sidebar .sidebar-items");
		if (!$sidebar.length) return;

		const $productItem = findSidebarItem("Products");
		if (!$productItem || !$productItem.length) return;

		isNestingSubmenu = true;

		// 1. Ensure sub-container exists inside Products item
		let $nested = $productItem.find("> .shopify-product-subitems");
		if (!$nested.length) {
			$nested = $('<div class="sidebar-child-item nested-container shopify-product-subitems"></div>');
			$productItem.append($nested);
		}

		// 2. Add chevron toggle button to Products item if not already present
		const $anchor = $productItem.find("> .standard-sidebar-item > .item-anchor");
		if ($anchor.length && !$productItem.find(".shopify-product-chevron").length) {
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
			const $subItem = findSidebarItem(sub.name);
			if ($subItem && $subItem.length && !$nested.has($subItem).length) {
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
			const $subItem = $nested.find(`.sidebar-item-container[item-name="${sub.name}"], .sidebar-item-container[data-id="${sub.name}"]`);
			const isThisSubActive = fullRoute.includes(sub.route) || fullRoute.includes(sub.name.toLowerCase().replace(/ /g, "-"));
			if (isThisSubActive) {
				isAnySubActive = true;
				$subItem.addClass("active-subitem");
			} else {
				$subItem.removeClass("active-subitem");
			}
		});

		// Active styling for Products parent pill
		if (isProductActive && !isAnySubActive) {
			$productItem.addClass("shopify-parent-active");
		} else {
			$productItem.removeClass("shopify-parent-active");
		}

		isNestingSubmenu = false;
	}

	function pinSettingsAtEnd() {
		if (isPinningSettings) return;
		isPinningSettings = true;
		try {
			// 1. Proactively remove left dock gear buttons
			removeDockSettings();

			// 2. Locate Settings in sidebar
			let $settingsItem = findSidebarItem("Settings");
			if (!$settingsItem || !$settingsItem.length) {
				$settingsItem = $(".body-sidebar .sidebar-item-container[item-name='Settings']");
			}
			if (!$settingsItem || !$settingsItem.length) {
				$settingsItem = $(".body-sidebar .sidebar-item-container:has([href*='Store%20Settings'], [href*='store-settings'])");
			}

			if ($settingsItem && $settingsItem.length) {
				const $sidebarBottom = $(".body-sidebar .body-sidebar-bottom");
				if ($sidebarBottom.length) {
					// Move to bottom container so it sits at the absolute bottom of the panel
					if (!$sidebarBottom.children(".sidebar-item-container[item-name='Settings']").length) {
						$sidebarBottom.append($settingsItem);
					}
				} else {
					// Fallback: append to the end of sidebar-items
					const $sidebarItems = $(".body-sidebar .sidebar-items");
					if (!$sidebarItems.has($settingsItem).length) {
						$sidebarItems.append($settingsItem);
					}
				}

				$settingsItem.addClass("shopify-pinned-settings");
			}
		} finally {
			isPinningSettings = false;
		}
	}

	function runAllSidebarEnhancements() {
		removeDockSettings();
		setupShopifyProductSubmenu();
		pinSettingsAtEnd();
	}

	removeDockSettings();

	$(document).ready(function () {
		removeDockSettings();
		setTimeout(runAllSidebarEnhancements, 20);
		setTimeout(runAllSidebarEnhancements, 100);
		setTimeout(runAllSidebarEnhancements, 300);
		setTimeout(runAllSidebarEnhancements, 700);
		setTimeout(runAllSidebarEnhancements, 1500);
	});

	$(document).on("sidebar_setup", function () {
		setTimeout(runAllSidebarEnhancements, 30);
	});

	if (window.frappe && frappe.router) {
		frappe.router.on("change", function () {
			setTimeout(runAllSidebarEnhancements, 50);
		});
	}

	// Observer on sidebar
	const observer = new MutationObserver(function (mutations) {
		if (isNestingSubmenu || isPinningSettings) return;
		for (const m of mutations) {
			if (m.addedNodes.length > 0) {
				setTimeout(runAllSidebarEnhancements, 40);
				break;
			}
		}
	});

	function attachObserver() {
		const target = document.querySelector(".body-sidebar");
		if (target) {
			observer.observe(target, { childList: true, subtree: true });
		} else {
			setTimeout(attachObserver, 300);
		}

		function attachDockObserver() {
			const dockTarget = document.getElementById("desk-dock") || document.querySelector(".dock");
			if (dockTarget) {
				const dockObserver = new MutationObserver(function () {
					removeDockSettings();
				});
				dockObserver.observe(dockTarget, { childList: true, subtree: true });
				removeDockSettings();
			} else {
				setTimeout(attachDockObserver, 300);
			}
		}
		attachDockObserver();
	}
	attachObserver();
})();
