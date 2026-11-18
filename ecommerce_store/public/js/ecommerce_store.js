// Copyright (c) 2026, Zain and contributors
// Pinned Settings at the end of the left side panel (Shopify style)

(function () {
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

	$(document).ready(function () {
		setTimeout(pinSettingsAtEnd, 200);
		setTimeout(pinSettingsAtEnd, 800);
	});

	$(document).on("sidebar_setup", function () {
		setTimeout(pinSettingsAtEnd, 150);
	});

	if (window.frappe && frappe.router) {
		frappe.router.on("change", function () {
			setTimeout(pinSettingsAtEnd, 200);
		});
	}
})();
