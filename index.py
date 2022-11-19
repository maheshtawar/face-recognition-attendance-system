from tkinter import*
import pymysql
from datetime import datetime,date
from tkinter import ttk
from PIL import ImageTk

class Index:
    def __init__(self,root):
        self.root=root
        self.root.title("Face Recognition Attendance Management System")
        self.root.geometry("1024x640")
        self.root.iconphoto(False, PhotoImage(file = 'facial-recognition.png'))
        self.root.resizable(False, False)
        
        self.bg = ImageTk.PhotoImage(file="synthetic-data-1024x640.png")
        self.bg_image = Label(self.root,image=self.bg).place(x=0,y=0,relheight=1,relwidth=1)

        # self.root.wm_attributes("-transparent", 'blue')  # to make transparent background

        addStudentButton = Button(self.root,fg="red",text="Add Student",font=('arial',14,'bold'),command=self.studentcall).place(x=340,y=25)
        attendanceButton = Button(self.root,fg="red",text="Take Attendance",font=('arial',14,'bold'),command=self.openWindow).place(x=540,y=25)
        logoutButton = Button(self.root,text="logout",fg="red",command=self.logout).place(x=900,y=25)

# ------------------------------------------    OPTIONS    -----------------------------------------------------------------------
        con = pymysql.connect(host='localhost',user='root',password='',database='face_recognition')
        cur = con.cursor()

        datesList = []
        subList = []

        cur.execute("SELECT date,subject from attendance")
        for row in cur:
            datesList.append(row[0])
            subList.append(row[1])
            
        selectDate = StringVar()
        selectDate.set(date.today())
        selectSub = StringVar()
        selectSub.set(subList[-1])

        labelFrame = LabelFrame(self.root,text="Select Date and Subject and Submit to get Attendance")
        labelFrame.place(x=200,y=100)

        datelabel =Label(labelFrame,text="Select Date").pack()
        dateSelect = OptionMenu(labelFrame,selectDate,*set(datesList)).pack()
        
        sublabel = Label(labelFrame,text="Select Subject").pack()
        subSelect = OptionMenu(labelFrame,selectSub,*set(subList)).pack()

        button = Button(labelFrame,text="SUBMIT",command=lambda:selected())    
        button.pack()

        refresh = Button(labelFrame,text="REFRESH TODAY'S DATA",command=lambda:refreshed())    
        refresh.pack()

        for widget in labelFrame.winfo_children():
            widget.pack_configure(padx=10, pady=10,side=LEFT)
# ------------------------------------     CONTAINER/TREEVIEW    --------------------------------------------------------------------------------
        containerframe = Frame(self.root)
        containerframe.place(x=10,y=180)

        treexScroll = Scrollbar(containerframe,orient=HORIZONTAL)
        treexScroll.pack(side=BOTTOM,fill=X)
        
        treeyScroll = Scrollbar(containerframe,orient=VERTICAL)
        treeyScroll.pack(side=RIGHT,fill=Y)

        headingLine = Label(containerframe,text="Attendance",font=('arial',14,'bold')).pack()
        tree =ttk.Treeview(containerframe, columns=("rollno", "fname", "date","in_time","subject"),show="headings",height=17,yscrollcommand=treeyScroll.set,xscrollcommand=treexScroll.set)
        tree.pack()

        treexScroll.config(command=tree.xview)
        treeyScroll.config(command=tree.yview)

        # width of columns and alignment 
        tree.column("rollno",width=180,  anchor =CENTER)
        tree.column("fname",anchor =CENTER)
        tree.column("date",  anchor =CENTER)
        tree.column("in_time",  anchor =CENTER)
        tree.column("subject",  anchor =CENTER)
        
        # Headings  
        # respective columns
        tree.heading("rollno", text ="Roll No")
        tree.heading("fname", text ="FName")
        tree.heading("date", text ="Date")
        tree.heading("in_time", text ="in_time")  
        tree.heading("subject", text ="Subject")

        cur.execute("SELECT * from attendance where date = %s ",date.today())
        for row in cur:
            tree.insert('','end',values=(row[1],row[2],row[3],row[4],row[5]))
# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------    ON SELECTING DATE AND SUBJECT SHOW THAT DATE ATTENDANCE    -----------------------------------------------------------------------
        def selected():
            vdate = selectDate.get()
            vsub = selectSub.get()
            cur.execute("SELECT * from attendance where date = %s and subject = %s ",(vdate,vsub))
            for item in tree.get_children():
                tree.delete(item)
            for row in cur:
                tree.insert('','end',values=(row[1],row[2],row[3],row[4],row[5]))
            
                
# ------------------------------------------    REFRESH FUNCTION    -----------------------------------------------------------------------
        def refreshed():
            cur.execute("SELECT * from attendance where date = %s ",date.today())
            for item in tree.get_children():
                tree.delete(item)
            for row in cur:
                tree.insert('','end',values=(row[1],row[2],row[3],row[4],row[5]))

#-------------------------------------------    ATTENDANCE MARK EXTERNAL CODE   --------------------------------------

    def studentcall(self):
        self.root.destroy()
        from student import Student
        Student(Tk())

    def face_recognition(self,sub):
        from attendance import FaceRecognition 
        FaceRecognition(sub)
    
    def openWindow(self):
        def submit():
            # sub = entry.get()
            sub = selectSub1.get()
            self.newWindow.destroy()
            self.face_recognition(sub)

        self.newWindow = Toplevel(self.root)
        self.newWindow.title("New Window")
        self.newWindow.geometry("200x200")
        self.newWindow.iconphoto(False, PhotoImage(file = 'facial-recognition.png'))
        label1 = Label(self.newWindow,text="Select Subject").pack(pady=20)
        # entry = Entry(self.newWindow)
        selectSub1 = StringVar()
        selectSub1.set("CS-301")
        entry = OptionMenu(self.newWindow,selectSub1,"CS-301","CS-302","CS-303")
        entry.pack()
        button = Button(self.newWindow,text="Submit",command=submit).pack(pady=20)       

    # ----------------------------------------------------------------------------------
    def logout(self):
        self.root.destroy()
        from login import Login
        Login(Tk()) 

if __name__ == "__main__":
    root=Tk()
    app=Index(root)
    root.mainloop()