import sqlite3
from tkinter import *
from tkinter import messagebox, ttk
from datetime import datetime

conn = sqlite3.connect('expenses.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        category TEXT,
        amount REAL,
        description TEXT
    )
''')
conn.commit()

def add_expense():
    date = date_entry.get()
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    category = category_entry.get()
    amount = amount_entry.get()
    description = description_entry.get()
    
    if category and amount:
        try:
            amount = float(amount)
            c.execute('''
                INSERT INTO expenses (date, category, amount, description)
                VALUES (?, ?, ?, ?)
            ''', (date, category, amount, description))
            conn.commit()
            messagebox.showinfo("Success", "Expense added successfully!")
            view_expenses()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
    else:
        messagebox.showerror("Error", "Please fill out all fields")

def view_expenses():
    for row in tree.get_children():
        tree.delete(row)

    c.execute('SELECT * FROM expenses')
    rows = c.fetchall()
    for row in rows:
        tree.insert("", END, values=row)

def view_expenses_by_category():
    category = category_filter_entry.get()
    if category:
        for row in tree.get_children():
            tree.delete(row)
        c.execute('SELECT * FROM expenses WHERE category = ?', (category,))
        rows = c.fetchall()
        for row in rows:
            tree.insert("", END, values=row)
    else:
        messagebox.showerror("Error", "Please enter a category to filter")

root = Tk()
root.title("Expense Tracker")

Label(root, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=5)
date_entry = Entry(root)
date_entry.grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Category:").grid(row=1, column=0, padx=10, pady=5)
category_entry = Entry(root)
category_entry.grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Amount:").grid(row=2, column=0, padx=10, pady=5)
amount_entry = Entry(root)
amount_entry.grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Description:").grid(row=3, column=0, padx=10, pady=5)
description_entry = Entry(root)
description_entry.grid(row=3, column=1, padx=10, pady=5)

add_button = Button(root, text="Add Expense", command=add_expense)
add_button.grid(row=4, column=0, columnspan=2, pady=10)

columns = ('ID', 'Date', 'Category', 'Amount', 'Description')
tree = ttk.Treeview(root, columns=columns, show='headings')
tree.heading('ID', text='ID')
tree.heading('Date', text='Date')
tree.heading('Category', text='Category')
tree.heading('Amount', text='Amount')
tree.heading('Description', text='Description')

tree.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

scrollbar = ttk.Scrollbar(root, orient=VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=5, column=4, sticky='ns')

Label(root, text="Filter by Category:").grid(row=6, column=0, padx=10, pady=5)
category_filter_entry = Entry(root)
category_filter_entry.grid(row=6, column=1, padx=10, pady=5)

filter_button = Button(root, text="Filter", command=view_expenses_by_category)
filter_button.grid(row=6, column=2, pady=5)

view_all_button = Button(root, text="View All", command=view_expenses)
view_all_button.grid(row=6, column=3, pady=5)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)

view_expenses()

root.mainloop()

conn.close()