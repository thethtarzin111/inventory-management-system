from tkinter import *
from tkinter import ttk, messagebox
from db_helper import get_db_connection

# Search columns that are safe to filter on
SEARCH_COLUMNS = {"Email": "email", "Name": "name", "Contact": "contact"}

class employeeClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+320+220")

        self.root.config(bg="white")
        self.root.resizable(False,False)
        self.root.focus_force()

        #------------ all variables --------------
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()
        self.var_emp_id=StringVar()
        self.var_gender=StringVar()
        self.var_contact=StringVar()
        self.var_name=StringVar()
        self.var_dob=StringVar()
        self.var_doj=StringVar()
        self.var_email=StringVar()
        self.var_pass=StringVar()
        self.var_utype=StringVar()
        self.var_salary=StringVar()

        #---------- Search Frame -------------
        SearchFrame=LabelFrame(self.root,text="Search Employee",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=250,y=20,width=600,height=70)

        #------------ options ----------------
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","Email","Name","Contact"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        Entry(SearchFrame, textvariable=self.var_searchtxt,
              font=("goudy old style", 15), bg="lightyellow").place(x=200, y=10)
        Button(SearchFrame, command=self.search, text="Search",
               font=("goudy old style", 15), bg="#4caf50", fg="white",
               cursor="hand2").place(x=410, y=9, width=150, height=30)

        #-------------- title ---------------
        Label(self.root, text="Employee Details",
              font=("goudy old style", 15), bg="#0f4d7d",
              fg="white").place(x=50, y=100, width=1000)

        #-------------- content ---------------
        #---------- row 1 ----------------
        Label(self.root, text="Emp ID", font=("goudy old style", 15), bg="white").place(x=50, y=150)
        Label(self.root, text="Gender", font=("goudy old style", 15), bg="white").place(x=350, y=150)
        Label(self.root, text="Contact", font=("goudy old style", 15), bg="white").place(x=750, y=150)
 
        Entry(self.root, textvariable=self.var_emp_id,
              font=("goudy old style", 15), bg="lightyellow").place(x=150, y=150, width=180)
        cmb_gender = ttk.Combobox(
            self.root, textvariable=self.var_gender,
            values=("Select", "Male", "Female", "Other"),
            state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_gender.place(x=500, y=150, width=180)
        cmb_gender.current(0)
        Entry(self.root, textvariable=self.var_contact,
              font=("goudy old style", 15), bg="lightyellow").place(x=850, y=150, width=180)

        #---------- row 2 ----------------
        Label(self.root, text="Name", font=("goudy old style", 15), bg="white").place(x=50, y=190)
        Label(self.root, text="D.O.B.", font=("goudy old style", 15), bg="white").place(x=350, y=190)
        Label(self.root, text="D.O.J.", font=("goudy old style", 15), bg="white").place(x=750, y=190)
 
        Entry(self.root, textvariable=self.var_name,
              font=("goudy old style", 15), bg="lightyellow").place(x=150, y=190, width=180)
        Entry(self.root, textvariable=self.var_dob,
              font=("goudy old style", 15), bg="lightyellow").place(x=500, y=190, width=180)
        Entry(self.root, textvariable=self.var_doj,
              font=("goudy old style", 15), bg="lightyellow").place(x=850, y=190, width=180)

        #---------- row 3 ----------------
        Label(self.root, text="Email", font=("goudy old style", 15), bg="white").place(x=50, y=230)
        Label(self.root, text="Password", font=("goudy old style", 15), bg="white").place(x=350, y=230)
        Label(self.root, text="User Type", font=("goudy old style", 15), bg="white").place(x=750, y=230)
 
        Entry(self.root, textvariable=self.var_email,
              font=("goudy old style", 15), bg="lightyellow").place(x=150, y=230, width=180)
        Entry(self.root, textvariable=self.var_pass,
              font=("goudy old style", 15), bg="lightyellow").place(x=500, y=230, width=180)
        cmb_utype = ttk.Combobox(
            self.root, textvariable=self.var_utype,
            values=("Admin", "Employee"),
            state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_utype.place(x=850, y=230, width=180)
        cmb_utype.current(0)
        
        #---------- row 4 ----------------
        Label(self.root, text="Address", font=("goudy old style", 15), bg="white").place(x=50, y=270)
        Label(self.root, text="Salary", font=("goudy old style", 15), bg="white").place(x=500, y=270)

        self.txt_address = Text(self.root, font=("goudy old style", 15), bg="lightyellow")
        self.txt_address.place(x=150, y=270, width=300, height=60)
        Entry(self.root, textvariable=self.var_salary,
              font=("goudy old style", 15), bg="lightyellow").place(x=600, y=270, width=180)
        
        #-------------- buttons -----------------
        Button(self.root, text="Save", command=self.add, 
               font=("goudy old style", 15), bg="#2196f3", fg="white",
               cursor="hand2").place(x=500, y=305, width=110, height=28)
        Button(self.root, text="Update", command=self.update,
               font=("goudy old style", 15), bg="#4caf50", fg="white",
               cursor="hand2").place(x=620, y=305, width=110, height=28)
        Button(self.root, text="Delete", command=self.delete,
               font=("goudy old style", 15), bg="#f44336", fg="white",
               cursor="hand2").place(x=740, y=305, width=110, height=28)
        Button(self.root, text="Clear", command=self.clear,
               font=("goudy old style", 15), bg="#607d8b", fg="white",
               cursor="hand2").place(x=860, y=305, width=110, height=28)

        #------------ employee details -------------
        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=0,y=350,relwidth=1,height=150)

        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

        columns = ("eid", "name", "email", "gender", "contact",
                   "dob", "doj", "pass", "utype", "address", "salary")
        headings = ("EMP ID", "Name", "Email", "Gender", "Contact",
                    "D.O.B", "D.O.J", "Password", "User Type", "Address", "Salary")
        
        self.EmployeeTable=ttk.Treeview(emp_frame,columns=columns,yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)
        
        for col, heading in zip(columns, headings):
            self.EmployeeTable.heading(col, text=heading)
            self.EmployeeTable.column(col, width=100)
        self.EmployeeTable["show"] = "headings"
        self.EmployeeTable.pack(fill=BOTH, expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()
#-----------------------------------------------------------------------------------------------------
    def add(self):
        if not self.var_emp_id.get():
            messagebox.showerror("Error", "Employee ID must be required", parent=self.root)
            return
        con = get_db_connection()
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),))
            if cur.fetchone():
                messagebox.showerror("Error", "This Employee ID is already assigned", parent=self.root)
            else:
                cur.execute(
                    "INSERT INTO employee(eid,name,email,gender,contact,dob,doj,pass,utype,address,salary) "
                    "VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                    (self.var_emp_id.get(), self.var_name.get(), self.var_email.get(),
                     self.var_gender.get(), self.var_contact.get(), self.var_dob.get(),
                     self.var_doj.get(), self.var_pass.get(), self.var_utype.get(),
                     self.txt_address.get('1.0', END), self.var_salary.get()))
                con.commit()
                messagebox.showinfo("Success", "Employee Added Successfully", parent=self.root)
                self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {ex}", parent=self.root)
        finally:
            con.close()

    def show(self):
        con = get_db_connection()
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM employee")
            rows = cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {ex}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        f = self.EmployeeTable.focus()
        row = self.EmployeeTable.item(f)['values']
        if row:
            self.var_emp_id.set(row[0])
            self.var_name.set(row[1])
            self.var_email.set(row[2])
            self.var_gender.set(row[3])
            self.var_contact.set(row[4])
            self.var_dob.set(row[5])
            self.var_doj.set(row[6])
            self.var_pass.set(row[7])
            self.var_utype.set(row[8])
            self.txt_address.delete('1.0', END)
            self.txt_address.insert(END, row[9])
            self.var_salary.set(row[10])

    def update(self):
        if not self.var_emp_id.get():
            messagebox.showerror("Error", "Employee ID must be required", parent=self.root)
            return
        con = get_db_connection()
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),))
            if not cur.fetchone():
                messagebox.showerror("Error", "Invalid Employee ID", parent=self.root)
            else:
                cur.execute(
                    "UPDATE employee SET name=?,email=?,gender=?,contact=?,dob=?,doj=?,"
                    "pass=?,utype=?,address=?,salary=? WHERE eid=?",
                    (self.var_name.get(), self.var_email.get(), self.var_gender.get(),
                     self.var_contact.get(), self.var_dob.get(), self.var_doj.get(),
                     self.var_pass.get(), self.var_utype.get(),
                     self.txt_address.get('1.0', END), self.var_salary.get(),
                     self.var_emp_id.get()))
                con.commit()
                messagebox.showinfo("Success", "Employee Updated Successfully", parent=self.root)
                self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {ex}", parent=self.root)
        finally:
            con.close()

    def delete(self):
        if not self.var_emp_id.get():
            messagebox.showerror("Error", "Employee ID must be required", parent=self.root)
            return
        con = get_db_connection()
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),))
            if not cur.fetchone():
                messagebox.showerror("Error", "Invalid Employee ID", parent=self.root)
            elif messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root):
                cur.execute("DELETE FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                con.commit()
                messagebox.showinfo("Delete", "Employee Deleted Successfully", parent=self.root)
                self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {ex}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_pass.set("")
        self.var_utype.set("Admin")
        self.txt_address.delete('1.0',END)
        self.var_salary.set("")
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        self.show()

    def search(self):
        #Search employees using a safe parameterised query.
        search_by = self.var_searchby.get()
        search_txt = self.var_searchtxt.get()
 
        if search_by == "Select":
            messagebox.showerror("Error", "Select Search By option", parent=self.root)
            return
        if not search_txt:
            messagebox.showerror("Error", "Search input should be required", parent=self.root)
            return
 
        # Map display label to actual column name
        column = SEARCH_COLUMNS.get(search_by, search_by.lower())
        con = get_db_connection()
        cur = con.cursor()
        try:
            cur.execute(f"SELECT * FROM employee WHERE {column} LIKE ?", (f"%{search_txt}%",))
            rows = cur.fetchall()
            if rows:
                self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                for row in rows:
                    self.EmployeeTable.insert('', END, values=row)
            else:
                messagebox.showerror("Error", "No record found!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {ex}", parent=self.root)
        finally:
            con.close()


if __name__=="__main__":
    root=Tk()
    obj=employeeClass(root)
    root.mainloop()