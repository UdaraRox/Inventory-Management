import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os

DATA_DIR = "inventory_data"
os.makedirs(DATA_DIR, exist_ok=True)

# ==================================================
# DATABASE FUNCTIONS
# ==================================================
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
        "Date", "Item", "Supplier", "Remarks",
        "Quantity", "NetRate", "TotalCost"
    ])

# ==================================================
# LOGIN WINDOW
# ==================================================
def login_window():
    login = tk.Tk()
    login.title("Login Wellassa Inventory Management System")
    login.geometry("500x200")
    login.configure(bg="#F4F6F8")

    tk.Label(login, text="Login Wellassa Inventory Management System",
             font=("Arial", 16, "bold"), bg="#F4F6F8").pack(pady=10)

    tk.Label(login, text="Username", bg="#F4F6F8").pack()
    username_entry = tk.Entry(login)
    username_entry.pack(pady=5)

    tk.Label(login, text="Password", bg="#F4F6F8").pack()
    password_entry = tk.Entry(login, show="*")
    password_entry.pack(pady=5)

    def check_login():
        if username_entry.get() == "Admin" and password_entry.get() == "20031111":
            login.destroy()
            main_window()
        else:
            messagebox.showerror("Error", "Invalid Username or Password")

    tk.Button(login, text="Login", bg="#2C5DAA", fg="white",
              command=check_login, height=2, width=15).pack(pady=15)

    login.mainloop()

# ==================================================
# COMMON GRN FORM
# ==================================================
def open_grn_form(title, inventory_list):
    win = tk.Toplevel()
    win.title(title)
    win.geometry("650x620")
    win.configure(bg="#F4F6F8")

    tk.Label(win, text=title, font=("Arial", 14, "bold"), bg="#F4F6F8").pack(pady=10)

    form = tk.Frame(win, bg="#F4F6F8")
    form.pack(padx=20, pady=10, fill="x")
    form.columnconfigure(1, weight=1)

    date_var = tk.StringVar()
    item_var = tk.StringVar()
    supplier_var = tk.StringVar()
    remarks_var = tk.StringVar()
    qty_var = tk.StringVar()
    rate_var = tk.StringVar()
    transport_var = tk.StringVar()
    other_var = tk.StringVar()

    transport_kg = tk.StringVar(value="0.00")
    other_kg = tk.StringVar(value="0.00")
    net_rate = tk.StringVar(value="0.00")
    total_cost = tk.StringVar(value="0.00")

    def only_numbers(v):
        return v == "" or v.replace(".", "", 1).isdigit()

    vcmd = win.register(only_numbers)

    def calculate(*args):
        try:
            q = float(qty_var.get())
            r = float(rate_var.get())
            t = float(transport_var.get() or 0)
            o = float(other_var.get() or 0)

            tkg = t / q if q != 0 else 0
            okg = o / q if q != 0 else 0
            net = r + tkg + okg

            transport_kg.set(f"{tkg:.2f}")
            other_kg.set(f"{okg:.2f}")
            net_rate.set(f"{net:.2f}")
            total_cost.set(f"{net * q:.2f}")
        except:
            transport_kg.set("0.00")
            other_kg.set("0.00")
            net_rate.set("0.00")
            total_cost.set("0.00")

    for v in (qty_var, rate_var, transport_var, other_var):
        v.trace_add("write", calculate)

    def row(lbl, widget, r):
        tk.Label(form, text=lbl, bg="#F4F6F8").grid(row=r, column=0, sticky="w", pady=6)
        widget.grid(row=r, column=1, sticky="ew", pady=6)

    row("Date", tk.Entry(form, textvariable=date_var), 0)
    row("Inventory Type",
        ttk.Combobox(form, values=inventory_list,
                     textvariable=item_var, state="readonly"), 1)
    row("Supplier Name", tk.Entry(form, textvariable=supplier_var), 2)
    row("Remarks", tk.Entry(form, textvariable=remarks_var), 3)

    row("Quantity (KG)",
        tk.Entry(form, textvariable=qty_var,
                 validate="key", validatecommand=(vcmd, "%P")), 4)
    row("Rate (Rs / KG)",
        tk.Entry(form, textvariable=rate_var,
                 validate="key", validatecommand=(vcmd, "%P")), 5)

    row("Transport cost (Total Rs)",
        tk.Entry(form, textvariable=transport_var,
                 validate="key", validatecommand=(vcmd, "%P")), 6)
    tk.Label(form, text="Rs / KG", bg="#F4F6F8").grid(row=6, column=2)
    tk.Label(form, textvariable=transport_kg, bg="#F4F6F8").grid(row=6, column=3)

    row("Other costs (Total Rs)",
        tk.Entry(form, textvariable=other_var,
                 validate="key", validatecommand=(vcmd, "%P")), 7)
    tk.Label(form, text="Rs / KG", bg="#F4F6F8").grid(row=7, column=2)
    tk.Label(form, textvariable=other_kg, bg="#F4F6F8").grid(row=7, column=3)

    tk.Label(form, text="Net rate per KG",
             font=("Arial", 10, "bold"), bg="#F4F6F8").grid(row=8, column=0, pady=6)
    tk.Label(form, textvariable=net_rate,
             font=("Arial", 10, "bold"), bg="#F4F6F8").grid(row=8, column=1)

    tk.Label(form, text="Total Cost (Rs)",
             font=("Arial", 10, "bold"), bg="#F4F6F8").grid(row=9, column=0)
    tk.Label(form, textvariable=total_cost,
             font=("Arial", 10, "bold"), bg="#F4F6F8").grid(row=9, column=1)

    # -------- BUTTON FUNCTIONS --------
    def clear_fields():
        for v in (date_var, item_var, supplier_var, remarks_var,
                  qty_var, rate_var, transport_var, other_var):
            v.set("")
        transport_kg.set("0.00")
        other_kg.set("0.00")
        net_rate.set("0.00")
        total_cost.set("0.00")

    def submit_grn():
        item = item_var.get()
        if not item:
            messagebox.showerror("Error", "Please select an inventory type.")
            return
        try:
            record = {
                "Date": date_var.get(),
                "Item": item,
                "Supplier": supplier_var.get(),
                "Remarks": remarks_var.get(),
                "Quantity": float(qty_var.get()),
                "NetRate": float(net_rate.get()),
                "TotalCost": float(total_cost.get())
            }
            save_record(item, record)
            messagebox.showinfo("Success", f"GRN Record Saved for {item}!")
            win.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please make sure all numeric fields are correctly filled.")

    # -------- BUTTON BAR --------
    btns = tk.Frame(win, bg="#F4F6F8")
    btns.pack(pady=20)

    tk.Button(btns, text="Submit GRN", width=15, bg="#2C5DAA", fg="white",
              command=submit_grn).pack(side="left", padx=10)
    tk.Button(btns, text="Clear", width=15, bg="white",
              command=clear_fields).pack(side="left", padx=10)
    tk.Button(btns, text="Cancel", width=15, bg="white",
              command=win.destroy).pack(side="left", padx=10)

