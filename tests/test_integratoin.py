"""
Integration Tests for IMS Inventory Management System
Purpose: Tests complete workflows across multiple operations.
Can run with: pytest tests/test_integration.py -v
"""
class TestIntegration:

    # T001: full product lifecycle integration test.
    # Scenario: Add category -> add supplier -> add product -> sell units -> verify stock update.
    # Reflects real workflow: category.py -> supplier.py -> product.py -> billing.py
    def test_scenario1_full_product_lifecycle(self, db):

        cur = db.cursor()

        #  Add a category
        cur.execute("INSERT INTO category(name) VALUES(?)", ("Electronics",))
        db.commit()
        cur.execute("SELECT cid FROM category WHERE name=?", ("Electronics",))
        assert cur.fetchone() is not None, "Category should exist after insert"

        # Add a supplier
        cur.execute("INSERT INTO supplier(name,contact,desc) VALUES(?,?,?)",
                    ("TechSupplier", "9999999", "Electronics supplier"))
        db.commit()
        cur.execute("SELECT invoice FROM supplier WHERE name=?", ("TechSupplier",))
        assert cur.fetchone() is not None, "Supplier should exist after insert"

        # Add a product
        cur.execute(
            "INSERT INTO product(Category,Supplier,name,price,qty,status) VALUES(?,?,?,?,?,?)",
            ("Electronics", "TechSupplier", "Smartphone", "599.99", "15", "Active"))
        db.commit()
        cur.execute("SELECT pid, qty FROM product WHERE name=?", ("Smartphone",))
        row = cur.fetchone()
        assert row is not None, "Product should exist after insert"
        pid, qty = row[0], int(row[1])
        assert qty == 15

        # Simulate a sale of 5 units (Reflects billing.py bill_middle())
        sold = 5
        remaining = qty - sold
        status = "Inactive" if remaining == 0 else "Active"
        cur.execute("UPDATE product SET qty=?,status=? WHERE pid=?", (remaining, status, pid))
        db.commit()

        # Verify final state
        cur.execute("SELECT qty, status FROM product WHERE pid=?", (pid,))
        final = cur.fetchone()
        assert int(final[0]) == 10, "Quantity should be 10 after selling 5"
        assert final[1] == "Active", "Status should still be Active with stock remaining"

    # T002: Low stock alert integration test
    # Scenario: Product starts with sufficient stock -> sells down below threshold  -> dashboard low stock count increases -> low stock window query reflects it
    # Reflects dashboard.py update_content() + low_stock.py load_low_stock()
    def test_scenario2_low_stock_alert_triggered_after_sale(self, db):
        cur = db.cursor()
        threshold = 5

        # Add product with stock just above threshold
        cur.execute(
            "INSERT INTO product(Category,Supplier,name,price,qty,status) VALUES(?,?,?,?,?,?)",
            ("Tools", "SupplierB", "Drill", "89.99", "8", "Active"))
        db.commit()

        # Verify not in low stock initially
        cur.execute(
            "SELECT COUNT(*) FROM product WHERE CAST(qty AS INTEGER) <= ?", (threshold,))
        assert cur.fetchone()[0] == 0, "Should have no low stock items initially"

        # Simulate sale that drops qty below threshold
        cur.execute("SELECT pid FROM product WHERE name=?", ("Drill",))
        pid = cur.fetchone()[0]
        cur.execute("UPDATE product SET qty=? WHERE pid=?", (4, pid))
        db.commit()

        # Dashboard count should now detect the alert
        cur.execute(
            "SELECT COUNT(*) FROM product WHERE CAST(qty AS INTEGER) <= ?", (threshold,))
        low_count = cur.fetchone()[0]
        assert low_count == 1, "Dashboard should detect 1 low stock item"

        # Low stock window query should return the correct product
        cur.execute(
            "SELECT name, qty FROM product WHERE CAST(qty AS INTEGER) <= ?", (threshold,))
        rows = cur.fetchall()
        assert len(rows) == 1
        assert rows[0][0] == "Drill"
        assert int(rows[0][1]) == 4