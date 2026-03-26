'''
This is the shared pytest fixtures that can be used across multiple test files in the tests/ directory. It includes fixtures for setting up a test database, creating a test client for the Flask application, and any other common setup or teardown code needed for testing.
pytest loads this file before running any tests so no import is needed in test files.
'''

import pytest
import sqlite3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

@pytest.fixture
def db():
    # Setup: create a new in-memory database and return the connection
    conn = sqlite3.connect(':memory:')
    cur = conn.cursor()
    # Create tables and insert test data as needed
    cur.execute('''CREATE TABLE employee(
        eid TEXT PRIMARY KEY,
        name TEXT, email TEXT, gender TEXT, contact TEXT,
        dob TEXT, doj TEXT, pass TEXT, utype TEXT,
        address TEXT, salary TEXT)''')
    
    cur.execute("""CREATE TABLE supplier(
        invoice INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, contact TEXT, desc TEXT)""")
    
    cur.execute("""CREATE TABLE category(
        cid INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT)""")
    
    cur.execute("""CREATE TABLE product(
        pid INTEGER PRIMARY KEY AUTOINCREMENT,
        Category TEXT, Supplier TEXT, name TEXT,
        price TEXT, qty TEXT, status TEXT)""")
    
    conn.commit()
    
    yield conn  # This is where the testing happens
    
    # Teardown: close the database connection
    conn.close()

