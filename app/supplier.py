from tkinter import *
from tkinter import ttk, messagebox
from db_helper import get_db_connection


class supplierClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+320+220")
        self.root.config(bg="white")
        self.root.resizable(False, False)
        self.root.focus_force()
 
        # Variables
        self.var_searchtxt = StringVar()
        self.var_sup_invoice = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()
 
        # Title
        Label(self.root, text="Supplier Details",
              font=("goudy old style", 20, "bold"), bg="#0f4d7d",
              fg="white").place(x=50, y=10, width=1000, height=40)
 
        # Form fields
        Label(self.root, text="Invoice No.", font=("goudy old style", 15),
              bg="white").place(x=50, y=80)
        Entry(self.root, textvariable=self.var_sup_invoice,
              font=("goudy old style", 15), bg="lightyellow").place(x=180, y=80, width=180)
 
        Label(self.root, text="Name", font=("goudy old style", 15),
              bg="white").place(x=50, y=120)
        Entry(self.root, textvariable=self.var_name,
              font=("goudy old style", 15), bg="lightyellow").place(x=180, y=120, width=180)
 
        Label(self.root, text="Contact", font=("goudy old style", 15),
              bg="white").place(x=50, y=160)
        Entry(self.root, textvariable=self.var_contact,
              font=("goudy old style", 15), bg="lightyellow").place(x=180, y=160, width=180)
 
        Label(self.root, text="Description", font=("goudy old style", 15),
              bg="white").place(x=50, y=200)
        self.txt_desc = Text(self.root, font=("goudy old style", 15), bg="lightyellow")
        self.txt_desc.place(x=180, y=200, width=470, height=120)
 
        # Buttons
        Button(self.root, text="Save", command=self.add,
               font=("goudy old style", 15), bg="#2196f3", fg="white",
               cursor="hand2").place(x=180, y=370, width=110, height=35)
        Button(self.root, text="Update", command=self.update,
               font=("goudy old style", 15), bg="#4caf50", fg="white",
               cursor="hand2").place(x=300, y=370, width=110, height=35)
        Button(self.root, text="Delete", command=self.delete,
               font=("goudy old style", 15), bg="#f44336", fg="white",
               cursor="hand2").place(x=420, y=370, width=110, height=35)
        Button(self.root, text="Clear", command=self.clear,
               font=("goudy old style", 15), bg="#607d8b", fg="white",
               cursor="hand2").place(x=540, y=370, width=110, height=35)
 
        # Search
        Label(self.root, text="Invoice No.", bg="white",
              font=("goudy old style", 15)).place(x=700, y=80)
        Entry(self.root, textvariable=self.var_searchtxt,
              font=("goudy old style", 15), bg="lightyellow").place(x=850, y=80, width=160)
        Button(self.root, command=self.search, text="Search",
               font=("goudy old style", 15), bg="#4caf50", fg="white",
               cursor="hand2").place(x=980, y=79, width=100, height=28)
 
        # Supplier table
        sup_frame = Frame(self.root, bd=3, relief=RIDGE)
        sup_frame.place(x=700, y=120, width=380, height=350)
 
        scrolly = Scrollbar(sup_frame, orient=VERTICAL)
        scrollx = Scrollbar(sup_frame, orient=HORIZONTAL)
 
        self.SupplierTable = ttk.Treeview(
            sup_frame, columns=("invoice", "name", "contact", "desc"),
            yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.SupplierTable.xview)
        scrolly.config(command=self.SupplierTable.yview)
 
        for col, heading, width in [
            ("invoice", "Invoice", 90), ("name", "Name", 100),
            ("contact", "Contact", 100), ("desc", "Description", 100)
        ]:
            self.SupplierTable.heading(col, text=heading)
            self.SupplierTable.column(col, width=width)
        self.SupplierTable["show"] = "headings"
        self.SupplierTable.pack(fill=BOTH, expand=1)
        self.SupplierTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()
#-----------------------------------------------------------------------------------------------------
    def add(self):
        if not self.var_sup_invoice.get():
            messagebox.showerror("Error", "Invoice must be required", parent=self.root)
            return
        con = get_db_connection()
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
            if cur.fetchone():
                messagebox.showerror("Error", "Invoice no. is already assigned", parent=self.root)
            else:
                cur.execute(
                    "INSERT INTO supplier(invoice,name,contact,desc) VALUES(?,?,?,?)",
                    (self.var_sup_invoice.get(), self.var_name.get(),
                     self.var_contact.get(), self.txt_desc.get('1.0', END)))
                con.commit()
                messagebox.showinfo("Success", "Supplier Added Successfully", parent=self.root)
                self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {ex}", parent=self.root)
        finally:
            con.close()

    def show(self):
        con = get_db_connection()
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM supplier")
            rows = cur.fetchall()
            self.SupplierTable.delete(*self.SupplierTable.get_children())
            for row in rows:
                self.SupplierTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {ex}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        f = self.SupplierTable.focus()
        row = self.SupplierTable.item(f)['values']
        if row:
            self.var_sup_invoice.set(row[0])
            self.var_name.set(row[1])
            self.var_contact.set(row[2])
            self.txt_desc.delete('1.0', END)
            self.txt_desc.insert(END, row[3])

    def update(self):
        if not self.var_sup_invoice.get():
            messagebox.showerror("Error", "Invoice must be required", parent=self.root)
            return
        con = get_db_connection()
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
            if not cur.fetchone():
                messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)
            else:
                cur.execute(
                    "UPDATE supplier SET name=?,contact=?,desc=? WHERE invoice=?",
                    (self.var_name.get(), self.var_contact.get(),
                     self.txt_desc.get('1.0', END), self.var_sup_invoice.get()))
                con.commit()
                messagebox.showinfo("Success", "Supplier Updated Successfully", parent=self.root)
                self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {ex}", parent=self.root)
        finally:
            con.close()
    def delete(self):
        if not self.var_sup_invoice.get():
            messagebox.showerror("Error", "Invoice No. must be required", parent=self.root)
            return
        con = get_db_connection()
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
            if not cur.fetchone():
                messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)
            elif messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root):
                cur.execute("DELETE FROM supplier WHERE invoice=?", (self.var_sup_invoice.get(),))
                con.commit()
                messagebox.showinfo("Delete", "Supplier Deleted Successfully", parent=self.root)
                self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {ex}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete('1.0',END)
        self.var_searchtxt.set("")
        self.show()

    def search(self):
        if not self.var_searchtxt.get():
            messagebox.showerror("Error", "Invoice No. should be required", parent=self.root)
            return
        con = get_db_connection()
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.var_searchtxt.get(),))
            row = cur.fetchone()
            if row:
                self.SupplierTable.delete(*self.SupplierTable.get_children())
                self.SupplierTable.insert('', END, values=row)
            else:
                messagebox.showerror("Error", "No record found!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {ex}", parent=self.root)
        finally:
            con.close()


if __name__=="__main__":
    root=Tk()
    obj=supplierClass(root)
    root.mainloop()