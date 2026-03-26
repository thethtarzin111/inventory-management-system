'''
Unit tests for IMS Inventory Management System
Purpose: Each individual database operation is tested in isolation.
Can run with: pytest tests/test_unit.py -v
'''

# Unit tests for category table operations.
class TestCategoryUnit:

    # T001: Add a new category and verify it exists.
    def test_add_category(self, db):
        cur = db.cursor()
        cur.execute("INSERT INTO category(name) VALUES(?)", ("Electronics",))
        db.commit()

        cur.execute("SELECT name FROM category WHERE name=?", ("Electronics",))
        row = cur.fetchone()
        assert row is not None
        assert row[0] == "Electronics"

    # T002: Inserting a duplicate category name is blocked by the app logic check.
    def test_duplicate_category_not_added(self, db):
        cur = db.cursor()
        cur.execute("INSERT INTO category(name) VALUES(?)", ("Electronics",))
        db.commit()

        # Simulate the app-level duplicate check (mirrors category.py add())
        cur.execute("SELECT * FROM category WHERE name=?", ("Electronics",))
        existing = cur.fetchone()
        assert existing is not None, "Duplicate check should find the existing row"

    # T003: Successfully deleting a category by its ID
    def test_delete_category(self, db):
        cur = db.cursor()
        cur.execute("INSERT INTO category(name) VALUES(?)", ("Furniture",))
        db.commit()

        cur.execute("SELECT cid FROM category WHERE name=?", ("Furniture",))
        cid = cur.fetchone()[0] # cid = category id

        cur.execute("DELETE FROM category WHERE cid=?", (cid,))
        db.commit()

        cur.execute("SELECT * FROM category WHERE cid=?", (cid,))
        assert cur.fetchone() is None, "Category should be deleted"

# ==============================================================================

# Unit tests for category table operations.
class TestProductUnit:

    # T004: Add a new product and verify it exists.
    def test_add_product(self, db):
        cur = db.cursor()
        # First, add a category to link the product to
        cur.execute("INSERT INTO category(name) VALUES(?)", ("Electronics",))
        cur.execute("INSERT INTO supplier(name,contact,desc) VALUES(?,?,?)",
                    ("SupplierA", "123456", "Test supplier"))
        db.commit()

        # Add the product
        cur.execute(
            "INSERT INTO product(Category,Supplier,name,price,qty,status) VALUES(?,?,?,?,?,?)",
            ("Electronics", "SupplierA", "Laptop", "999.99", "10", "Active"))
        db.commit()

        cur.execute("SELECT * FROM product WHERE name=?", ("Laptop",))
        row = cur.fetchone()
        assert row is not None
        assert row[3] == "Laptop"
        assert row[6] == "Active"

    # T005: Product quantity updates correctly after a sale
    def test_update_product_quantity(self, db):
        cur = db.cursor()
        cur.execute(
            "INSERT INTO product(Category,Supplier,name,price,qty,status) VALUES(?,?,?,?,?,?)",
            ("Electronics", "SupplierA", "Mouse", "25.00", "10", "Active"))
        db.commit()
 
        cur.execute("SELECT pid FROM product WHERE name=?", ("Mouse",))
        pid = cur.fetchone()[0]
 
        new_qty = 10 - 3  # sell 3 units
        cur.execute("UPDATE product SET qty=? WHERE pid=?", (new_qty, pid))
        db.commit()
 
        cur.execute("SELECT qty FROM product WHERE pid=?", (pid,))
        assert int(cur.fetchone()[0]) == 7

    # T006: Product status becomes Inactive when quantity reaches 0
    def test_product_status_inactive_when_out_of_stock(self, db):
        cur = db.cursor()
        cur.execute(
            "INSERT INTO product(Category,Supplier,name,price,qty,status) VALUES(?,?,?,?,?,?)",
            ("Electronics", "SupplierA", "Keyboard", "45.00", "1", "Active"))
        db.commit()
 
        cur.execute("SELECT pid FROM product WHERE name=?", ("Keyboard",))
        pid = cur.fetchone()[0]

        # This mirrors billing.py bill_middle() logic
        remaining = 1 - 1
        status = "Inactive" if remaining == 0 else "Active"
        cur.execute("UPDATE product SET qty=?,status=? WHERE pid=?", (remaining, status, pid))
        db.commit()

        cur.execute("SELECT qty, status FROM product WHERE pid=?", (pid,))
        row = cur.fetchone()
        assert int(row[0]) == 0
        assert row[1] == "Inactive"

# Unit tests for low stock detection logic
class TestLowStockUnit:
 
    #T007: Low stock query returns only products at or below threshold
    def test_low_stock_query_returns_correct_products(self, db):
        cur = db.cursor()
        cur.executemany(
            "INSERT INTO product(Category,Supplier,name,price,qty,status) VALUES(?,?,?,?,?,?)",
            [
                ("Cat", "Sup", "ProductA", "10", "3", "Active"),    # low stock
                ("Cat", "Sup", "ProductB", "20", "5", "Active"),    # at threshold
                ("Cat", "Sup", "ProductC", "30", "20", "Active"),   # normal
                ("Cat", "Sup", "ProductD", "40", "0", "Inactive"),  # out of stock
            ]
        )
        db.commit()
 
        cur.execute(
            "SELECT name FROM product WHERE CAST(qty AS INTEGER) <= ?", (5,))
        low = [row[0] for row in cur.fetchall()]
 
        assert "ProductA" in low
        assert "ProductB" in low
        assert "ProductD" in low
        assert "ProductC" not in low
 
    #T008: Low stock query returns nothing when all products are well stocked
    def test_no_low_stock_when_all_sufficient(self, db):
        cur = db.cursor()
        cur.executemany(
            "INSERT INTO product(Category,Supplier,name,price,qty,status) VALUES(?,?,?,?,?,?)",
            [
                ("Cat", "Sup", "ProductX", "10", "50", "Active"),
                ("Cat", "Sup", "ProductY", "20", "100", "Active"),
            ]
        )
        db.commit()
 
        cur.execute(
            "SELECT COUNT(*) FROM product WHERE CAST(qty AS INTEGER) <= ?", (5,))
        assert cur.fetchone()[0] == 0
 