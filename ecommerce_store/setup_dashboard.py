import frappe
import json

def setup_shopify_dashboard():
    print("Setting up Shopify-Style Dashboard...")

    # 1. Custom HTML Block
    block_name = "Shopify Store Overview"
    
    html = """
<div class="shopify-dash">
  <!-- Top Welcome Banner -->
  <div class="shopify-header-card">
    <div class="store-meta">
      <div class="store-avatar">🛍️</div>
      <div>
        <div class="store-title-row">
          <h2 class="store-name" id="shp-store-name">ProStore Ecommerce</h2>
          <span class="live-status-pill"><span class="dot"></span> Headless Backend Active</span>
        </div>
        <p class="store-sub">Here's what's happening with your store today.</p>
      </div>
    </div>
    <div class="store-actions">
      <a href="/app/store-order" class="shp-btn shp-btn-outline">📦 View Orders</a>
      <a href="/app/product/new" class="shp-btn shp-btn-primary">+ Add Product</a>
    </div>
  </div>

  <!-- Action Required / To-Do Banner -->
  <div class="shopify-action-banner" id="shp-action-banner">
    <div class="action-icon">📦</div>
    <div class="action-content">
      <strong id="shp-action-title">Orders to Fulfill</strong>
      <p id="shp-action-desc">You have pending orders that need to be packaged and shipped.</p>
    </div>
    <a href="/app/store-order?order_status=Pending" class="shp-btn shp-btn-sm shp-btn-warning" id="shp-action-btn">Fulfill Orders</a>
  </div>

  <!-- KPI Metrics Grid -->
  <div class="shp-metrics-grid">
    <div class="shp-metric-card">
      <div class="metric-top">
        <span class="metric-label">Total Sales</span>
        <span class="metric-icon">💰</span>
      </div>
      <div class="metric-value" id="shp-total-sales">Rs. 0.00</div>
      <div class="metric-sub text-success">↑ Live verified sales</div>
    </div>

    <div class="shp-metric-card">
      <div class="metric-top">
        <span class="metric-label">Total Orders</span>
        <span class="metric-icon">🛍️</span>
      </div>
      <div class="metric-value" id="shp-total-orders">0</div>
      <div class="metric-sub text-muted">All-time customer orders</div>
    </div>

    <div class="shp-metric-card highlight-card">
      <div class="metric-top">
        <span class="metric-label">To Fulfill</span>
        <span class="metric-icon">⏳</span>
      </div>
      <div class="metric-value text-warning" id="shp-pending-orders">0</div>
      <div class="metric-sub text-warning font-weight-bold">Awaiting shipment</div>
    </div>

    <div class="shp-metric-card">
      <div class="metric-top">
        <span class="metric-label">Active Products</span>
        <span class="metric-icon">📦</span>
      </div>
      <div class="metric-value" id="shp-active-products">0</div>
      <div class="metric-sub text-muted">In active catalog</div>
    </div>

    <div class="shp-metric-card">
      <div class="metric-top">
        <span class="metric-label">Total Customers</span>
        <span class="metric-icon">👥</span>
      </div>
      <div class="metric-value" id="shp-total-customers">0</div>
      <div class="metric-sub text-muted">Registered accounts</div>
    </div>
  </div>

  <!-- Quick Navigation Tiles -->
  <div class="shp-nav-row">
    <a href="/app/store-order" class="shp-nav-tile">
      <div class="tile-icon">🛒</div>
      <div class="tile-info">
        <div class="tile-title">Orders</div>
        <div class="tile-sub">Manage & Track</div>
      </div>
    </a>
    <a href="/app/product" class="shp-nav-tile">
      <div class="tile-icon">🏷️</div>
      <div class="tile-info">
        <div class="tile-title">Products</div>
        <div class="tile-sub">Catalog & Variants</div>
      </div>
    </a>
    <a href="/app/store-customer" class="shp-nav-tile">
      <div class="tile-icon">👥</div>
      <div class="tile-info">
        <div class="tile-title">Customers</div>
        <div class="tile-sub">Buyers & Profiles</div>
      </div>
    </a>
    <a href="/app/store-banner" class="shp-nav-tile">
      <div class="tile-icon">🖼️</div>
      <div class="tile-info">
        <div class="tile-title">Hero Banners</div>
        <div class="tile-sub">Sliders & Promos</div>
      </div>
    </a>
    <a href="/app/store-coupon" class="shp-nav-tile">
      <div class="tile-icon">🎟️</div>
      <div class="tile-info">
        <div class="tile-title">Discounts</div>
        <div class="tile-sub">Coupons & Deals</div>
      </div>
    </a>
    <a href="/app/store-settings" class="shp-nav-tile">
      <div class="tile-icon">⚙️</div>
      <div class="tile-info">
        <div class="tile-title">Settings</div>
        <div class="tile-sub">Delivery & Policies</div>
      </div>
    </a>
  </div>
</div>
"""

    css = """
.shopify-dash {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  color: #202223;
  padding: 8px 0;
}

.shopify-header-card {
  background: linear-gradient(135deg, #ffffff 0%, #f6f8fa 100%);
  border: 1px solid #dce0e5;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.03);
  margin-bottom: 20px;
}

.store-meta {
  display: flex;
  align-items: center;
  gap: 16px;
}

.store-avatar {
  font-size: 32px;
  background: #f1f3f5;
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  border: 1px solid #e1e4e8;
}

.store-title-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.store-name {
  font-size: 22px;
  font-weight: 700;
  margin: 0;
  color: #1a1c1d;
  letter-spacing: -0.3px;
}

.live-status-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 600;
  background: #e3f8eb;
  color: #0b6b34;
  padding: 4px 10px;
  border-radius: 20px;
}

.live-status-pill .dot {
  width: 8px;
  height: 8px;
  background: #10b981;
  border-radius: 50%;
  box-shadow: 0 0 6px rgba(16, 185, 129, 0.6);
}

.store-sub {
  font-size: 14px;
  color: #6d7175;
  margin: 4px 0 0 0;
}

.store-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.shp-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 600;
  border-radius: 8px;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.15s ease;
}

.shp-btn:hover {
  text-decoration: none;
  transform: translateY(-1px);
}

.shp-btn-primary {
  background: #008060;
  color: #ffffff !important;
  border: 1px solid #008060;
  box-shadow: 0 1px 3px rgba(0, 128, 96, 0.2);
}

.shp-btn-primary:hover {
  background: #006e52;
}

.shp-btn-outline {
  background: #ffffff;
  color: #202223 !important;
  border: 1px solid #c9cccf;
}

.shp-btn-outline:hover {
  background: #f6f6f7;
  border-color: #babfc3;
}

.shp-btn-warning {
  background: #ffc96b;
  color: #4a2c00 !important;
  border: 1px solid #f2b44b;
}

.shp-btn-warning:hover {
  background: #f7be54;
}

.shp-btn-sm {
  padding: 6px 12px;
  font-size: 12px;
}

.shopify-action-banner {
  background: #fff8e6;
  border: 1px solid #ffe199;
  border-left: 5px solid #d97706;
  border-radius: 10px;
  padding: 16px 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.02);
}

.action-icon {
  font-size: 26px;
}

.action-content {
  flex: 1;
}

.action-content strong {
  display: block;
  font-size: 14px;
  color: #78350f;
  margin-bottom: 2px;
}

.action-content p {
  margin: 0;
  font-size: 13px;
  color: #92400e;
}

.shp-metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.shp-metric-card {
  background: #ffffff;
  border: 1px solid #e1e3e5;
  border-radius: 12px;
  padding: 18px 20px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.02);
  transition: all 0.2s ease;
}

.shp-metric-card:hover {
  border-color: #c9cccf;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.shp-metric-card.highlight-card {
  border-color: #ffd699;
  background: #fffdf8;
}

.metric-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.metric-label {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #6d7175;
}

.metric-icon {
  font-size: 16px;
}

.metric-value {
  font-size: 24px;
  font-weight: 700;
  color: #202223;
  margin-bottom: 4px;
  letter-spacing: -0.5px;
}

.metric-sub {
  font-size: 12px;
}

.text-success { color: #008060; }
.text-warning { color: #b45309; }
.text-muted { color: #8c9196; }

.shp-nav-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 12px;
  margin-bottom: 20px;
}

.shp-nav-tile {
  background: #ffffff;
  border: 1px solid #e1e3e5;
  border-radius: 10px;
  padding: 14px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: #202223 !important;
  transition: all 0.15s ease;
}

.shp-nav-tile:hover {
  border-color: #008060;
  background: #f6fcf8;
  transform: translateY(-2px);
  text-decoration: none;
}

.tile-icon {
  font-size: 22px;
}

.tile-title {
  font-size: 13px;
  font-weight: 600;
  color: #202223;
}

.tile-sub {
  font-size: 11px;
  color: #8c9196;
}
"""

    js = """
frappe.call({
    method: "ecommerce_store.api.store.get_shopify_dashboard_data",
    callback: function(r) {
        if (r.message && r.message.status === "success") {
            let d = r.message.data;
            if (root_element) {
                let nameEl = root_element.querySelector("#shp-store-name");
                if (nameEl) nameEl.textContent = d.store_name;

                let salesEl = root_element.querySelector("#shp-total-sales");
                if (salesEl) salesEl.textContent = d.currency_symbol + " " + d.total_sales.toLocaleString('en-US', {minimumFractionDigits: 2});

                let ordersEl = root_element.querySelector("#shp-total-orders");
                if (ordersEl) ordersEl.textContent = d.total_orders;

                let pendingEl = root_element.querySelector("#shp-pending-orders");
                if (pendingEl) pendingEl.textContent = d.pending_orders;

                let prodEl = root_element.querySelector("#shp-active-products");
                if (prodEl) prodEl.textContent = d.active_products;

                let custEl = root_element.querySelector("#shp-total-customers");
                if (custEl) custEl.textContent = d.total_customers;

                let banner = root_element.querySelector("#shp-action-banner");
                if (banner) {
                    if (d.pending_orders > 0) {
                        banner.style.display = "flex";
                        root_element.querySelector("#shp-action-title").textContent = d.pending_orders + " Orders Need Fulfillment";
                        root_element.querySelector("#shp-action-desc").textContent = "You have " + d.pending_orders + " pending customer order(s) awaiting courier shipment.";
                    } else if (d.low_stock_products > 0) {
                        banner.style.display = "flex";
                        root_element.querySelector("#shp-action-title").textContent = d.low_stock_products + " Products Low on Stock";
                        root_element.querySelector("#shp-action-desc").textContent = "Inventory for some items has reached the reorder threshold.";
                        root_element.querySelector("#shp-action-btn").href = "/app/product?stock_quantity=<=5";
                        root_element.querySelector("#shp-action-btn").textContent = "Restock Items";
                    } else {
                        banner.style.display = "none";
                    }
                }
            }
        }
    }
});
"""

    if not frappe.db.exists("Custom HTML Block", block_name):
        doc = frappe.get_doc({
            "doctype": "Custom HTML Block",
            "name": block_name,
            "html": html,
            "style": css,
            "script": js
        })
        doc.insert(ignore_permissions=True)
        print("Created Custom HTML Block: Shopify Store Overview")
    else:
        doc = frappe.get_doc("Custom HTML Block", block_name)
        doc.html = html
        doc.style = css
        doc.script = js
        doc.save(ignore_permissions=True)
        print("Updated Custom HTML Block: Shopify Store Overview")

    # 2. Update Workspace
    ws_content = [
        # 1. Custom Shopify Block at Top
        {"type": "custom_block", "data": {"custom_block_name": block_name, "col": 12}},

        {"type": "spacer", "data": {"col": 12}},

        # 2. Sales Analytics Charts
        {"type": "header", "data": {"text": "<span class='h4 font-weight-bold'>📈 Analytics & Trends</span>", "col": 12}},
        {"type": "chart", "data": {"chart_name": "Daily Sales Trend", "col": 7}},
        {"type": "chart", "data": {"chart_name": "Orders by Status", "col": 5}},

        {"type": "spacer", "data": {"col": 12}},

        # 3. Modules
        {"type": "header", "data": {"text": "<span class='h4 font-weight-bold'>📂 Management Modules</span>", "col": 12}},
        {"type": "card", "data": {"card_name": "Catalog Management", "col": 4}},
        {"type": "card", "data": {"card_name": "Sales & Orders", "col": 4}},
        {"type": "card", "data": {"card_name": "Customer & Marketing", "col": 4}}
    ]

    ws_doc = frappe.get_doc("Workspace", "Ecommerce Store")
    ws_doc.type = "Workspace"
    ws_doc.content = json.dumps(ws_content)
    ws_doc.set("custom_blocks", [{"custom_block_name": block_name}])
    ws_doc.set("charts", [
        {"chart_name": "Orders by Status"},
        {"chart_name": "Daily Sales Trend"}
    ])

    # Clean up storefront shortcuts & links
    ws_doc.shortcuts = [s for s in ws_doc.shortcuts if s.label not in ("Visit Live Store", "Store Customizer")]
    ws_doc.links = [l for l in ws_doc.links if l.label != "Storefront Customizer"]

    ws_doc.save(ignore_permissions=True)
    frappe.db.commit()
    print("Workspace updated with Shopify Store Overview successfully!")

if __name__ == "__main__":
    setup_shopify_dashboard()
