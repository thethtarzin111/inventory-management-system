from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import time
import os
import tempfile
from db_helper import get_db_connection

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, 'images')
BILL_DIR = os.path.join(BASE_DIR, 'bill')
os.makedirs(BILL_DIR, exist_ok = True)

DISCOUNT_RATE = 0.05 # 5% discount

class billClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+110+80")
        self.root.resizable(False,False)
        self.root.config(bg="white")
        self.cart_list=[]
        self.bill_ready = False # set a proper boolean

        #------------- title --------------
        self.icon_title=PhotoImage(file=os.path.join(IMAGE_DIR, "logo1.png"))
        Label(
            self.root, text="Inventory Management System",
            image=self.icon_title, compound=LEFT,
            font=("times new roman", 40, "bold"),
            bg="#010c48", fg="white", anchor="w", padx=20
        ).place(x=0, y=0, relwidth=1, height=70)

        #------------ logout button -----------
        Button(
            self.root, text="Logout",
            font=("times new roman", 15, "bold"),
            bg="yellow", cursor="hand2").place(x=1150, y=10, height=50, width=150)

        #------------ clock -----------------
        self.lbl_clock=Label(self.root,text="Welcome to Inventory Management System\t\t Date: DD:MM:YYYY\t\t Time: HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #-------------- product frame -----------------
        ProductFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        ProductFrame1.place(x=6,y=110,width=410,height=550)

        Label(ProductFrame1, text="All Products",
              font=("goudy old style", 20, "bold"),
              bg="#262626", fg="white").pack(side=TOP, fill=X)
        
        self.var_search=StringVar()

        ProductFrame2=Frame(ProductFrame1,bd=2,relief=RIDGE,bg="white")
        ProductFrame2.place(x=2,y=42,width=398,height=90)

        Label(ProductFrame2, text="Search Product | By Name",
              font=("times new roman", 15, "bold"), bg="white", fg="green").place(x=2, y=5)
        Label(ProductFrame2, text="Product Name",
              font=("times new roman", 15, "bold"), bg="white").place(x=2, y=45)
        Entry(ProductFrame2, textvariable=self.var_search,
              font=("times new roman", 15), bg="lightyellow").place(x=128, y=47, width=150, height=22)
        Button(ProductFrame2, text="Search", command=self.search,
               font=("goudy old style", 15), bg="#2196f3", fg="white",
               cursor="hand2").place(x=285, y=45, width=100, height=25)
        Button(ProductFrame2, text="Show All", command=self.show,
               font=("goudy old style", 15), bg="#083531", fg="white",
               cursor="hand2").place(x=285, y=10, width=100, height=25)
        
        ProductFrame3=Frame(ProductFrame1,bd=3,relief=RIDGE)
        ProductFrame3.place(x=2,y=140,width=398,height=375)

        scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)\
        
        self.product_Table=ttk.Treeview(ProductFrame3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)

        for col, heading, width in [
            ("pid", "P ID", 40), ("name", "Name", 100),
            ("price", "Price", 100), ("qty", "Quantity", 40), ("status", "Status", 90)
        ]:
            self.product_Table.heading(col, text=heading)
            self.product_Table.column(col, width=width)

        self.product_Table["show"] = "headings"
        self.product_Table.pack(fill=BOTH, expand=1)
        self.product_Table.bind("<ButtonRelease-1>", self.get_data)
 
        Label(ProductFrame1,
              text="Note: 'Enter 0 Quantity to remove product from the Cart'",
              font=("goudy old style", 12), anchor="w", bg="white", fg="red").pack(side=BOTTOM, fill=X)
        
        #-------------- customer frame ---------------
        self.var_cname=StringVar()
        self.var_contact=StringVar()

        CustomerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        CustomerFrame.place(x=420,y=110,width=530,height=70)

        Label(CustomerFrame, text="Customer Details",
              font=("goudy old style", 15), bg="lightgray").pack(side=TOP, fill=X)
        Label(CustomerFrame, text="Name",
              font=("times new roman", 15), bg="white").place(x=5, y=35)
        Entry(CustomerFrame, textvariable=self.var_cname,
              font=("times new roman", 13), bg="lightyellow").place(x=80, y=35, width=180)
        Label(CustomerFrame, text="Contact No.",
              font=("times new roman", 15), bg="white").place(x=270, y=35)
        Entry(CustomerFrame, textvariable=self.var_contact,
              font=("times new roman", 15), bg="lightyellow").place(x=380, y=35, width=140)

        # Calculator + Cart container
        Cal_Cart_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Cal_Cart_Frame.place(x=420,y=190,width=530,height=360)

        #--------------- calculator frame ---------------------
        self.var_cal_input=StringVar()

        Cal_Frame=Frame(Cal_Cart_Frame,bd=9,relief=RIDGE,bg="white")
        Cal_Frame.place(x=5,y=10,width=268,height=340)

        self.txt_cal_input=Entry(Cal_Frame,textvariable=self.var_cal_input,font=('arial',15,'bold'),width=21,bd=10,relief=GROOVE,state='readonly',justify=RIGHT)
        self.txt_cal_input.grid(row=0,columnspan=4)

        buttons = [
            (7, 1, 0), (8, 1, 1), (9, 1, 2), ('+', 1, 3),
            (4, 2, 0), (5, 2, 1), (6, 2, 2), ('-', 2, 3),
            (1, 3, 0), (2, 3, 1), (3, 3, 2), ('*', 3, 3),
            (0, 4, 0), ('C', 4, 1), ('=', 4, 2), ('/', 4, 3),
        ]
        for label, row, col in buttons:
            if label == 'C':
                cmd = self.clear_cal
            elif label == '=':
                cmd = self.perform_cal
            else:
                cmd = lambda l=label: self.get_input(l)
            Button(Cal_Frame, text=label, font=('arial', 15, 'bold'),
                   command=cmd, bd=5, width=4, pady=10, cursor="hand2").grid(row=row, column=col)

        #------------------ cart frame --------------------
        Cart_Frame=Frame(Cal_Cart_Frame,bd=3,relief=RIDGE)
        Cart_Frame.place(x=280,y=8,width=245,height=342)
        self.cartTitle=Label(Cart_Frame,text="Cart \t Total Products: [0]",font=("goudy old style",15),bg="lightgray")
        self.cartTitle.pack(side=TOP,fill=X)

        scrolly2=Scrollbar(Cart_Frame,orient=VERTICAL)
        scrollx2=Scrollbar(Cart_Frame,orient=HORIZONTAL)\
        
        self.CartTable=ttk.Treeview(Cart_Frame,columns=("pid","name","price","qty"),yscrollcommand=scrolly2.set,xscrollcommand=scrollx2.set)
        scrollx2.pack(side=BOTTOM,fill=X)
        scrolly2.pack(side=RIGHT,fill=Y)
        scrollx2.config(command=self.CartTable.xview)
        scrolly2.config(command=self.CartTable.yview)

        for col, heading, width in [
            ("pid", "P ID", 40), ("name", "Name", 100),
            ("price", "Price", 90), ("qty", "Quantity", 30)
        ]:
            self.CartTable.heading(col, text=heading)
            self.CartTable.column(col, width=width)
        self.CartTable["show"] = "headings"
        self.CartTable.pack(fill=BOTH, expand=1)
        self.CartTable.bind("<ButtonRelease-1>", self.get_data_cart)

        #-------------- add cart widgets frame ---------------
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()

        Add_CartWidgets_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Add_CartWidgets_Frame.place(x=420,y=550,width=530,height=110)

        Label(Add_CartWidgets_Frame, text="Product Name",
              font=("times new roman", 15), bg="white").place(x=5, y=5)
        Entry(Add_CartWidgets_Frame, textvariable=self.var_pname,
              font=("times new roman", 15), bg="lightyellow",
              state='readonly').place(x=5, y=35, width=190, height=22)
 
        Label(Add_CartWidgets_Frame, text="Price Per Qty",
              font=("times new roman", 15), bg="white").place(x=230, y=5)
        Entry(Add_CartWidgets_Frame, textvariable=self.var_price,
              font=("times new roman", 15), bg="lightyellow",
              state='readonly').place(x=230, y=35, width=150, height=22)
 
        Label(Add_CartWidgets_Frame, text="Quantity",
              font=("times new roman", 15), bg="white").place(x=390, y=5)
        Entry(Add_CartWidgets_Frame, textvariable=self.var_qty,
              font=("times new roman", 15), bg="lightyellow").place(x=390, y=35, width=120, height=22)

        self.lbl_inStock=Label(Add_CartWidgets_Frame,text="In Stock",font=("times new roman",15),bg="white")
        self.lbl_inStock.place(x=5,y=70)

        Button(Add_CartWidgets_Frame, command=self.clear_cart, text="Clear",
               font=("times new roman", 15, "bold"), bg="lightgray",
               cursor="hand2").place(x=180, y=70, width=150, height=30)
        Button(Add_CartWidgets_Frame, command=self.add_update_cart, text="Add | Update",
               font=("times new roman", 15, "bold"), bg="orange",
               cursor="hand2").place(x=340, y=70, width=180, height=30)
        
        #------------------- billing area -------------------
        billFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billFrame.place(x=953,y=110,width=400,height=410)

        Label(billFrame, text="Customer Bill Area",
              font=("goudy old style", 20, "bold"),
              bg="#262626", fg="white").pack(side=TOP, fill=X)
        
        scrolly3=Scrollbar(billFrame,orient=VERTICAL)
        scrolly3.pack(side=RIGHT,fill=Y)

        self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly3.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly3.config(command=self.txt_bill_area.yview)

        #------------------- billing buttons -----------------------
        billMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billMenuFrame.place(x=953,y=520,width=400,height=140)

        self.lbl_amnt=Label(billMenuFrame,text="Bill Amount\n[0]",font=("goudy old style",15,"bold"),bg="#3f51b5",fg="white")
        self.lbl_amnt.place(x=2,y=5,width=120,height=70)

        self.lbl_discount=Label(billMenuFrame,text="Discount\n[5%]",font=("goudy old style",15,"bold"),bg="#8bc34a",fg="white")
        self.lbl_discount.place(x=124,y=5,width=120,height=70)

        self.lbl_net_pay=Label(billMenuFrame,text="Net Pay\n[0]",font=("goudy old style",15,"bold"),bg="#607d8b",fg="white")
        self.lbl_net_pay.place(x=246,y=5,width=160,height=70)

        Button(billMenuFrame, text="Print", command=self.print_bill,
               cursor="hand2", font=("goudy old style", 15, "bold"),
               bg="lightgreen", fg="white").place(x=2, y=80, width=120, height=50)
        Button(billMenuFrame, text="Clear All", command=self.clear_all,
               cursor="hand2", font=("goudy old style", 15, "bold"),
               bg="gray", fg="white").place(x=124, y=80, width=120, height=50)
        Button(billMenuFrame, text="Generate Bill", command=self.generate_bill,
               cursor="hand2", font=("goudy old style", 15, "bold"),
               bg="#009688", fg="white").place(x=246, y=80, width=160, height=50)

        self.show()
        #self.bill_top()
        self.update_date_time()
