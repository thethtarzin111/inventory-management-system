from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import time
import os

from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass

from low_stock import LowStockClass
from db_helper import get_db_connection

# ------------------ BASE PATH SETUP ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")
BILL_DIR = os.path.join(BASE_DIR, "bill")
LOW_STOCK_THRESHOLD = 5   

os.makedirs(BILL_DIR, exist_ok=True)
# ---------------------------------------------------

class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+110+80")
        self.root.resizable(False, False)
        self.root.config(bg="white")

        # ------------- title --------------
        self.icon_title = PhotoImage(file=os.path.join(IMAGE_DIR, "logo1.png"))
        Label(
            self.root,
            text="Inventory Management System",
            image=self.icon_title,
            compound=LEFT,
            font=("times new roman", 40, "bold"),
            bg="#010c48",
            fg="white",
            anchor="w",
            padx=20
        ).place(x=0, y=0, relwidth=1, height=70)

        # ------------ logout button -----------
        Button(
            self.root, text="Logout",
            font=("times new roman", 15, "bold"),
            bg="yellow", cursor="hand2"
        ).place(x=1150, y=10, height=50, width=150)

        # ------------ clock -----------------
        self.lbl_clock = Label(
            self.root,
            text="Welcome to Inventory Management System\t\t Date: DD:MM:YYYY\t\t Time: HH:MM:SS",
            font=("times new roman", 15),
            bg="#4d636d", fg="white"
        )
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        # ---------------- left menu ---------------
        self.MenuLogo = Image.open(os.path.join(IMAGE_DIR, "menu_im.png"))
        self.MenuLogo = self.MenuLogo.resize((200, 200))
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)

        LeftMenu = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        LeftMenu.place(x=0, y=102, width=200, height=565)

        Label(LeftMenu, image=self.MenuLogo).pack(side=TOP, fill=X)
        Label(LeftMenu, text="Menu", font=("times new roman", 20), bg="#009688").pack(side=TOP, fill=X)

        self.icon_side = PhotoImage(file=os.path.join(IMAGE_DIR, "side.png"))

        menu_buttons = [
            ("Employee", self.employee),
            ("Supplier", self.supplier),
            ("Category", self.category),
            ("Products", self.product),
            ("Sales", self.sales),
            ("Low Stock", self.low_stock),   # NEW menu button
        ]
        for text, cmd in menu_buttons:
            Button(
                LeftMenu, text=text, command=cmd,
                image=self.icon_side, compound=LEFT,
                padx=5, anchor="w",
                font=("times new roman", 20, "bold"),
                bg="white", bd=3, cursor="hand2"
            ).pack(side=TOP, fill=X)

        Button(
            LeftMenu, text="Exit",
            image=self.icon_side, compound=LEFT,
            padx=5, anchor="w",
            font=("times new roman", 20, "bold"),
            bg="white", bd=3, cursor="hand2",
            command=self.root.destroy
        ).pack(side=TOP, fill=X)

        # Stat cards
        self.lbl_employee = Label(
            self.root, text="Total Employee\n{ 0 }",
            bd=5, relief=RIDGE, bg="#33bbf9",
            fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_employee.place(x=300, y=120, height=150, width=300)
 
        self.lbl_supplier = Label(
            self.root, text="Total Supplier\n{ 0 }",
            bd=5, relief=RIDGE, bg="#ff5722",
            fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_supplier.place(x=650, y=120, height=150, width=300)
 
        self.lbl_category = Label(
            self.root, text="Total Category\n{ 0 }",
            bd=5, relief=RIDGE, bg="#009688",
            fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_category.place(x=1000, y=120, height=150, width=300)

        # Product card will turn red if low stock detected
        self.lbl_product = Label(
            self.root, text="Total Product\n{ 0 }",
            bd=5, relief=RIDGE, bg="#607d8b",
            fg="white", font=("goudy old style", 20, "bold"),
            cursor="hand2")
        self.lbl_product.place(x=300, y=300, height=150, width=300)
        self.lbl_product.bind("<Button-1>", lambda e: self.low_stock())  # clickable shortcut
 
        self.lbl_sales = Label(
            self.root, text="Total Sales\n{ 0 }",
            bd=5, relief=RIDGE, bg="#ffc107",
            fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_sales.place(x=650, y=300, height=150, width=300)
 
        # New feature: low stock alert card
        self.lbl_low_stock = Label(
            self.root, text="Low Stock Items\n{ 0 }",
            bd=5, relief=RIDGE, bg="#607d8b",
            fg="white", font=("goudy old style", 20, "bold"),
            cursor="hand2")
        self.lbl_low_stock.place(x=1000, y=300, height=150, width=300)
        self.lbl_low_stock.bind("<Button-1>", lambda e: self.low_stock())
 
        # Footer
        Label(
            self.root,
            text="IMS-Inventory Management System",
            font=("times new roman", 12),
            bg="#4d636d", fg="white"
        ).pack(side=BOTTOM, fill=X)
 
        self.update_content()

    # -------------- functions ----------------
    def employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = employeeClass(self.new_win)

    def supplier(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = supplierClass(self.new_win)

    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = categoryClass(self.new_win)

    def product(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = productClass(self.new_win)

    def sales(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = salesClass(self.new_win)

    # New function to open low stock window
    def low_stock(self):              
        self.new_win = Toplevel(self.root)
        self.new_obj = LowStockClass(self.new_win)

    def update_content(self):
        con = get_db_connection()
        cur = con.cursor()

        try:
            cur.execute("SELECT COUNT(*) FROM product")
            self.lbl_product.config(text=f"Total Product\n[ {cur.fetchone()[0]} ]")

            cur.execute("SELECT COUNT(*) FROM category")
            self.lbl_category.config(text=f"Total Category\n[ {cur.fetchone()[0]} ]")

            cur.execute("SELECT COUNT(*) FROM employee")
            self.lbl_employee.config(text=f"Total Employee\n[ {cur.fetchone()[0]} ]")

            cur.execute("SELECT COUNT(*) FROM supplier")
            self.lbl_supplier.config(text=f"Total Supplier\n[ {cur.fetchone()[0]} ]")

            # New feature: count low stock products
            cur.execute(
                "SELECT COUNT(*) FROM product WHERE CAST(qty AS INTEGER) <= ?",
                (LOW_STOCK_THRESHOLD,)
            )
            low_count = cur.fetchone()[0]
            self.lbl_low_stock.config(text=f"Low Stock Items\n[ {low_count} ]")
 
            # Turn product card red if any low stock, otherwise normal grey
            if low_count > 0:
                self.lbl_product.config(bg="#c0392b")   # red warning
                self.lbl_low_stock.config(bg="#c0392b")
            else:
                self.lbl_product.config(bg="#607d8b")   # normal grey
                self.lbl_low_stock.config(bg="#4caf50")  # green = all good
            # ---------------------------------------
 
            bill_count = len(os.listdir(BILL_DIR))
            self.lbl_sales.config(text=f"Total Sales\n[ {bill_count} ]")

            time_ = time.strftime("%I:%M:%S")
            date_ = time.strftime("%d-%m-%Y")
            self.lbl_clock.config(
                text=f"Welcome to Inventory Management System\t\t Date: {date_}\t\t Time: {time_}"
            )

        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {e}", parent=self.root)
        finally:
            con.close()

        self.lbl_clock.after(200, self.update_content)

if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()
