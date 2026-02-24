import tkinter as tk
from tkinter import ttk
psw = tk.Tk()
psw.geometry("500x250")

#Heding
Head_Boder=tk.Frame(psw, width=500, height=80, bg="#8BB6FA")
Head_Boder.pack()

#Heding Lable "Grade 10 Student Login"

HDL=tk.Label(
    Head_Boder,
    bg="#8BB6FA",
    text="GRADE 10", 
    fg="#000000",
    font=("Arial", 15, "bold")          
              )
HDL.place(relx=0.5, rely=0.3, anchor="center")


HDL1=tk.Label(
    Head_Boder,
    bg="#8BB6FA",
    text="Student Login", 
    fg="#000000",
    font=("Arial", 13, "bold")          
              )
HDL1.place(relx=0.5, rely=0.6, anchor="center")

#Function for Password
def PSW_function():
    iPSW= PSW_input.get()
    iUN= user_name_input.get()
    if iUN == "a":
        if iPSW == "a": ##########-----Main Window
            root = tk.Tk()
            root.title("Students Data Base")
            root.geometry("500x350")
            #Heding
            root_Boder=tk.Frame(root, width=500, height=95, bg="#8BB6FA")
            root_Boder.pack()
            rootHDL=tk.Label(
                root_Boder,
                bg="#8BB6FA",
                text="GRADE 10", 
                fg="#000000",
                font=("Arial", 15, "bold")  )
            rootHDL.place(relx=0.5, rely=0.3, anchor="center")
            
            rootHDL1=tk.Label(
                root_Boder,
                bg="#8BB6FA",
                text="Student Appication", 
                fg="#000000",
                font=("Arial", 13, "bold")   )
            rootHDL1.place(relx=0.5, rely=0.6, anchor="center")
            
            #Root Boddy
            rootBody=tk.Frame(root, width=500, height=300, bg="#346AC2")
            rootBody.place(y=80, )            
            #Name
            name=tk.Entry(rootBody)
            name.pack()
            #Student Id
            stid=tk.Entry(rootBody)
            stid.pack()
            #Age
            age=tk.Entry(rootBody)
            age.pack()
            # Submit Button
            rootsubmit=ttk.Button(rootBody,text="Submit")
            rootsubmit.pack()
            # Stanby Button
            rootreport=ttk.Button(rootBody,text="report")
            rootreport.pack()            
            
        else:
            PSW_ERROR = tk.Tk()
            PSW_ERROR.title("Password Error")
            PSW_ERROR.geometry("400x90") 
            PSW_ERROR_lbl=tk.Label(PSW_ERROR, text="Password Is Not Correct")
            PSW_ERROR_lbl.pack()
            
                   
    else:
        Name_Error = tk.Tk()
        Name_Error.title("Name Error")
        Name_Error.geometry("400x90")
        Name_Error_lbl=tk.Label(Name_Error, text="NAMA WARADI YAKO")
        Name_Error_lbl.pack()
        
        
    

#Body of the Login
Body=tk.Frame(psw, width=500, height=170, bg="#346AC2")
Body.place(y=80, )
    # user_name_label line
user_name_label=tk.Label(Body,text="User Name :",font=("Arial", 12, ))
user_name_label.place(x=55, y=30)

user_name_input=tk.Entry(Body ,width=50) #input of the user name
user_name_input.place(x=180, y=30)

    # Password line
PSW_label=tk.Label(Body,text="Pass Word :",font=("Arial", 12, ))
PSW_label.place(x=55, y=80)

PSW_input=tk.Entry(Body ,width=50) #input of the Password
PSW_input.place(x=180, y=80)

    #------ Button ------
butn=tk.Frame(Body, width=400, height=25, bg="#346AC2")
butn.place(y=130, relx=0.5 ,anchor="center")

    #Submit Button
Submit=ttk.Button(butn, text="Submit",width=30,command=PSW_function)
Submit.place(x=0, y=00)

    #Clear Button
clear=ttk.Button(butn, text="Clear",width=30)
clear.place(x=210, y=0)


psw.mainloop()