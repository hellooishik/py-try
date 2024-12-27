import tkinter as tk
from tkinter import messagebox

# Initialize main application
class PersonalFinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Calculator")
        self.income = 0
        self.expenses = []

        # UI Elements
        self.create_main_menu()

    def create_main_menu(self):
        """Creates the main menu layout."""
        tk.Label(self.root, text="Personal Finance Calculator", font=("Helvetica", 16, "bold")).pack(pady=10)
        
        tk.Button(self.root, text="Add Income", width=20, command=self.add_income_ui).pack(pady=5)
        tk.Button(self.root, text="Add Expense", width=20, command=self.add_expense_ui).pack(pady=5)
        tk.Button(self.root, text="View Summary", width=20, command=self.view_summary).pack(pady=5)
        tk.Button(self.root, text="Exit", width=20, command=self.root.quit).pack(pady=20)

    def add_income_ui(self):
        """UI for adding income."""
        self.clear_screen()
        tk.Label(self.root, text="Enter Your Monthly Income", font=("Helvetica", 14)).pack(pady=10)
        income_entry = tk.Entry(self.root, font=("Helvetica", 12))
        income_entry.pack(pady=5)

        def save_income():
            try:
                income = float(income_entry.get())
                if income < 0:
                    messagebox.showerror("Error", "Income cannot be negative.")
                    return
                self.income = income
                messagebox.showinfo("Success", f"Income of £{income} saved!")
                self.return_to_main_menu()
            except ValueError:
                messagebox.showerror("Error", "Invalid income. Please enter a number.")

        tk.Button(self.root, text="Save Income", command=save_income).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.return_to_main_menu).pack(pady=10)

    def add_expense_ui(self):
        """UI for adding expenses."""
        if self.income == 0:
            messagebox.showerror("Error", "Please add income first!")
            return
        
        self.clear_screen()
        tk.Label(self.root, text="Enter Expense Details", font=("Helvetica", 14)).pack(pady=10)

        tk.Label(self.root, text="Amount", font=("Helvetica", 12)).pack(pady=5)
        amount_entry = tk.Entry(self.root, font=("Helvetica", 12))
        amount_entry.pack(pady=5)

        tk.Label(self.root, text="Category (essential/non-essential)", font=("Helvetica", 12)).pack(pady=5)
        category_entry = tk.Entry(self.root, font=("Helvetica", 12))
        category_entry.pack(pady=5)

        def save_expense():
            try:
                amount = float(amount_entry.get())
                category = category_entry.get().lower()
                if amount < 0:
                    messagebox.showerror("Error", "Expense cannot be negative.")
                    return
                if category not in ["essential", "non-essential"]:
                    messagebox.showerror("Error", "Category must be 'essential' or 'non-essential'.")
                    return
                self.expenses.append({"amount": amount, "category": category})
                messagebox.showinfo("Success", f"Expense of £{amount} ({category}) saved!")
                self.return_to_main_menu()
            except ValueError:
                messagebox.showerror("Error", "Invalid expense. Please enter a number.")

        tk.Button(self.root, text="Save Expense", command=save_expense).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.return_to_main_menu).pack(pady=10)

    def view_summary(self):
        """Displays the budget summary."""
        if not self.expenses:
            messagebox.showinfo("Summary", "No expenses added yet.")
            return

        total_expenses = sum(e["amount"] for e in self.expenses)
        essential_expenses = sum(e["amount"] for e in self.expenses if e["category"] == "essential")
        non_essential_expenses = sum(e["amount"] for e in self.expenses if e["category"] == "non-essential")
        remaining_budget = self.income - total_expenses

        summary = (
            f"--- Budget Summary ---\n"
            f"Total Income: £{self.income}\n"
            f"Total Expenses: £{total_expenses}\n"
            f"  - Essential: £{essential_expenses}\n"
            f"  - Non-Essential: £{non_essential_expenses}\n"
            f"Remaining Budget: £{remaining_budget}\n"
        )
        if remaining_budget > 0:
            summary += "Great! You are under budget. Consider saving the surplus!"
        else:
            summary += "Warning! You are over budget. Reassess your expenses."

        messagebox.showinfo("Summary", summary)

    def clear_screen(self):
        """Clears all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def return_to_main_menu(self):
        """Returns to the main menu."""
        self.clear_screen()
        self.create_main_menu()


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = PersonalFinanceApp(root)
    root.geometry("400x400")
    root.mainloop()
