import tkinter as tk
from tkinter import ttk
import json

import PP_Sladosti_warehouse

DRIED_FRUITS_FILE = 'dried_fruits.json'
NUTS_FILE = 'nuts.json'
OTHER_FILE = 'other.json'

dried_fruits = PP_Sladosti_warehouse.dried_fruits
nuts = PP_Sladosti_warehouse.nuts
other = PP_Sladosti_warehouse.other

def load_data(name):
    try:
        with open(name, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data(name):
    return

def update_fruits_list():
    fruits_list.delete(0, tk.END)
    for k, v in dried_fruits_data.items():
        fruits_list.insert(tk.END, f"{v[1]} - {v[0]}")

def update_nuts_list():
    nuts_list.delete(0, tk.END)
    for k, v in nuts_data.items():
        nuts_list.insert(tk.END, f"{v[1]} - {v[0]}")

def update_other_list():
    other_list.delete(0, tk.END)
    for k, v in other_data.items():
        other_list.insert(tk.END, f"{v[1]} - {v[0]}")

window = tk.Tk()
window.title("PP Sladosty warehouse")
window.geometry('800x600')

dried_fruits_data = load_data(DRIED_FRUITS_FILE)
nuts_data = load_data(NUTS_FILE)
other_data = load_data(OTHER_FILE)

notebook = ttk.Notebook(window)
notebook.pack(fill=tk.BOTH, expand=True)

frame_main = tk.Frame(notebook, padx=5, pady=5)
notebook.add(frame_main, text="Warehouse")

frame_data = tk.Frame(frame_main, padx=5, pady=5)
frame_data.pack(side=tk.TOP)

frame_fruits = tk.Frame(frame_data)
frame_fruits.pack(side=tk.LEFT, padx=5)

fruits_label = tk.Label(frame_fruits, text="Dried fruits:")
fruits_label.pack(anchor=tk.N, padx=5)

fruits_list = tk.Listbox(frame_fruits, height=15, width=30, bd=6)
fruits_list.pack(anchor=tk.W)

update_fruits_list()

frame_nuts = tk.Frame(frame_data)
frame_nuts.pack(side=tk.LEFT, padx=5)

nuts_label = tk.Label(frame_nuts, text="Nuts:")
nuts_label.pack(anchor=tk.N, padx=5)

nuts_list = tk.Listbox(frame_nuts, height=15, width=30)
nuts_list.pack(anchor=tk.CENTER)

update_nuts_list()

frame_other = tk.Frame(frame_data)
frame_other.pack(side=tk.LEFT, padx=5)

other_label = tk.Label(frame_other, text="Other:")
other_label.pack(anchor=tk.N, padx=5)

other_list = tk.Listbox(frame_other, height=15, width=30)
other_list.pack(anchor=tk.CENTER)

update_other_list()

frame_planning = tk.Frame(notebook, padx=5, pady=5)
notebook.add(frame_planning, text="Planning")

window.mainloop()