# ==================================================
# MENUS
# ==================================================
def open_grn_window():
    win = tk.Toplevel()
    win.title("Goods Received Notes")
    win.geometry("400x350")
    win.configure(bg="#F4F6F8")

    tk.Label(win, text="Goods Received Notes",
             font=("Arial", 14, "bold"), bg="#F4F6F8").pack(pady=15)

    tk.Button(win, text="Raw material (GRN)", height=2, bg="white",
              command=lambda: open_grn_form(
                  "Raw material Good receive Note",
                  ["p1", "p2", "p3", "p4", "p5", "p6", "p7"])
              ).pack(fill="x", padx=40, pady=5)

    tk.Button(win, text="Waste (PNWi)", height=2, bg="white",
              command=lambda: open_grn_form(
                  "Waste Good receive Note",
                  ["W1", "W2", "W3"])
              ).pack(fill="x", padx=40, pady=5)

    tk.Button(win, text="Finish Good (PNi)", height=2, bg="white",
              command=lambda: open_grn_form(
                  "Finish Good receive Note",
                  ["Fg1", "Fg2", "Fg3", "Fg4", "Fg5", "Fg6", "Fg7"])
              ).pack(fill="x", padx=40, pady=5)

    tk.Button(win, text="Packing Materials (GRNpm)", height=2, bg="white",
              command=lambda: open_grn_form(
                  "Packing Materials Good receive Note",
                  ["Pm1", "Pm2", "Pm3"])
              ).pack(fill="x", padx=40, pady=5)

def open_min_window():
    win = tk.Toplevel()
    win.title("Material Issue Notes")
    win.geometry("400x350")
    win.configure(bg="#F4F6F8")

    tk.Label(win, text="Material Issue Notes",
             font=("Arial", 14, "bold"), bg="#F4F6F8").pack(pady=15)

    for b in ["Raw material (PNo)", "Waste (WSN)",
              "Finish Good (SN)", "Packing Materials (PNpm)"]:
        tk.Button(win, text=b, height=2, bg="white").pack(fill="x", padx=40, pady=5)

# ==================================================
# BIN CARDS
# ==================================================
def open_bin_table(item):
    df = load_table(item)
    win = tk.Toplevel()
    win.title(f"Bin Card - {item}")
    win.geometry("900x400")
    win.configure(bg="#F4F6F8")

    tk.Label(win, text=f"Bin Card: {item}", font=("Arial", 14, "bold"), bg="#F4F6F8").pack(pady=10)

    frame = tk.Frame(win)
    frame.pack(fill="both", expand=True, padx=20, pady=10)

    tree = ttk.Treeview(frame, columns=list(df.columns), show="headings")
    tree.pack(side="left", fill="both", expand=True)

    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    vsb.pack(side="right", fill="y")
    tree.configure(yscrollcommand=vsb.set)

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))

    total_qty = df["Quantity"].sum() if not df.empty else 0
    total_val = df["TotalCost"].sum() if not df.empty else 0

    footer = tk.Frame(win, bg="#F4F6F8")
    footer.pack(fill="x", pady=10)

    tk.Label(footer, text=f"Total Quantity : {total_qty}",
             font=("Arial", 11, "bold"), bg="#F4F6F8").pack(side="left", padx=20)
    tk.Label(footer, text=f"Total Inventory Value : Rs {total_val:.2f}",
             font=("Arial", 11, "bold"), bg="#F4F6F8").pack(side="right", padx=20)