#---------------------- all functions ------------------------------
    def get_input(self,num):
        self.var_cal_input.set(self.var_cal_input.get() + str(num))

    def clear_cal(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        # Evaluate the calculator expression safely
        expr = self.var_cal_input.get()
        try:
            result = eval(expr, {"__builtins__": {}})  # restrict builtins for safety
            self.var_cal_input.set(result)
        except Exception:
            messagebox.showerror("Error", "Invalid expression", parent=self.root)
            self.clear_cal()

    def _generate_invoice_number(self):
        # Generate a unique invoice number from the current timestamp
        return int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))
    
#---------------------- all functions ------------------------------
    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select pid,name,price,qty,status from product where status='Active'")
            rows=cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {ex}", parent=self.root)
        finally:
            con.close()

    def search(self):

        if not self.var_search.get():
            messagebox.showerror("Error", "Search input should be required", parent=self.root)
            return

        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute(
                "SELECT pid,name,price,qty,status FROM product WHERE name LIKE ?",
                (f"%{self.var_search.get()}%",))
            rows = cur.fetchall()
            if rows:
                self.product_Table.delete(*self.product_Table.get_children())
                for row in rows:
                    self.product_Table.insert('', END, values=row)
            else:
                messagebox.showerror("Error", "No record found!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {ex}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        f = self.product_Table.focus()
        row = self.product_Table.item(f)['values']
        if row:
            self.var_pid.set(row[0])
            self.var_pname.set(row[1])
            self.var_price.set(row[2])
            self.lbl_inStock.config(text=f"In Stock [{row[3]}]")
            self.var_stock.set(row[3])
            self.var_qty.set('1')
    
    def get_data_cart(self, ev):
        f = self.CartTable.focus()
        row = self.CartTable.item(f)['values']
        if row:
            self.var_pid.set(row[0])
            self.var_pname.set(row[1])
            self.var_price.set(row[2])
            self.var_qty.set(row[3])
        
    def add_update_cart(self):
        if not self.var_pid.get():
            messagebox.showerror("Error", "Please select product from the list", parent=self.root)
            return
        if not self.var_qty.get():
            messagebox.showerror("Error", "Quantity is required", parent=self.root)
            return
        if int(self.var_qty.get()) > int(self.var_stock.get()):
            messagebox.showerror("Error", "Invalid Quantity", parent=self.root)
            return
    
        cart_data = [
            self.var_pid.get(), self.var_pname.get(),
            self.var_price.get(), self.var_qty.get(), self.var_stock.get()
        ]
    
        existing_index = next(
            (i for i, row in enumerate(self.cart_list) if row[0] == self.var_pid.get()), None)
    
        if existing_index is not None:
            if messagebox.askyesno("Confirm",
                                "Product already present\nDo you want to Update|Remove from Cart?",
                                parent=self.root):
                if self.var_qty.get() == "0":
                    self.cart_list.pop(existing_index)
                else:
                    self.cart_list[existing_index][3] = self.var_qty.get()
        else:
            self.cart_list.append(cart_data)
    
        self.show_cart()
        self.bill_update()

    def bill_update(self):
        # Recalculate totals and refresh the billing labels
        bill_amount = sum(float(str(row[2]).replace('$', '').replace(',', '').strip()) * int(row[3]) for row in self.cart_list)
        discount = bill_amount * DISCOUNT_RATE
        net_pay = bill_amount - discount
 
        self.bill_amnt = bill_amount
        self.discount = discount
        self.net_pay = net_pay
 
        self.lbl_amnt.config(text=f"Bill Amnt\n{bill_amount:.2f}")
        self.lbl_net_pay.config(text=f"Net Pay\n{net_pay:.2f}")
        self.cartTitle.config(text=f"Cart \t Total Products: [{len(self.cart_list)}]")

    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def generate_bill(self):
        if not self.var_cname.get() or not self.var_contact.get():
            messagebox.showerror("Error",f"Customer Details are required",parent=self.root)
            return
        elif len(self.cart_list)==0:
            messagebox.showerror("Error",f"Please Add product to the Cart!!!",parent=self.root)
            return
        else:
            self.invoice = self._generate_invoice_number()
            self.bill_top()
            self.bill_middle()
            self.bill_bottom()
    
            bill_path = os.path.join(BILL_DIR, f"{self.invoice}.txt")
            with open(bill_path, 'w') as fp:
                fp.write(self.txt_bill_area.get('1.0', END))
    
            messagebox.showinfo("Saved", "Bill has been generated", parent=self.root)
            self.bill_ready = True

    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top_temp=f'''
\t\tXYZ-Inventory
\t Phone No. 9899459288 , Delhi-110053
{"="*46}
 Customer Name: {self.var_cname.get()}
 Ph. no. : {self.var_contact.get()}
 Bill No. {self.invoice}\t\t\tDate: {time.strftime("%d/%m/%Y")}
{"="*46}
 Product Name\t\t\tQTY\tPrice
{"="*46}
'''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)

    def bill_bottom(self):
        bill_bottom_temp=f'''
{"="*46}
 Bill Amount\t\t\t\tRs.{self.bill_amnt:.2f}
 Discount\t\t\t\tRs.{self.discount:.2f}
 Net Pay\t\t\t\tRs.{self.net_pay:.2f}
{"="*46}\n
'''
        self.txt_bill_area.insert(END,bill_bottom_temp)

    def bill_middle(self):
        con = get_db_connection()
        cur = con.cursor()
        try:
            for row in self.cart_list:
                pid, name, price, qty_sold, stock = row
                qty_sold = int(qty_sold)
                remaining_qty = int(stock) - qty_sold
                status = "Inactive" if remaining_qty == 0 else "Active"
                line_total = float(str(price).replace('$', '').replace(',', '').strip()) * qty_sold
 
                self.txt_bill_area.insert(
                    END, f"\n {name}\t\t\t{qty_sold}\tRs.{line_total:.2f}")
 
                cur.execute(
                    "UPDATE product SET qty=?,status=? WHERE pid=?",
                    (remaining_qty, status, pid))
                con.commit()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {ex}", parent=self.root)
        finally:
            con.close()

    def clear_cart(self):
        self.var_pid.set("")
        self.var_pname.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.lbl_inStock.config(text=f"In Stock")
        self.var_stock.set("")

    def clear_all(self):
        del self.cart_list[:]
        self.clear_cart()
        self.show()
        self.show_cart()
        self.var_cname.set("")
        self.var_contact.set("")
        self.bill_ready = False
        self.txt_bill_area.delete('1.0',END)
        self.cartTitle.config(text=f"Cart \t Total Products: [0]")
        self.var_search.set("")
        
    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)

    def print_bill(self):
        if self.bill_ready:
            messagebox.showinfo("Print", "Please wait while printing", parent=self.root)
            new_file = tempfile.mktemp('.txt')
            with open(new_file, 'w') as f:
                f.write(self.txt_bill_area.get('1.0', END))
            os.startfile(new_file, 'print')
        else:
            messagebox.showinfo("Print", "Please generate bill to print the receipt", parent=self.root)

if __name__=="__main__":
    root=Tk()
    obj=billClass(root)
    root.mainloop()