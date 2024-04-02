import pandas as pd
from tkinter import *
from tkinter import ttk

def load_csv(file_path):
    data = pd.read_csv(file_path, sep=';', names=['Pattern Name', 'Frequency', 'Power'])
    data_sorted = data.sort_values(by=['Pattern Name', 'Frequency'])
    return data_sorted

def display_data(data):
    root = Tk()
    root.title("Posortowane dane CSV")
    root.geometry("600x400")

    frame = Frame(root)
    frame.pack(fill=BOTH, expand=True)

    tree = ttk.Treeview(frame, columns=list(data.columns), show='headings')
    tree.pack(side=LEFT, fill=BOTH, expand=True)

    for col in data.columns:
        tree.heading(col, text=col)

    for _, row in data.iterrows():
        tree.insert("", "end", values=list(row))

    scrollbar = Scrollbar(frame, orient=VERTICAL, command=tree.yview)
    scrollbar.pack(side=RIGHT, fill='y')
    tree.configure(yscrollcommand=scrollbar.set)

    root.mainloop()

file_path =open(r'C:\Users\marsieradzka\Desktop\ris\Python_RIS\wyniki\18_03_24_03\19_03_reflection_20cm_3_5cm_17cm.csv')
data_sorted = load_csv(file_path)
display_data(data_sorted)
