import pandas as pd
import tkinter as tk
root = tk.Tk()
root.geometry("500x500")


def function():
    xy= input.get()
    print(xy)   

input=tk.Entry(root)
input.pack()
output=tk.Label(root ).pack()
   

b1=tk.Button(text="Print Output",command=function).pack()

#b2=tk.Button(text="Goods Received Notes2",).pack()






root.mainloop()