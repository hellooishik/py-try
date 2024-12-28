import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Global variables to hold income and expenses
income = 0
expenses = []
# Dummy data, this would be replaced by actual data from a database or session
summary_data = {
    'total_income': 0,
    'total_expenses': 0,
    'essential_expenses': 0,
    'non_essential_expenses': 0,
    'remaining_budget': 0,
    'message': 'Please add income and expenses to view the summary.'
}

@app.route('/')
def index():
    """Main page that redirects to the dashboard."""
    return render_template("index.html")

@app.route('/add_income', methods=['GET', 'POST'])
def add_income():
    """Page to add income."""
    global income
    if request.method == 'POST':
        try:
            income = float(request.form['income'])
            if income < 0:
                flash("Income cannot be negative.", 'error')
            else:
                flash(f"Income of £{income} saved!", 'success')
                return redirect(url_for('index'))
        except ValueError:
            flash("Invalid income. Please enter a number.", 'error')
    return render_template("add_income.html")

@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    """Page to add expense."""
    global expenses, income

    if income == 0:
        flash("Please add income first!", "error")
        return redirect(url_for('index'))

    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
            category = request.form['category']

            if amount <= 0:
                flash("Expense amount cannot be zero or negative.", 'error')
                return redirect(url_for('add_expense'))

            if category not in ["essential", "non-essential"]:
                flash("Category must be 'essential' or 'non-essential'.", 'error')
                return redirect(url_for('add_expense'))

            # Append the expense to the expenses list
            expenses.append({"amount": amount, "category": category})

            flash(f"Expense of £{amount} added under '{category}' category.", "success")

        except ValueError:
            flash("Invalid input. Please enter a valid amount.", 'error')

    return render_template("add_expense.html", expenses=expenses)


@app.route('/view_summary')
def view_summary():
    """Display budget summary."""
    global income, expenses

    # Check if income and expenses are set
    if not income or not expenses:
        # If income or expenses are missing, redirect the user to the "Add Income and Expenses" page
        return redirect(url_for('index'))  # Assuming index is the page to add income/expenses
    
    # Calculate total expenses and categorize them
    total_expenses = sum(expense['amount'] for expense in expenses)
    essential_expenses = sum(expense['amount'] for expense in expenses if expense['category'] == 'essential')
    non_essential_expenses = sum(expense['amount'] for expense in expenses if expense['category'] == 'non-essential')
    remaining_budget = income - total_expenses

    # Create the summary dictionary
    summary = {
        "total_income": income,
        "total_expenses": total_expenses,
        "essential_expenses": essential_expenses,
        "non_essential_expenses": non_essential_expenses,
        "remaining_budget": remaining_budget,
    }

    # Add a message based on the remaining budget
    if remaining_budget > 0:
        summary["message"] = "Great! You are under budget. Consider saving the surplus!"
    else:
        summary["message"] = "Warning! You are over budget. Reassess your expenses."

    # Render the summary template with the summary data
    return render_template("view_summary.html", summary=summary)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)