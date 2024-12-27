from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Global Variables to hold income and expenses
income = 0
expenses = []


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
        flash("Please add income first!", 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
            category = request.form['category'].lower()
            if amount < 0:
                flash("Expense cannot be negative.", 'error')
            elif category not in ["essential", "non-essential"]:
                flash("Category must be 'essential' or 'non-essential'.", 'error')
            else:
                expenses.append({"amount": amount, "category": category})
                flash(f"Expense of £{amount} ({category}) saved!", 'success')
                return redirect(url_for('index'))
        except ValueError:
            flash("Invalid expense. Please enter a number.", 'error')

    return render_template("add_expense.html")


@app.route('/view_summary')
def view_summary():
    """Display budget summary."""
    global income, expenses
    if not expenses:
        flash("No expenses added yet.", 'info')
        return redirect(url_for('index'))

    total_expenses = sum(e["amount"] for e in expenses)
    essential_expenses = sum(e["amount"] for e in expenses if e["category"] == "essential")
    non_essential_expenses = sum(e["amount"] for e in expenses if e["category"] == "non-essential")
    remaining_budget = income - total_expenses

    summary = {
        "total_income": income,
        "total_expenses": total_expenses,
        "essential_expenses": essential_expenses,
        "non_essential_expenses": non_essential_expenses,
        "remaining_budget": remaining_budget,
    }

    if remaining_budget > 0:
        summary["message"] = "Great! You are under budget. Consider saving the surplus!"
    else:
        summary["message"] = "Warning! You are over budget. Reassess your expenses."

    return render_template("view_summary.html", summary=summary)


if __name__ == "__main__":
    app.run(debug=True)
