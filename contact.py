import tkinter as tk
from tkinter import ttk, messagebox
import os

CONTACT_FILE = "contacts.txt"

def load_contacts():
    if os.path.exists(CONTACT_FILE):
        with open(CONTACT_FILE, "r") as f:
            for idx, line in enumerate(f):
                name, phone = line.strip().split(" - ")
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                contact_tree.insert("", "end", values=(name, phone), tags=(tag,))

def save_contacts():
    with open(CONTACT_FILE, "w") as f:
        for child in contact_tree.get_children():
            name, phone = contact_tree.item(child)['values']
            f.write(f"{name} - {phone}\n")

def add_contact():
    name = name_var.get().strip()
    phone = phone_var.get().strip()
    if name and phone:
        count = len(contact_tree.get_children())
        tag = 'evenrow' if count % 2 == 0 else 'oddrow'
        contact_tree.insert("", "end", values=(name, phone), tags=(tag,))
        name_var.set("")
        phone_var.set("")
        save_contacts()
    else:
        messagebox.showwarning("Input Error", "Please enter both name and phone.")

def delete_contact():
    selected = contact_tree.selection()
    if selected:
        for item in selected:
            contact_tree.delete(item)
        save_contacts()
    else:
        messagebox.showwarning("Selection Error", "Please select a contact to delete.")

def edit_contact():
    selected = contact_tree.selection()
    if selected:
        item = selected[0]
        name, phone = contact_tree.item(item, 'values')
        name_var.set(name)
        phone_var.set(phone)
        contact_tree.delete(item)
    else:
        messagebox.showwarning("Selection Error", "Please select a contact to edit.")

def filter_contacts(*args):
    query = search_var.get().lower()
    contact_tree.delete(*contact_tree.get_children())
    if os.path.exists(CONTACT_FILE):
        with open(CONTACT_FILE, "r") as f:
            for idx, line in enumerate(f):
                name, phone = line.strip().split(" - ")
                if query in name.lower() or query in phone:
                    tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                    contact_tree.insert("", "end", values=(name, phone), tags=(tag,))

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    apply_theme()

def apply_theme():
    bg = "#2c3e50" if dark_mode else "#f4f4f4"
    fg = "#ecf0f1" if dark_mode else "#2d3436"
    entry_bg = "#34495e" if dark_mode else "#ffffff"
    accent_bg = "#3498db"

    root.configure(bg=bg)
    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame):
            widget.configure(bg=bg)
            for child in widget.winfo_children():
                if isinstance(child, tk.Label):
                    child.configure(bg=bg, fg=fg)
                elif isinstance(child, tk.Entry):
                    child.configure(bg=entry_bg, fg=fg, insertbackground=fg)
    search_entry.configure(bg=entry_bg, fg=fg, insertbackground=fg)
    theme_btn.configure(bg=accent_bg, fg="white")
    add_btn.configure(bg="#27ae60", fg="white")
    del_btn.configure(bg="#e74c3c", fg="white")
    edit_btn.configure(bg=accent_bg, fg="white")

    # Apply Treeview styling
    style.configure("Treeview", 
                    background="#ecf0f1" if not dark_mode else "#34495e", 
                    foreground="#2d3436" if not dark_mode else "#ecf0f1", 
                    fieldbackground="#ecf0f1" if not dark_mode else "#34495e")

    # ✅ Updated as requested
    if dark_mode:
        contact_tree.tag_configure('evenrow', background="#3d566e", foreground="#ecf0f1")
        contact_tree.tag_configure('oddrow', background="#2c3e50", foreground="#ecf0f1")
    else:
        contact_tree.tag_configure('evenrow', background="#ecf0f1", foreground="#2d3436")
        contact_tree.tag_configure('oddrow', background="#ffffff", foreground="#2d3436")

# --- Window Setup ---
root = tk.Tk()
root.title("📇 Enhanced Contact Book")
root.geometry("680x660")
root.resizable(False, False)
dark_mode = False

# Fonts
font_heading = ("Segoe UI", 18, "bold")
font_label = ("Segoe UI", 11)
font_entry = ("Segoe UI", 10)
font_button = ("Segoe UI", 10, "bold")

# Variables
name_var = tk.StringVar()
phone_var = tk.StringVar()
search_var = tk.StringVar()
search_var.trace("w", filter_contacts)

# --- Title ---
tk.Label(root, text="My Contact Book", font=font_heading, bg="#f4f4f4", fg="#2d3436").pack(pady=20)

# --- Search ---
search_frame = tk.Frame(root, bg="#f4f4f4")
search_frame.pack(pady=5)
tk.Label(search_frame, text="Search: ", font=font_label, bg="#f4f4f4").pack(side="left", padx=5)
search_entry = tk.Entry(search_frame, textvariable=search_var, font=font_entry, width=30, relief="flat", highlightthickness=1)
search_entry.pack(side="left", padx=5)
search_entry.config(highlightbackground="#ccc", highlightcolor="#3498db", bd=5)

# --- Form ---
form_frame = tk.Frame(root, bg="#f4f4f4")
form_frame.pack(pady=10)

tk.Label(form_frame, text="Name:", font=font_label, bg="#f4f4f4").grid(row=0, column=0, padx=10, pady=10, sticky="w")
name_entry = tk.Entry(form_frame, textvariable=name_var, font=font_entry, width=30, relief="flat", highlightthickness=1)
name_entry.grid(row=0, column=1, pady=10)
name_entry.config(bg="white", highlightbackground="#ccc", highlightcolor="#3498db", bd=5)

tk.Label(form_frame, text="Phone:", font=font_label, bg="#f4f4f4").grid(row=1, column=0, padx=10, pady=10, sticky="w")
phone_entry = tk.Entry(form_frame, textvariable=phone_var, font=font_entry, width=30, relief="flat", highlightthickness=1)
phone_entry.grid(row=1, column=1, pady=10)
phone_entry.config(bg="white", highlightbackground="#ccc", highlightcolor="#3498db", bd=5)

# --- Buttons ---
btn_frame = tk.Frame(root, bg="#f4f4f4")
btn_frame.pack(pady=10)

add_btn = tk.Button(btn_frame, text="Add Contact", font=font_button, command=add_contact, padx=10, pady=5)
add_btn.grid(row=0, column=0, padx=5)

edit_btn = tk.Button(btn_frame, text="Edit Contact", font=font_button, command=edit_contact, padx=10, pady=5)
edit_btn.grid(row=0, column=1, padx=5)

del_btn = tk.Button(btn_frame, text="Delete Contact", font=font_button, command=delete_contact, padx=10, pady=5)
del_btn.grid(row=0, column=2, padx=5)

theme_btn = tk.Button(btn_frame, text="Toggle Theme", font=font_button, command=toggle_theme, padx=10, pady=5)
theme_btn.grid(row=0, column=3, padx=5)

# --- Treeview ---
tree_frame = tk.Frame(root)
tree_frame.pack(pady=10)

style = ttk.Style()
style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))

contact_tree = ttk.Treeview(tree_frame, columns=("Name", "Phone"), show="headings", height=15)
contact_tree.heading("Name", text="Name")
contact_tree.heading("Phone", text="Phone")
contact_tree.column("Name", anchor="center", width=220)
contact_tree.column("Phone", anchor="center", width=220)
contact_tree.pack()

# Initialize
apply_theme()
load_contacts()
root.mainloop()
