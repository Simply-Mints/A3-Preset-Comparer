import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from presetparser import get_mod_list

root = tk.Tk()
root.title("Arma 3 Preset Comparer")
root.geometry('800x500')
root.state("zoomed")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

master_mods = []
compare_mods = []

def load_preset(target_label, target_tree):

    filename = filedialog.askopenfilename(
        title='Select A Preset File',
        filetypes=(("Preset files", "*.html *.txt"), ("All files", "*.*"))
    )
    if not filename:
        return
    
    target_label.config(text=filename)

    mod_list = get_mod_list(filename)

    # This is cooked
    if target_label == left_label:
        global master_mods
        master_mods = mod_list
    elif target_label == right_label:
        global compare_mods
        compare_mods = mod_list


    for item in target_tree.get_children():
        target_tree.delete(item)

    for mod in mod_list:
        target_tree.insert("", "end", values=(mod["DisplayName"], mod["Link"]))

def compare_preset(master_mods, compare_mods, left_tree, right_tree):

    # clear previous tags
    for child in left_tree.get_children():
        left_tree.item(child, tags=())
    for child in right_tree.get_children():
        right_tree.item(child, tags=())

    master_set = {(m["DisplayName"], m["Link"]) for m in master_mods}
    compare_set = {(m["DisplayName"], m["Link"]) for m in compare_mods}

    missing_in_compare = master_set - compare_set
    extra_in_compare   = compare_set - master_set

    for child in left_tree.get_children():
        vals = left_tree.item(child, "values")
        tup = (vals[0], vals[1])

        if tup in missing_in_compare:
             left_tree.item(child, tags=("missing",))

    for child in right_tree.get_children():
        vals = right_tree.item(child, "values")
        tup = (vals[0], vals[1])
        if tup in extra_in_compare:
            right_tree.item(child, tags=("extra",))

left_frame = ttk.Frame(root, padding=10, borderwidth=5, relief='solid')
left_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

left_label = ttk.Label(left_frame, text='Empty Preset')
left_label.grid(sticky='n')

left_button_loadfile = ttk.Button(left_frame, text='Load Preset', default='active', command=lambda: load_preset(left_label, left_tree))
left_button_loadfile.grid(row=1, sticky='n')

left_frame.grid_rowconfigure(2, weight=1)
left_frame.grid_columnconfigure(0, weight=1)

left_tree = ttk.Treeview(left_frame, columns=('DisplayName', 'Link'), show='headings')
left_tree.heading("DisplayName", text="Display Name")
left_tree.heading("Link", text="Link")
left_tree.column("DisplayName", width=300)
left_tree.column("Link", width=500)
left_tree.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')

left_tree.tag_configure('missing', background='tomato')

left_button_compare = ttk.Button(left_frame, text='Compare', default='active', command=lambda: compare_preset(master_mods, compare_mods, left_tree, right_tree))
left_button_compare.grid(row=1, sticky='ne')

right_frame = ttk.Frame(root, padding=10, borderwidth=5, relief='solid')
right_frame.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

right_label = ttk.Label(right_frame, text='Empty Preset')
right_label.grid(sticky='n')

right_button_loadfile = ttk.Button(right_frame, text='Load Preset', default='active', command=lambda: load_preset(right_label, right_tree))
right_button_loadfile.grid(row=1, sticky='n')

right_frame.grid_rowconfigure(2, weight=1)
right_frame.grid_columnconfigure(0, weight=1)

right_tree = ttk.Treeview(right_frame, columns=('DisplayName', 'Link'), show='headings')
right_tree.heading("DisplayName", text="Display Name")
right_tree.heading("Link", text="Link")
right_tree.column("DisplayName", width=300)
right_tree.column("Link", width=500)
right_tree.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')

right_tree.tag_configure('extra', background='lightblue')

root.mainloop()