def open_bin_cards_menu():
    win = tk.Toplevel()
    win.title("Bin Cards")
    win.geometry("400x600")
    win.configure(bg="#F4F6F8")

    tk.Label(win, text="Select Item for Bin Card", font=("Arial", 14, "bold"), bg="#F4F6F8").pack(pady=15)

    groups = {
        "Raw Material": ["p1", "p2", "p3", "p4", "p5", "p6", "p7"],
        "Waste": ["W1", "W2", "W3"],
        "Finish Good": ["Fg1", "Fg2", "Fg3", "Fg4", "Fg5", "Fg6", "Fg7"],
        "Packing Materials": ["Pm1", "Pm2", "Pm3"]
    }

    # Scrollable frame 
    canvas = tk.Canvas(win, bg="#F4F6F8", highlightthickness=0)
    scrollbar = ttk.Scrollbar(win, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#F4F6F8")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=20)
    scrollbar.pack(side="right", fill="y")

    for group, items in groups.items():
        tk.Label(scrollable_frame, text=group, font=("Arial", 11, "bold"), 
                 bg="#F4F6F8", fg="#2C5DAA").pack(pady=(15, 5), anchor="w")
        for i in items:
            tk.Button(scrollable_frame, text=i, width=35, bg="white",
                      command=lambda x=i: open_bin_table(x)).pack(pady=2)

# ==================================================
# MAIN WINDOW
# ==================================================
def main_window():
    root = tk.Tk()
    root.title("Wellassa Inventory Management System")
    root.geometry("1100x600")
    root.configure(bg="#F4F6F8")

    header = tk.Frame(root, bg="#2C5DAA", height=60)
    header.pack(fill="x")

    tk.Label(header, text="Wellassa Inventory Management System",
             bg="#2C5DAA", fg="white",
             font=("Arial", 16, "bold")).pack(pady=18)

    main = tk.Frame(root, bg="#F4F6F8")
    main.pack(fill="both", expand=True, padx=20, pady=20)
    main.columnconfigure((0, 1, 2), weight=1)

    def card(parent, title):
        f = tk.Frame(parent, bg="white")
        f.pack(fill="both", expand=True)
        tk.Label(f, text=title, bg="white",
                 font=("Arial", 12, "bold")).pack(pady=10)
        ttk.Separator(f).pack(fill="x", padx=20)
        return f

    style = {"bg": "#E9ECEF", "bd": 0, "height": 2}

    # Processes
    p = tk.Frame(main, bg="#F4F6F8")
    p.grid(row=0, column=0, sticky="nsew", padx=10)
    pc = card(p, "Processes")
    tk.Button(pc, text="Goods Received Notes",
              command=open_grn_window, **style).pack(fill="x", padx=30, pady=10)
    tk.Button(pc, text="Material Issue Note",
              command=open_min_window, **style).pack(fill="x", padx=30, pady=10)

    # Reports
    r = tk.Frame(main, bg="#F4F6F8")
    r.grid(row=0, column=1, sticky="nsew", padx=10)
    rc = card(r, "Reports")
    
    # Linked the styled open_bin_cards_menu to this button
    tk.Button(rc, text="Bin Card", command=open_bin_cards_menu, **style).pack(fill="x", padx=30, pady=10)
    tk.Button(rc, text="Goods Received Notes", **style).pack(fill="x", padx=30, pady=10)
    tk.Button(rc, text="Material Issue Note", **style).pack(fill="x", padx=30, pady=10)

    # On Hand Quantity
    o = tk.Frame(main, bg="#F4F6F8")
    o.grid(row=0, column=2, sticky="nsew", padx=10)
    oc = card(o, "On Hand Quantity Report")

    for s in ["Stock A", "Stock B", "Stock C"]:
        f = tk.Frame(oc, bg="white", bd=1, relief="solid")
        f.pack(fill="x", padx=20, pady=10)
        tk.Label(f, text=s, font=("Arial", 10, "bold"),
                 bg="white").pack(anchor="w", padx=10)
        tk.Label(f, text="KG : 000", bg="white").pack(anchor="w", padx=20)
        tk.Label(f, text="RS : 000.00", bg="white").pack(anchor="w", padx=20)

    root.mainloop()

# ==================================================
# START APP
# ==================================================
if __name__ == "__main__":
    login_window()