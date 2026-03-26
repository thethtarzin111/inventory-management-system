from tkinter import *
from tkinter import ttk, messagebox
from db_helper import get_db_connection

LOW_STOCK_THRESHOLD = 5

class LowStockClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Low Stock Alert")
        self.root.geometry("800x450+280+200")
        self.root.config(bg="white")
        self.root.resizable(False, False)
        self.root.focus_force()

        # Title
        Label(
            self.root, text="Low Stock Products",
            font=("goudy old style", 24, "bold"), bg="#184a45", fg="white",
            bd=3, relief=RIDGE
        ).pack(side=TOP, fill=X, padx=10, pady=10)

        # Label for threadshold info (low stock)
        Label(
            self.root, text=f"Products with stock less than {LOW_STOCK_THRESHOLD}",
            font=("goudy old style", 15), bg="white", fg="#c0392b"
        ).pack(pady=(0, 5))

        # Table frame
        table_frame = Frame(self.root, bd=3, relief=RIDGE)
        table_frame.pack(fill=BOTH, expand=1, padx=10, pady=10)

        # Scrollbars
        scrolly = Scrollbar(table_frame, orient=VERTICAL)
        scrollx = Scrollbar(table_frame, orient=HORIZONTAL)

        columns = ("pid", "name", "category", "supplier", "price", "qty", "status")
        headings = ("P ID", "Product Name", "Category", "Supplier", "Price", "Qty Left", "Status")

        self.StockTable = ttk.Treeview(
            table_frame, columns=columns,
            yscrollcommand=scrolly.set,
            xscrollcommand=scrollx.set)
 
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.StockTable.xview)
        scrolly.config(command=self.StockTable.yview)
 
        col_widths = [50, 160, 120, 120, 80, 70, 80]
        for col, heading, width in zip(columns, headings, col_widths):
            self.StockTable.heading(col, text=heading)
            self.StockTable.column(col, width=width, anchor=CENTER)
 
        self.StockTable["show"] = "headings"

        # Color tags -> red: out of stock, orange: critically low
        self.StockTable.tag_configure("out_of_stock", background="#f5b7b1", foreground="#922b21")
        self.StockTable.tag_configure("low_stock", background="#fdebd0", foreground="#a04000")
        self.StockTable.pack(fill=BOTH, expand=1)

        # Bottom bar
        bottom_frame = Frame(self.root, bg="white")
        bottom_frame.pack(fill=X, padx=10, pady=8)
 
        self.lbl_count = Label(
            bottom_frame,
            text="Low stock items: 0",
            font=("goudy old style", 13, "bold"),
            bg="white", fg="#c0392b"
        )
        self.lbl_count.pack(side=LEFT, padx=10)

        Button(
            bottom_frame, text="Refresh",
            command=self.load_low_stock,
            font=("goudy old style", 13),
            bg="#2196f3", fg="white", cursor="hand2"
        ).pack(side=RIGHT, padx=5)
 
        Button(
            bottom_frame, text="Close",
            command=self.root.destroy,
            font=("goudy old style", 13),
            bg="#607d8b", fg="white", cursor="hand2"
        ).pack(side=RIGHT, padx=5)

        self.load_low_stock()

    def load_low_stock(self):
        # Query products with low stock
        con = get_db_connection()
        cur = con.cursor()
        try:
            cur.execute("SELECT pid, name, Category, Supplier, price, qty, status "
                        "FROM product WHERE CAST(qty AS INTEGER) <= ?", (LOW_STOCK_THRESHOLD,))
            rows = cur.fetchall()
            self.StockTable.delete(*self.StockTable.get_children())

            for row in rows:
                qty = int(row[5])
                tag = "out_of_stock" if qty == 0 else "low_stock"
                self.StockTable.insert("", END, values=row, tags=(tag,))

            self.lbl_count.config(text=f"Low stock items: {len(rows)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching data: {e}", parent=self.root)
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    obj = LowStockClass(root)
    root.mainloop()
