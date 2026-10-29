import frappe
from frappe.utils import today

def verify_all():
    print("=== STARTING BACKEND OPERATIONS VERIFICATION ===")

    # 1. Product check
    prod_name = frappe.db.get_value("Product", {"is_active": 1}, "name")
    if not prod_name:
        raise Exception("No active product found for testing.")

    prod = frappe.get_doc("Product", prod_name)
    initial_stock = prod.stock_quantity or 0
    print(f"Test Product: {prod.title} ({prod.name}) | Initial Stock: {initial_stock}")

    # 2. Test Stock Adjustment (Restock +10)
    print("\n--- Testing Stock Adjustment (Add Stock +10) ---")
    stk_adj = frappe.get_doc({
        "doctype": "Stock Adjustment",
        "adjustment_date": today(),
        "reason": "New Supplier Delivery / Restock",
        "reference_note": "PO-TEST-9988",
        "items": [
            {
                "product": prod.name,
                "action_type": "Add Stock (Restock)",
                "quantity": 10
            }
        ]
    })
    stk_adj.insert()
    stk_adj.submit()
    
    prod.reload()
    print(f"Stock after +10 Restock: {prod.stock_quantity} (Expected: {initial_stock + 10})")
    assert prod.stock_quantity == initial_stock + 10, "Stock restock calculation failed!"
    print("[PASS] Stock Adjustment Restock successful!")

    # 3. Test Stock Adjustment Cancellation (Revert +10)
    print("\n--- Testing Stock Adjustment Cancellation ---")
    stk_adj.cancel()
    prod.reload()
    print(f"Stock after Cancellation: {prod.stock_quantity} (Expected: {initial_stock})")
    assert prod.stock_quantity == initial_stock, "Stock adjustment cancel reversion failed!"
    print("[PASS] Stock Adjustment Cancellation reversion successful!")

    # 4. Test Order Creation & Cancellation Restock
    print("\n--- Testing Order Cancellation Auto-Restock ---")
    from ecommerce_store.api.orders import create_order
    res = create_order(
        customer_name="Zain Test Buyer",
        customer_email="zain_test@example.com",
        customer_phone="+923001234567",
        shipping_address="House 42, Street 7, Sector F-8",
        shipping_city="Islamabad",
        payment_method="Cash on Delivery",
        items=[{"product": prod.name, "quantity": 2}]
    )
    assert res.get("status") == "success", f"Order creation failed: {res.get('message')}"
    order_id = res["data"]["order_id"]
    print(f"Created Test Order: {order_id}")

    prod.reload()
    print(f"Stock after Order creation: {prod.stock_quantity} (Expected: {initial_stock - 2})")
    assert prod.stock_quantity == initial_stock - 2, "Stock deduction on order placement failed!"

    # Now cancel the order
    order_doc = frappe.get_doc("Store Order", order_id)
    cancel_res = order_doc.cancel_order(reason="Testing inventory auto-restock mechanism")
    assert cancel_res.get("status") == "success", "Order cancel_order failed!"

    prod.reload()
    print(f"Stock after Order cancellation: {prod.stock_quantity} (Expected: {initial_stock})")
    assert prod.stock_quantity == initial_stock, "Stock restoration on cancellation failed!"
    print("[PASS] Order Cancellation Inventory Auto-Restock successful!")

    # 5. Test Print Formats (Commercial Tax Invoice & Shipping Label)
    print("\n--- Testing Print Formats Rendering ---")
    invoice_html = frappe.get_print("Store Order", order_id, "Commercial Tax Invoice")
    assert "TAX INVOICE" in invoice_html, "Invoice HTML missing header!"
    assert "Zain Test Buyer" in invoice_html, "Invoice HTML missing customer name!"
    print("[PASS] Commercial Tax Invoice (A4) rendered cleanly!")

    label_html = frappe.get_print("Store Order", order_id, "Thermal Courier Shipping Label")
    assert "COURIER SHIPPING" in label_html or "DELIVER TO" in label_html, "Label HTML missing expected headers!"
    assert "ISLAMABAD" in label_html, "Label HTML missing shipping city!"
    print("[PASS] Thermal Courier Shipping Label (4x6) rendered cleanly!")

    print("\n=== ALL BACKEND OPERATIONS TESTS PASSED (100%) ===")

if __name__ == "__main__":
    verify_all()
