class BudgetPlanner:
    def __init__(self, initial_budget=0):
        self.budget = initial_budget
        self.income = 0
        self.expenses = {}

    def add_income(self, amount):
        """Add income to the budget."""
        self.income += amount
        self.budget += amount
        print(f"Added income: ${amount:.2f}")

    def add_expense(self, category, amount):
        """Add an expense under a specific category."""
        if category not in self.expenses:
            self.expenses[category] = 0
        self.expenses[category] += amount
        self.budget -= amount
        print(f"Added expense: ${amount:.2f} for {category}")

    def view_expenses(self):
        """Display all expenses by category."""
        if not self.expenses:
            print("No expenses recorded yet.")
        else:
            print("Expenses by category:")
            for category, amount in self.expenses.items():
                print(f"  {category}: ${amount:.2f}")

    def view_summary(self):
        """Display the current budget summary."""
        print(f"\nIncome: ${self.income:.2f}")
        self.view_expenses()
        print(f"Remaining Budget: ${self.budget:.2f}\n")

# Testing the BudgetPlanner class
if __name__ == "__main__":
    # Create a budget planner instance with an initial budget
    planner = BudgetPlanner()

    # Test adding income
    planner.add_income(1000)
    
    # Test adding expenses
    planner.add_expense("Groceries", 200)
    planner.add_expense("Rent", 500)
    planner.add_expense("Utilities", 100)
    
    # Test viewing the budget summary
    planner.view_summary()

    # Test adding more expenses and income
    planner.add_expense("Entertainment", 50)
    planner.add_income(200)
    
    # Final summary
    planner.view_summary()
