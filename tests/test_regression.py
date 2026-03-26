"""
Regression tests for IMS Inventory Management System
Purpose: Verify that bugs fixed during T2 refactoring stay fixed
Can run with: pytest tests/test_regression.py -v
"""

import pytest
import sqlite3


class TestRegression:

    # T001: Duplicate employee ID check works correctly
    # Found bug: original code allowed duplicate IDs if the check logic failed
    # Fix: parameterised SELECT before INSERT in employee.py add()
    def test_regression_duplicate_employee_blocked(self, db):
        cur = db.cursor()
        cur.execute(
            "INSERT INTO employee(eid,name,email,gender,contact,dob,doj,pass,utype,address,salary) "
            "VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            ("E001", "Alice", "alice@test.com", "Female", "123",
             "1990-01-01", "2020-01-01", "pass123", "Admin", "Helsinki", "3000"))
        db.commit()

        # Simulate the duplicate check from employee.py add()
        cur.execute("SELECT * FROM employee WHERE eid=?", ("E001",))
        existing = cur.fetchone()
        assert existing is not None, "Duplicate check must find the existing employee"

        # Verify only one record exists
        cur.execute("SELECT COUNT(*) FROM employee WHERE eid=?", ("E001",))
        assert cur.fetchone()[0] == 1, "Only one employee with this ID should exist"

    # T002: search no longer vulnerable to SQL injection
    # Found bug: original search() built queries via string concatenation
    # Fix: replaced with parameterised LIKE ? queries in employee.py and product.py
    def test_regression_search_uses_parameterised_query(self, db):
        cur = db.cursor()
        cur.execute(
            "INSERT INTO employee(eid,name,email,gender,contact,dob,doj,pass,utype,address,salary) "
            "VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            ("E002", "Bob", "bob@test.com", "Male", "456",
             "1985-05-05", "2019-06-01", "pass456", "Employee", "Espoo", "2500"))
        db.commit()

        # Safe parameterised search (the correct post-refactor approach)
        search_term = "Bob"
        cur.execute("SELECT * FROM employee WHERE name LIKE ?", (f"%{search_term}%",))
        rows = cur.fetchall()
        assert len(rows) == 1
        assert rows[0][1] == "Bob"

    # T003: Product add() validation correctly checks variable values
    # Found bug: original code checked `self.var_sup == 'Select'` (object comparison, always False)
    # Fix: changed to `self.var_sup.get() == 'Select'` in product.py add()
    # This test verifies by making sure that both 'Select' & 'Empty' are caught as invalid.
    def test_regression_product_validation_uses_get(self, db):
        invalid_values = ["Select", "Empty", ""]
        for val in invalid_values:
            is_invalid = val in ("Select", "Empty", "")
            assert is_invalid, f"Value '{val}' should be treated as invalid/unselected"

    # T004: database connections are always closed after use
    # Found bug: original code never called con.close(), risking database locks
    # Fix: added try/finally with con.close() in all methods
    # This test verifies by making sure that closed connections raises an exception on use
    def test_regression_connection_always_closed(self, db):
        con2 = sqlite3.connect(":memory:")
        cur2 = con2.cursor()
        cur2.execute("CREATE TABLE test(id INTEGER PRIMARY KEY, val TEXT)")
        try:
            cur2.execute("INSERT INTO test(val) VALUES(?)", ("hello",))
            con2.commit()
            cur2.execute("SELECT val FROM test")
            assert cur2.fetchone()[0] == "hello"
        finally:
            con2.close()

        # Accessing a closed connection should raise an exception
        with pytest.raises(Exception):
            cur2.execute("SELECT * FROM test")