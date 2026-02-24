import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os

DATA_DIR = "inventory_data"
os.makedirs(DATA_DIR, exist_ok=True)

# ----------------- DATABASE FUNCTIONS -----------------
def save_record(item, record):
    file = f"{DATA_DIR}/{item}.csv"
    df = pd.DataFrame([record])
    if os.path.exists(file):
        df.to_csv(file, mode="a", header=False, index=False)
    else:
        df.to_csv(file, index=False)

def load_table(item):
    file = f"{DATA_DIR}/{item}.csv"
    if os.path.exists(file):
        return pd.read_csv(file)
    return pd.DataFrame(columns=[
        "Date","Item","Supplier","Remarks",
        "Quantity","NetRate","TotalCost"
    ])

# ----------------- BIN CARD VIEW -----------------
def open_bin_table(item):
    df = load_table(item)

    win = tk.Toplevel()
    win.title(f"Bin Card - {item}")
    win.geometry("900x400")

    tree = ttk.Treeview(win, columns=list(df.columns), show="headings")
    tree.pack(fill="both", expand=True)

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))

    total_qty = df["Quantity"].sum()
    total_val = df["TotalCost"].sum()

    footer = tk.Frame(win)
    footer.pack(fill="x")

    tk.Label(footer, text=f"Total Quantity : {total_qty}",
             font=("Arial",10,"bold")).pack(side="left", padx=20)
    tk.Label(footer, text=f"Total Inventory Value : Rs {total_val:.2f}",
             font=("Arial",10,"bold")).pack(side="right", padx=20)

# ----------------- BIN CARD MENU -----------------
def open_bin_cards():
    win = tk.Toplevel()
    win.title("Bin Cards")
    win.geometry("400x550")

    groups = {
        "Raw Material": ["P1","P2","P3","P4","P5","P6","P7"],
        "Waste": ["W1","W2","W3"],
        "Finish Good": ["Fg1","Fg2","Fg3","Fg4","Fg5","Fg6","Fg7"],
        "Packing Materials": ["Pm1","Pm2","Pm3"]
    }

    for group, items in groups.items():
        tk.Label(win, text=group, font=("Arial",11,"bold")).pack(pady=5)
        for i in items:
            tk.Button(win, text=i, width=20,
                      command=lambda x=i: open_bin_table(x)).pack(pady=2)

# ----------------- GRN FORM -----------------
def open_grn_form(title, inventory_list):
    win = tk.Toplevel()
    win.title(title)
    win.geometry("650x620")

    vars = {k: tk.StringVar() for k in
        ["date","item","supplier","remarks","qty","rate","transport","other"]}

    net_rate = tk.StringVar(value="0.00")
    total_cost = tk.StringVar(value="0.00")

    def calculate(*_):
        try:
            q = float(vars["qty"].get())
            r = float(vars["rate"].get())
            t = float(vars["transport"].get() or 0)
            o = float(vars["other"].get() or 0)
            net = r + (t+o)/q
            net_rate.set(f"{net:.2f}")
            total_cost.set(f"{net*q:.2f}")
        except:
            net_rate.set("0.00")
            total_cost.set("0.00")

    for k in ["qty","rate","transport","other"]:
        vars[k].trace_add("write", calculate)

    form = tk.Frame(win)
    form.pack(padx=20, pady=10, fill="x")
    form.columnconfigure(1, weight=1)

    def row(label, var, r):
        tk.Label(form, text=label).grid(row=r, column=0, sticky="w", pady=5)
        tk.Entry(form, textvariable=var).grid(row=r, column=1, sticky="ew")

    row("Date", vars["date"], 0)
    ttk.Combobox(form, values=inventory_list,
                 textvariable=vars["item"], state="readonly").grid(row=1,column=1,sticky="ew")
    tk.Label(form, text="Inventory Type").grid(row=1,column=0,sticky="w")

    row("Supplier", vars["supplier"], 2)
    row("Remarks", vars["remarks"], 3)
    row("Quantity", vars["qty"], 4)
    row("Rate", vars["rate"], 5)
    row("Transport Cost", vars["transport"], 6)
    row("Other Cost", vars["other"], 7)

    tk.Label(form, text="Net Rate / KG").grid(row=8,column=0)
    tk.Label(form, textvariable=net_rate).grid(row=8,column=1)

    tk.Label(form, text="Total Cost").grid(row=9,column=0)
    tk.Label(form, textvariable=total_cost).grid(row=9,column=1)

    def submit():
        item = vars["item"].get()
        if not item:
            messagebox.showerror("Error","Select inventory item")
            return
        record = {
            "Date": vars["date"].get(),
            "Item": item,
            "Supplier": vars["supplier"].get(),
            "Remarks": vars["remarks"].get(),
            "Quantity": float(vars["qty"].get()),
            "NetRate": float(net_rate.get()),
            "TotalCost": float(total_cost.get())
        }
        save_record(item, record)
        messagebox.showinfo("Saved","GRN Record Saved")
        win.destroy()

    btns = tk.Frame(win)
    btns.pack(pady=20)
    tk.Button(btns, text="Submit", width=15, command=submit).pack(side="left", padx=10)
    tk.Button(btns, text="Cancel", width=15, command=win.destroy).pack(side="left")

# ----------------- GOODS RECEIVED NOTES -----------------
def open_grn_window():
    win = tk.Toplevel()
    win.title("Goods Received Notes")
    win.geometry("400x300")

    tk.Button(win,text="Raw Material",
        command=lambda: open_grn_form("Raw Material GRN",
            ["P1","P2","P3","P4","P5","P6","P7"])).pack(fill="x",pady=5)

    tk.Button(win,text="Waste",
        command=lambda: open_grn_form("Waste GRN",
            ["W1","W2","W3"])).pack(fill="x",pady=5)

    tk.Button(win,text="Finish Good",
        command=lambda: open_grn_form("Finish Good GRN",
            ["Fg1","Fg2","Fg3","Fg4","Fg5","Fg6","Fg7"])).pack(fill="x",pady=5)

    tk.Button(win,text="Packing Materials",
        command=lambda: open_grn_form("Packing Material GRN",
            ["Pm1","Pm2","Pm3"])).pack(fill="x",pady=5)

# ----------------- MAIN WINDOW -----------------
def main_window():
    root = tk.Tk()
    root.title("Wellassa Inventory Management System")
    root.geometry("1100x600")

    tk.Button(root, text="Goods Received Notes",
              command=open_grn_window, height=2).pack(pady=10)

    tk.Button(root, text="Bin Card",
              command=open_bin_cards, height=2).pack(pady=10)

    root.mainloop()

# ----------------- LOGIN -----------------
def login_window():
    login = tk.Tk()
    login.geometry("300x200")
    tk.Label(login, text="Username").pack()
    u = tk.Entry(login); u.pack()
    tk.Label(login, text="Password").pack()
    p = tk.Entry(login, show="*"); p.pack()

    def go():
        if u.get()=="Admin" and p.get()=="20031111":
            login.destroy()
            main_window()
        else:
            messagebox.showerror("Error","Invalid Login")

    tk.Button(login, text="Login", command=go).pack(pady=10)
    login.mainloop()

login_window()
