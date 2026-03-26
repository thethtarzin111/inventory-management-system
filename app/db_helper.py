# Eliminates duplication where every file opens its own database connection

import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'ims.db')

def get_db_connection():
    # Return a new SQLite conection to the IMS database
    return sqlite3.connect(DB_PATH)