import sqlite3
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

def add_expense(date, category, amount, description):
    c.execute('''
        INSERT INTO expenses (date, category, amount, description)
        VALUES (?, ?, ?, ?)
    ''', (date, category, amount, description))
    conn.commit()
    print(f"Expense added: {category} - {amount} on {date}")

def view_expenses():
    c.execute('SELECT * FROM expenses')
    rows = c.fetchall()
    if rows:
        for row in rows:
            print(f"ID: {row[0]}, Date: {row[1]}, Category: {row[2]}, Amount: {row[3]}, Description: {row[4]}")
    else:
        print("No expenses recorded.")

def view_expenses_by_category(category):
    c.execute('SELECT * FROM expenses WHERE category = ?', (category,))
    rows = c.fetchall()
    if rows:
        print(f"Expenses in category '{category}':")
        for row in rows:
            print(f"Date: {row[1]}, Amount: {row[3]}, Description: {row[4]}")
    else:
        print(f"No expenses found in category '{category}'.")

def show_menu():
    print("\nExpense Tracker")
    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. View Expenses by Category")
    print("4. Exit")

def main():
    while True:
        show_menu()
        choice = input("Enter your choice: ")
        
        if choice == '1':
            date = input("Enter date (YYYY-MM-DD) or press enter for today: ")
            if not date:
                date = datetime.now().strftime("%Y-%m-%d")
            category = input("Enter category (e.g., Food, Travel, Shopping): ")
            amount = float(input("Enter amount: "))
            description = input("Enter description: ")
            add_expense(date, category, amount, description)
        
        elif choice == '2':
            view_expenses()
        
        elif choice == '3':
            category = input("Enter category to filter: ")
            view_expenses_by_category(category)
        
        elif choice == '4':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

conn.close()
