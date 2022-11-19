from tkinter import PhotoImage, Tk, messagebox
from PIL import ImageTk
from tkinter import *

import pymysql

class Login:
    def __init__(self,root):
        self.root = root
        self.root.title("Face Recognition Login")
        self.root.geometry("1024x640")
        self.root.resizable(False, False)
        self.root.iconphoto(False, PhotoImage(file = 'facial-recognition.png'))
        
        self.bg = ImageTk.PhotoImage(file="synthetic-data-1024x640.png")
        self.bg_image = Label(self.root,image=self.bg).place(x=0,y=0,relheight=1,relwidth=1)

        # self.root.wm_attributes("-transparent", 'blue')  # to make transparent background
        # title = Label(self.root,text="FACEREC",font=('arial',25,'bold'),bg='#045189',fg='red').pack()

        mainFrame = Frame(self.root)
        mainFrame.place(x=150,y=120,height=400,width=310)

        usernameV = StringVar()
        passwordV = StringVar()
        displayLabelV = StringVar()

        title = Label(mainFrame,text="LOGIN HERE",font=("arial",20,"bold"),fg="red").pack()
        usernameL = Label(mainFrame,text="Username : ",font=("arial",15)).pack()
        username = Entry(mainFrame,textvariable=usernameV,width=30).pack()
        
        passwordL = Label(mainFrame,text="Password : ",font=("arial",15)).pack()
        password = Entry(mainFrame,textvariable=passwordV,show='*',width=30).pack()

        loginButton = Button(mainFrame,text="LOGIN",font=("arial",11),command=lambda:login()).pack()
        addAdmin = Button(mainFrame,text="Add New Admin",font=("arial",11),command=lambda:admin()).pack()
        
        displayLabel = Label(mainFrame,textvariable=displayLabelV,fg="red").pack()

        for widget in mainFrame.winfo_children():
            widget.pack_configure(padx=10, pady=10)
# ----------------------------------------------    LOGIN   ------------------------------------------------------------------
        con = pymysql.connect(host='localhost',user='root',password='',database='face_recognition')
        cur = con.cursor()
        def login():
            usernameg = usernameV.get()
            passwordg = passwordV.get()
            userlogin = []
            usernameList = []
            if (usernameg=="" or passwordg==""):
                messagebox.showerror("FILED : ","All Field Required !!! ")
            elif(usernameg!="" or passwordg!=""):                
                cur.execute("SELECT * from admin")        
                for row in cur:
                    usernameD = row[1]
                    passwordD = row[2]    
                    if (usernameg==usernameD and passwordg==passwordD):
                        userlogin.append(usernameD)
                        userlogin.append(passwordD)
                    else:
                        usernameList.append(usernameD)
                # ********************************************
                if len(userlogin)>1:
                    # print("run1")
                    if usernameg==userlogin[0] and passwordg==userlogin[1]:
                        self.root.destroy()
                        from index import Index
                        Index(Tk())
                        # displayLabelV.set("Login Successfully !!! ")
                elif len(usernameList)>0:    
                    # print("run2")
                    if usernameg in usernameList :
                        displayLabelV.set("Incorrect Password!, Please Enter Valid password")
                    else:
                        displayLabelV.set("Username incorrect or user not exist")
                else:
                    # print("run3")
                    displayLabelV.set("First Add admin")

# ----------------------------------------------    Add Admin   -------------------------------------------------------------------
        def admin():
            # mainFrame.destroy()
            mainFrame.place_forget()
            addFrame = Frame(self.root)
            addFrame.place(x=150,y=120,height=400,width=310) 
            nameV = StringVar()
            unameV = StringVar()
            passV = StringVar()
            cpassV = StringVar()
            displayLabel1V = StringVar()
            
            title1 = Label(addFrame,text="Register HERE",font=("arial",20,"bold"),fg="red").pack()

            nameL = Label(addFrame,text="Enter Name :").pack()
            name = Entry(addFrame,textvariable=nameV,width=30).pack()
            
            unameL = Label(addFrame,text="User Name : ").pack()
            uname = Entry(addFrame,textvariable=unameV,width=30).pack()
            
            passL = Label(addFrame,text="Password : ").pack()
            psw = Entry(addFrame,textvariable=passV,width=30,show="*").pack()
            
            cpassL = Label(addFrame,text="Confirm Password").pack()
            cpass = Entry(addFrame,textvariable=cpassV,width=30,show="*").pack()

            bottomframe1 = Frame(addFrame)
            bottomframe1.pack(pady=20)
            regbtn = Button(bottomframe1,text="Register",font=("arial",11),command=lambda:register()).pack(side=LEFT,padx=10)
            backbtn = Button(bottomframe1,text="Login",font=("arial",11),command=lambda:back()).pack(side=RIGHT,padx=10)

            displayLabel1 = Label(addFrame,textvariable=displayLabel1V,fg="red").pack()

            for widget in addFrame.winfo_children():
                widget.pack_configure(padx=10, pady=5)
# ----------------------------------------------------------------------------------------------------------------
            def register():
                nameg = nameV.get()
                unameg = unameV.get()
                passg = passV.get()
                cpassg = cpassV.get()
                unameD = []

                if (nameg=="" or unameg=="" or passg=="" or cpassg==""):
                    messagebox.showerror("FIELD : ","All Field Required !!! ")
                elif (passg!=cpassg):
                    displayLabel1V.set("Check !! password and confirm password need same")
                else:
                    cur.execute("SELECT * from admin")
                    for row in cur :
                        unameD.append(row[1])
                    if unameg in unameD:
                        displayLabel1V.set("Uname Exist , Please try another one")
                    else:
                        displayLabel1V.set("Register Successfully")
#-------------------------------------------------------------------------------------------------------------
            def back():
                addFrame.place_forget()
                mainFrame.place(x=150,y=120,height=400,width=310)




if __name__ == "__main__":
    root=Tk()
    app=Login(root)
    root.mainloop()