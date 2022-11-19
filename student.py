import os
import shutil
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
from PIL import Image,ImageTk
import pymysql

class Student:
    def __init__(self,root):
        self.root = root
        self.root.title("Add Student Details")
        self.root.geometry("1024x640")
        self.root.resizable(False, False)
        self.root.iconphoto(False, PhotoImage(file = 'facial-recognition.png'))
        
        self.bg = ImageTk.PhotoImage(file="synthetic-data-1024x640.png")
        self.bg_image = Label(self.root,image=self.bg).place(x=0,y=0,relheight=1,relwidth=1)
        
        heading1 = Label(self.root,text="Add Student Details",font=('arial',14,'bold')).pack(pady=20)
        backbtn = Button(self.root,text="Main Page",command=self.back).place(x=10,y=10)

        frame1 = LabelFrame(self.root,text="    Student Details Form    ")
        frame1.pack() 
        # -----------------------   ROW 0   --------------------------
        rollnolabel =Label(frame1,text="Roll No").grid(row=0,column=0)
        fnamelabel = Label(frame1,text="First Name").grid(row=0,column=1)
        lnamelabel = Label(frame1,text="Last Name").grid(row=0,column=2)
        
        # -----------------------   ROW 1   --------------------------
        v_rollno = StringVar()
        v_fname = StringVar()
        v_lname = StringVar()
        rollno = Entry(frame1,textvariable=v_rollno).grid(row=1,column=0)
        fname = Entry(frame1,textvariable=v_fname).grid(row=1,column=1)
        lname = Entry(frame1,textvariable=v_lname).grid(row=1,column=2)

        # -----------------------   ROW 2   --------------------------
        v_address = StringVar()
        addresslabel = Label(frame1,text="Address").grid(row=2,column=0)
        address = Entry(frame1,textvariable=v_address,width=50).grid(row=2,column=1,columnspan=3)

        # -----------------------   ROW 3   --------------------------
        contactlabel =Label(frame1,text="Contact").grid(row=3,column=0)
        genderlabel = Label(frame1,text="Gender").grid(row=3,column=1)
        doblabel = Label(frame1,text="DOB").grid(row=3,column=2)
        
        # -----------------------   ROW 4   --------------------------
        v_contact = StringVar()
        v_gender = StringVar()
        v_gender.set("Male")
        v_dob = StringVar()
        contact = Entry(frame1,textvariable=v_contact).grid(row=4,column=0)
        gender = OptionMenu(frame1,v_gender,"Male","Female","Other").grid(row=4,column=1)
        # gender = Entry(frame1,textvariable=v_gender).grid(row=4,column=1)
        # dob = Entry(frame1,textvariable=v_dob).grid(row=4,column=2)
        dob = DateEntry(frame1,selectmode='day',textvariable=v_dob,date_pattern='yyyy-MM-dd').grid(row=4,column=2)

        # -----------------------   ROW 5   --------------------------
        ButtonOutput = StringVar()
        ButtonOutput.set("")
        classlabel =Label(frame1,text="Class").grid(row=5,column=0)
        imagelabel = Label(frame1,text="Image").grid(row=5,column=1)
        outputlabel = Label(frame1,textvariable=ButtonOutput).grid(row=5,column=2,rowspan=2)
        
        # -----------------------   ROW 6   --------------------------
        v_class = StringVar()
        v_class.set("MCS")
        class1 = OptionMenu(frame1,v_class,"MCS","BCS","MCA","BE").grid(row=6,column=0)
        # class1 = Entry(frame1,textvariable=v_class).grid(row=6,column=0)
        image1 = Button(frame1,text="Upload Image",command=lambda:upload_file()).grid(row=6,column=1)

        for widget in frame1.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        submitButton = Button(self.root,text="Submit",width=30,command=lambda:submit()).pack(pady=10)

        # ----------------------------------------------    FRAME 2-Database TreeView    --------------------------------------------------------
        
        frame2 = LabelFrame(self.root,text="    STUDENT DETAILS    ")
        frame2.pack(padx=20,pady=5)


        treexScroll = Scrollbar(frame2,orient=HORIZONTAL)
        treexScroll.pack(side=BOTTOM,fill=X)
        
        treeyScroll = Scrollbar(frame2,orient=VERTICAL)
        treeyScroll.pack(side=RIGHT,fill=Y)

        tree =ttk.Treeview(frame2, columns=("roll_no", "fname", "lname","address","contact","gender","DOB","class","image")
        ,show="headings",yscrollcommand=treeyScroll.set,xscrollcommand=treexScroll.set)
        tree.pack(padx=20,pady=20)

        treexScroll.config(command=tree.xview)
        treeyScroll.config(command=tree.yview)

        # width of columns and alignment 
        tree.column("roll_no",minwidth=100, width=120, anchor =CENTER)
        tree.column("fname",minwidth=120,width=180,anchor =CENTER)
        tree.column("lname",minwidth=120,width=180, anchor =CENTER)
        tree.column("address",minwidth=120,width=180, anchor =CENTER)
        tree.column("contact",minwidth=120,width=180, anchor =CENTER)
        tree.column("gender",minwidth=120,width=180, anchor =CENTER)
        tree.column("DOB",minwidth=120,width=180, anchor =CENTER)
        tree.column("class",minwidth=120,width=180, anchor =CENTER)
        tree.column("image",minwidth=120,width=180, anchor =CENTER)
        
        # Headings  
        # respective columns
        tree.heading("roll_no", text ="Roll No")
        tree.heading("fname", text ="FName")
        tree.heading("lname", text ="Lname")
        tree.heading("address", text ="Address")  
        tree.heading("contact", text ="Contact")
        tree.heading("gender", text ="Gender")
        tree.heading("DOB", text ="DOB")
        tree.heading("class", text ="Class")
        tree.heading("image", text ="Image")
        
        con = pymysql.connect(host='localhost',user='root',password='',database='face_recognition')
        cur = con.cursor()
        cur.execute("SELECT * from student")
        for row in cur:
            tree.insert('','end',values=(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]))    

        # ----------------------------------------  SUBMIT FORM    --------------------------------------------------------------- 
        def submit():
            n_rollno = v_rollno.get()
            n_fname = v_fname.get()
            n_lname = v_lname.get()
            n_address = v_address.get()
            n_contact = v_contact.get()
            n_gender = v_gender.get()
            n_dob = v_dob.get()
            n_class = v_class.get()
            image_name = ButtonOutput.get()
            
            if n_rollno=="" or n_fname=="" or n_lname=="" or n_address=="" or n_contact=="" or n_gender=="" or n_dob=="" or n_class=="" or image_name=="":
                messagebox.showerror('ERROR : ','All Fields Required')
            else:
                cur.execute("""INSERT INTO student(roll_no, fname, lname, address, contact, gender, DOB, class, image) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (n_rollno,n_fname,n_lname,n_address,n_contact,n_gender,n_dob,n_class,image_name))
                con.commit()
                if TRUE:
                    messagebox.showinfo('SUCCESS : ','Data Added Successfully')
                    path = list(files["filename"])
                    shutil.move(path[0],"E:\Clg MSC1\SEM 3\ProjecteMCS2\images")

                else:
                    messagebox.showerror('FAILED : ','Failed to Add !!! ')

                

        # ----------------------------------------     UPLOAD FILE     --------------------------------------------------------------- 
        files = {}
        def upload_file():
            if v_rollno.get()=="" or v_fname.get()=="":
                messagebox.showerror('ERROR : ','All Fields Required')  

            else:
                files['filename']=filedialog.askopenfilenames(filetypes=[('JPG','*.jpg'),('PNG','*.png'),('JPEG','*.jpeg')],initialdir = os.getcwd(), title='Select File/Files')
                if len(files['filename'])!=0:
                    path = list(files["filename"])
                    image_name = path[0].split("/")[-1]
                    
                    if image_name.split(".")[0] == v_rollno.get()+"_"+v_fname.get() :
                        ButtonOutput.set(image_name.split('.')[0])
                        # shutil.move(path[0],"E:\Clg MSC1\SEM 3\Face recognition\images")
                    else:
                        messagebox.showwarning('REQUIRED : ',f'File name must be \n "{v_rollno.get()}_{v_fname.get()}"')
        
        # -------------------------------------------------------------------------------------------------------
        
    def back(self):
        self.root.destroy()
        from index import Index
        Index(Tk())          
    

if __name__ == "__main__":
    root=Tk()
    app=Student(root)
    root.mainloop()