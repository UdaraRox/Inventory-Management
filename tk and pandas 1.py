import tkinter as tk
from tkinter import ttk
import pandas as pd
import os


psw = tk.Tk()
psw.geometry("500x250")

# ---------------- FILE SETUP (PANDAS DATABASE) ----------------
FILE_NAME = "students_data.csv"

# Create CSV file if it does not exist
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["Name", "Student ID", "Age"])
    df.to_csv(FILE_NAME, index=False)

# ---------------- HEADING ----------------
Head_Boder = tk.Frame(psw, width=500, height=80, bg="#8BB6FA")
Head_Boder.pack()

HDL = tk.Label(
    Head_Boder,
    bg="#8BB6FA",
    text="GRADE 10",
    fg="#000000",
    font=("Arial", 15, "bold")
)
HDL.place(relx=0.5, rely=0.3, anchor="center")

HDL1 = tk.Label(
    Head_Boder,
    bg="#8BB6FA",
    text="Student Login",
    fg="#000000",
    font=("Arial", 13, "bold")
)
HDL1.place(relx=0.5, rely=0.6, anchor="center")

# ---------------- LOGIN FUNCTION ----------------
def PSW_function():
    iPSW = PSW_input.get()
    iUN = user_name_input.get()

    if iUN == "a":
        if iPSW == "a":

            root = tk.Tk()
            root.title("Students Data Base")
            root.geometry("500x350")

            # -------- ROOT HEADER --------
            root_Boder = tk.Frame(root, width=500, height=95, bg="#8BB6FA")
            root_Boder.pack()

            rootHDL = tk.Label(
                root_Boder,
                bg="#8BB6FA",
                text="GRADE 10",
                fg="#000000",
                font=("Arial", 15, "bold")
            )
            rootHDL.place(relx=0.5, rely=0.3, anchor="center")

            rootHDL1 = tk.Label(
                root_Boder,
                bg="#8BB6FA",
                text="Student Appication",
                fg="#000000",
                font=("Arial", 13, "bold")
            )
            rootHDL1.place(relx=0.5, rely=0.6, anchor="center")

            # -------- ROOT BODY --------
            rootBody = tk.Frame(root, width=500, height=300, bg="#346AC2")
            rootBody.place(y=80)

            # -------- INPUT FIELDS --------
            name = tk.Entry(rootBody)
            name.pack()

            stid = tk.Entry(rootBody)
            stid.pack()

            age = tk.Entry(rootBody)
            age.pack()

            # -------- SAVE DATA FUNCTION --------
            def save_data():
                df = pd.read_csv(FILE_NAME)

                new_row = {
                    "Name": name.get(),
                    "Student ID": stid.get(),
                    "Age": age.get()
                }

                new_df = pd.DataFrame([new_row])
                df = pd.concat([df, new_df], ignore_index=True)

                df.to_csv(FILE_NAME, index=False)

                name.delete(0, tk.END)
                stid.delete(0, tk.END)
                age.delete(0, tk.END)

            # -------- REPORT FUNCTION --------
            def show_report():
                report = tk.Tk()
                report.title("Student Report")
                report.geometry("500x300")

                df = pd.read_csv(FILE_NAME)

                text = tk.Text(report, width=60, height=15)
                text.pack()

                text.insert(tk.END, df.to_string(index=False))

            # -------- BUTTONS --------
            rootsubmit = ttk.Button(rootBody, text="Submit", command=save_data)
            rootsubmit.pack()

            rootreport = ttk.Button(rootBody, text="report", command=show_report)
            rootreport.pack()

        else:
            PSW_ERROR = tk.Tk()
            PSW_ERROR.title("Password Error")
            PSW_ERROR.geometry("400x90")
            tk.Label(PSW_ERROR, text="Password Is Not Correct").pack()

    else:
        Name_Error = tk.Tk()
        Name_Error.title("Name Error")
        Name_Error.geometry("400x90")
        tk.Label(Name_Error, text="NAMA WARADI YAKO").pack()

# ---------------- LOGIN BODY ----------------
Body = tk.Frame(psw, width=500, height=170, bg="#346AC2")
Body.place(y=80)

user_name_label = tk.Label(Body, text="User Name :", font=("Arial", 12))
user_name_label.place(x=55, y=30)

user_name_input = tk.Entry(Body, width=50)
user_name_input.place(x=180, y=30)

PSW_label = tk.Label(Body, text="Pass Word :", font=("Arial", 12))
PSW_label.place(x=55, y=80)

PSW_input = tk.Entry(Body, width=50)
PSW_input.place(x=180, y=80)

butn = tk.Frame(Body, width=400, height=25, bg="#346AC2")
butn.place(y=130, relx=0.5, anchor="center")

Submit = ttk.Button(butn, text="Submit", width=30, command=PSW_function)
Submit.place(x=0, y=0)

clear = ttk.Button(butn, text="Clear", width=30)
clear.place(x=210, y=0)

psw.mainloop()
