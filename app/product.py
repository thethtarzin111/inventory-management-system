from tkinter import *
from tkinter import ttk, messagebox
from db_helper import get_db_connection
 
SEARCH_COLUMNS = {"Category": "Category", "Supplier": "Supplier", "Name": "name"}

class productClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+320+220")
        self.root.config(bg="white")
        self.root.resizable(False,False)
        self.root.focus_force()
        #---------------------------------------
        #----------- variables -------------
        self.var_cat = StringVar()
        self.var_pid = StringVar()
        self.var_sup = StringVar()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.cat_list = []
        self.sup_list = []

        # Left product form frame
        product_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        product_Frame.place(x=10,y=10,width=450,height=480)

        #------------ title --------------
        Label(product_Frame, text="Manage Product Details",
              font=("goudy old style", 18), bg="#0f4d7d", fg="white").pack(side=TOP, fill=X)

        fields = [
            ("Category", 60), ("Supplier", 110), ("Name", 160),
            ("Price", 210), ("Quantity", 260), ("Status", 310)
        ]
        for text, y in fields:
            Label(product_Frame, text=text, font=("goudy old style", 18), bg="white").place(x=30, y=y)
 
        self.cmb_cat = ttk.Combobox(product_Frame, textvariable=self.var_cat,
                                    values=self.cat_list, state='readonly',
                                    justify=CENTER, font=("goudy old style", 15))
        self.cmb_cat.place(x=150, y=60, width=200)
 
        self.cmb_sup = ttk.Combobox(product_Frame, textvariable=self.var_sup,
                                    values=self.sup_list, state='readonly',
                                    justify=CENTER, font=("goudy old style", 15))
        self.cmb_sup.place(x=150, y=110, width=200)
 
        Entry(product_Frame, textvariable=self.var_name,
              font=("goudy old style", 15), bg="lightyellow").place(x=150, y=160, width=200)
        Entry(product_Frame, textvariable=self.var_price,
              font=("goudy old style", 15), bg="lightyellow").place(x=150, y=210, width=200)
        Entry(product_Frame, textvariable=self.var_qty,
              font=("goudy old style", 15), bg="lightyellow").place(x=150, y=260, width=200)

        cmb_status=ttk.Combobox(product_Frame,textvariable=self.var_status,values=("Active","Inactive"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_status.place(x=150,y=310,width=200)
        cmb_status.current(0)

        #-------------- buttons -----------------
        Button(product_Frame, text="Save", command=self.add,
               font=("goudy old style", 15), bg="#2196f3", fg="white",
               cursor="hand2").place(x=10, y=400, width=100, height=40)
        Button(product_Frame, text="Update", command=self.update,
               font=("goudy old style", 15), bg="#4caf50", fg="white",
               cursor="hand2").place(x=120, y=400, width=100, height=40)
        Button(product_Frame, text="Delete", command=self.delete,
               font=("goudy old style", 15), bg="#f44336", fg="white",
               cursor="hand2").place(x=230, y=400, width=100, height=40)
        Button(product_Frame, text="Clear", command=self.clear,
               font=("goudy old style", 15), bg="#607d8b", fg="white",
               cursor="hand2").place(x=340, y=400, width=100, height=40)

        #---------- Search Frame -------------
        SearchFrame=LabelFrame(self.root,text="Search Product",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=480,y=10,width=600,height=80)

        #------------ options ----------------
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","Category","Supplier","Name"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        Entry(SearchFrame, textvariable=self.var_searchtxt,
              font=("goudy old style", 15), bg="lightyellow").place(x=200, y=10)
        Button(SearchFrame, text="Search", command=self.search,
               font=("goudy old style", 15), bg="#4caf50", fg="white",
               cursor="hand2").place(x=410, y=9, width=150, height=30)

        #------------ product details -------------
        product_frame=Frame(self.root,bd=3,relief=RIDGE)
        product_frame.place(x=480,y=100,width=600,height=390)

        scrolly=Scrollbar(product_frame,orient=VERTICAL)
        scrollx=Scrollbar(product_frame,orient=HORIZONTAL)\
        
        columns = ("pid", "Category", "Supplier", "name", "price", "qty", "status")
        headings = ("P ID", "Category", "Supplier", "Name", "Price", "Quantity", "Status")
 
        self.ProductTable = ttk.Treeview(product_frame, columns=columns,
                                         yscrollcommand=scrolly.set,
                                         xscrollcommand=scrollx.set)
        
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)
        
        for col, heading in zip(columns, headings):
            self.ProductTable.heading(col, text=heading)
            self.ProductTable.column(col, width=100)
        self.ProductTable["show"] = "headings"
        self.ProductTable.pack(fill=BOTH, expand=1)
        self.ProductTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()
        self.fetch_cat_sup()
