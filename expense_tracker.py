import os
import json
from datetime import datetime

# File to store expense data
EXPENSE_FILE = "expenses.json"
expense_data = []

def load_expenses():
    global expense_data
    if os.path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, "r") as file:
            expense_data = json.load(file)
        print("Loaded expense data.")
    else:
        print("No expense data to load.")

def save_expenses_to_file():
    with open(EXPENSE_FILE, "w") as file:
        json.dump(expense_data, file, indent=4)

def show_expenses():
    if expense_data:
        print("Expense History:")
        for entry in expense_data:
            date = entry['date']
            amount = entry['amount']
            category = entry['category']
            description = entry['description']
            print(f"{date}: {amount} | Category: {category} | Description: {description}")
    else:
        print("No expense entries available!")

def submit_expense():
    amount = float(input("Enter the expense amount: "))
    category = input("Enter the category of the expense (e.g., food, transport, bills): ")
    description = input("Enter a brief description of the expense: ")
    
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "amount": amount,
        "category": category,
        "description": description
    }
    
    expense_data.append(entry)
    print("Expense logged!")
    save_expenses_to_file()

def analyze_expenses():
    if expense_data:
        category_totals = {}
        for entry in expense_data:
            category = entry['category']
            amount = entry['amount']
            category_totals[category] = category_totals.get(category, 0) + amount
        
        print("Expense Analysis:")
        for category, total in category_totals.items():
            print(f"{category}: ${total:.2f}")
    else:
        print("No expenses to analyze!")

def expense_tracker_system():
    load_expenses()
    while True:
        print("\nExpense Tracker System")
        print("1. Log Expense")
        print("2. Show Expense History")
        print("3. Analyze Expenses")
        print("4. Exit")

        choice = input("Please select an option (1-4): ")

        if choice == "1":
            submit_expense()
        elif choice == "2":
            show_expenses()
        elif choice == "3":
            analyze_expenses()
        elif choice == "4":
            print("Exiting expense tracker system.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    expense_tracker_system()
