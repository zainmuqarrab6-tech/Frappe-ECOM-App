# Ecommerce Store - Headless Frappe Application Hooks

app_name = "ecommerce_store"
app_title = "Ecommerce Store"
app_publisher = "Zain"
app_description = "Headless E-Commerce Backend for Frappe"
app_email = "zain@example.com"
app_license = "mit"

# Application entry point in Desk apps screen
add_to_apps_screen = [
	{
		"name": "ecommerce_store",
		"logo": "/assets/frappe/images/frappe-framework-logo.svg",
		"title": "Ecommerce Store",
		"route": "/desk/ecommerce-store",
	}
]

# Desk assets inclusion
app_include_css = "/assets/ecommerce_store/css/ecommerce_store.css?v=2026111905"
app_include_js = "/assets/ecommerce_store/js/ecommerce_store.js?v=2026111905"

# Headless mode: default web home page directs to Desk login
home_page = "login"