#-----------------------------------------------------------------------------------------------------
    def fetch_cat_sup(self):
        # Populate category and supplier lists for the comboboxes, with "Select" and "Empty" as default options
        con = get_db_connection()
        cur = con.cursor()
        try:
            cur.execute("SELECT name FROM category")
            cats = [row[0] for row in cur.fetchall()]
            self.cat_list.clear()
            self.cat_list += (cats if cats else ["Empty"])
            if cats:
                self.cat_list.insert(0, "Select")
 
            cur.execute("SELECT name FROM supplier")
            sups = [row[0] for row in cur.fetchall()]
            self.sup_list.clear()
            self.sup_list += (sups if sups else ["Empty"])
            if sups:
                self.sup_list.insert(0, "Select")
 
            self.cmb_cat['values'] = self.cat_list
            self.cmb_sup['values'] = self.sup_list
            if self.cat_list:
                self.cmb_cat.current(0)
            if self.sup_list:
                self.cmb_sup.current(0)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {ex}", parent=self.root)
        finally:
            con.close()

    
    
    def add(self):
        cat = self.var_cat.get()
        sup = self.var_sup.get()
        if cat in ("Select", "Empty", "") or sup in ("Select", "Empty", ""):
            messagebox.showerror("Error", "All fields are required", parent=self.root)
            return
        con = get_db_connection()
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM product WHERE name=?", (self.var_name.get(),))
            if cur.fetchone():
                messagebox.showerror("Error", "Product already present", parent=self.root)
            else:
                cur.execute(
                    "INSERT INTO product(Category,Supplier,name,price,qty,status) VALUES(?,?,?,?,?,?)",
                    (cat, sup, self.var_name.get(), self.var_price.get(),
                     self.var_qty.get(), self.var_status.get()))
                con.commit()
                messagebox.showinfo("Success", "Product Added Successfully", parent=self.root)
                self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {ex}", parent=self.root)
        finally:
            con.close()

    def show(self):
        con = get_db_connection()
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM product")
            rows = cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {ex}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        f = self.ProductTable.focus()
        row = self.ProductTable.item(f)['values']
        if row:
            self.var_pid.set(row[0])
            self.var_cat.set(row[1])
            self.var_sup.set(row[2])
            self.var_name.set(row[3])
            self.var_price.set(row[4])
            self.var_qty.set(row[5])
            self.var_status.set(row[6])

    def update(self):
        if not self.var_pid.get():
            messagebox.showerror("Error", "Please select product from list", parent=self.root)
            return
        con = get_db_connection()
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM product WHERE pid=?", (self.var_pid.get(),))
            if not cur.fetchone():
                messagebox.showerror("Error", "Invalid Product", parent=self.root)
            else:
                cur.execute(
                    "UPDATE product SET Category=?,Supplier=?,name=?,price=?,qty=?,status=? WHERE pid=?",
                    (self.var_cat.get(), self.var_sup.get(), self.var_name.get(),
                     self.var_price.get(), self.var_qty.get(), self.var_status.get(),
                     self.var_pid.get()))
                con.commit()
                messagebox.showinfo("Success", "Product Updated Successfully", parent=self.root)
                self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {ex}", parent=self.root)
        finally:
            con.close()

    def delete(self):
        if not self.var_pid.get():
            messagebox.showerror("Error", "Select Product from the list", parent=self.root)
            return
        con = get_db_connection()
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM product WHERE pid=?", (self.var_pid.get(),))
            if not cur.fetchone():
                messagebox.showerror("Error", "Invalid Product", parent=self.root)
            elif messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root):
                cur.execute("DELETE FROM product WHERE pid=?", (self.var_pid.get(),))
                con.commit()
                messagebox.showinfo("Delete", "Product Deleted Successfully", parent=self.root)
                self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {ex}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("Active")
        self.var_pid.set("")
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        self.show()

    
    def search(self):
        #Search products using a safe parameterised query
        search_by = self.var_searchby.get()
        search_txt = self.var_searchtxt.get()
 
        if search_by == "Select":
            messagebox.showerror("Error", "Select Search By option", parent=self.root)
            return
        if not search_txt:
            messagebox.showerror("Error", "Search input should be required", parent=self.root)
            return
 
        column = SEARCH_COLUMNS.get(search_by, search_by)
        con = get_db_connection()
        cur = con.cursor()
        try:
            cur.execute(f"SELECT * FROM product WHERE {column} LIKE ?", (f"%{search_txt}%",))
            rows = cur.fetchall()
            if rows:
                self.ProductTable.delete(*self.ProductTable.get_children())
                for row in rows:
                    self.ProductTable.insert('', END, values=row)
            else:
                messagebox.showerror("Error", "No record found!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {ex}", parent=self.root)
        finally:
            con.close()

if __name__=="__main__":
    root=Tk()
    obj=productClass(root)
    root.mainloop()