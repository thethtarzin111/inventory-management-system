from db_helper import get_db_connection

def create_db():
    con = get_db_connection()
    cur = con.cursor()

    try: 
        cur.execute("""CREATE TABLE IF NOT EXISTS employee(eid INTEGER PRIMARY KEY AUTOINCREMENT,name text,email text,gender text,contact text,dob text,doj text,pass text,utype text,address text,salary text)""")
        con.commit()
    except Exception as e:
        print(f"Error creating employee table: {e}")
    
    try:
        cur.execute("""CREATE TABLE IF NOT EXISTS supplier(invoice INTEGER PRIMARY KEY AUTOINCREMENT,name text,contact text,desc text)""")
        con.commit()
    except Exception as e:
        print(f"Error creating supplier table: {e}")

    try:
        cur.execute("""CREATE TABLE IF NOT EXISTS category(cid INTEGER PRIMARY KEY AUTOINCREMENT,name text)""")
        con.commit()
    except Exception as e:
        print(f"Error creating category table: {e}")

    try:
        cur.execute("""CREATE TABLE IF NOT EXISTS product(pid INTEGER PRIMARY KEY AUTOINCREMENT,Category text, Supplier text,name text,price text,qty text,status text)""")
        con.commit()
    except Exception as e:
        print(f"Error creating product table: {e}")

    finally:
        con.close()

create_db()