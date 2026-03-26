import os
from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
from db_helper import get_db_connection

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")

class categoryClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+320+220")
        self.root.config(bg="white")
        self.root.resizable(False,False)
        self.root.focus_force()

        #------------ variables -------------
        self.var_cat_id=StringVar()
        self.var_name=StringVar()

        #--------------- title ---------------------
        Label(
            self.root, text="Manage Product Category",
            font=("goudy old style", 30), bg="#184a45", fg="white",
            bd=3, relief=RIDGE
        ).pack(side=TOP, fill=X, padx=10, pady=20)
 
        Label(self.root, text="Enter Category Name",
              font=("goudy old style", 30), bg="white").place(x=50, y=100)
        Entry(self.root, textvariable=self.var_name, bg="lightyellow",
              font=("goudy old style", 18)).place(x=50, y=170, width=300)
 
        Button(self.root, text="ADD", command=self.add,
               font=("goudy old style", 15), bg="#4caf50", fg="white",
               cursor="hand2").place(x=360, y=170, width=150, height=30)
        Button(self.root, text="Delete", command=self.delete,
               font=("goudy old style", 15), bg="red", fg="white",
               cursor="hand2").place(x=520, y=170, width=150, height=30)

        #------------ category details -------------
        cat_frame=Frame(self.root,bd=3,relief=RIDGE)
        cat_frame.place(x=700,y=100,width=380,height=100)

        scrolly=Scrollbar(cat_frame,orient=VERTICAL)
        scrollx=Scrollbar(cat_frame,orient=HORIZONTAL)\
        
        self.CategoryTable=ttk.Treeview(cat_frame,columns=("cid","name"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CategoryTable.xview)
        scrolly.config(command=self.CategoryTable.yview)

        self.CategoryTable.heading("cid",text="C ID")
        self.CategoryTable.heading("name",text="Name")
        self.CategoryTable["show"]="headings"
        self.CategoryTable.column("cid",width=90)
        self.CategoryTable.column("name",width=100)
        
        self.CategoryTable.pack(fill=BOTH,expand=1)
        self.CategoryTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()

        #----------------- images ---------------------
        self._load_image("cat.jpg", x=50, y=220)
        self._load_image("category.jpg", x=580, y=220)

    def _load_image(self, filename, x, y):
        #Load, resize, and display an image
        path = os.path.join(IMAGE_DIR, filename)
        img = Image.open(path).resize((500, 250))
        photo = ImageTk.PhotoImage(img)
        lbl = Label(self.root, image=photo, bd=2, relief=RAISED)
        lbl.image = photo  # keep reference to prevent garbage collection
        lbl.place(x=x, y=y)
#----------------------------------------------------------------------------------
    def add(self):
        name = self.var_name.get().strip()
        if not name:
            messagebox.showerror("Error", "Category Name must be required", parent=self.root)
            return
        con = get_db_connection()
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM category WHERE name=?", (name,))
            if cur.fetchone():
                messagebox.showerror("Error", "Category already present", parent=self.root)
            else:
                cur.execute("INSERT INTO category(name) VALUES(?)", (name,))
                con.commit()
                messagebox.showinfo("Success", "Category Added Successfully", parent=self.root)
                self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {ex}", parent=self.root)
        finally:
            con.close()

    def show(self):
        con = get_db_connection()
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM category")
            rows = cur.fetchall()
            self.CategoryTable.delete(*self.CategoryTable.get_children())
            for row in rows:
                self.CategoryTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {ex}", parent=self.root)
        finally:
            con.close()

    
    def clear(self):
        self.var_name.set("")
        self.var_cat_id.set("")
        self.show()

    def get_data(self, ev):
        f = self.CategoryTable.focus()
        row = self.CategoryTable.item(f)['values']
        if row:
            self.var_cat_id.set(row[0])
            self.var_name.set(row[1])
    
    def delete(self):
        if not self.var_cat_id.get():
            messagebox.showerror("Error", "Please select a category from the list", parent=self.root)
            return
        con = get_db_connection()
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM category WHERE cid=?", (self.var_cat_id.get(),))
            if not cur.fetchone():
                messagebox.showerror("Error", "Invalid Category", parent=self.root)
            elif messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root):
                cur.execute("DELETE FROM category WHERE cid=?", (self.var_cat_id.get(),))
                con.commit()
                messagebox.showinfo("Delete", "Category Deleted Successfully", parent=self.root)
                self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {ex}", parent=self.root)
        finally:
            con.close()



if __name__=="__main__":
    root=Tk()
    obj=categoryClass(root)
    root.mainloop()