
def calculate_totals(transactions):
    """Calculate total income, expenses and balance."""

    total_income = 0
    total_expenses = 0

    for transaction in transactions:
        transaction_type = transaction[1]
        amount = transaction[2]

        if transaction_type == "Income":
            total_income += amount
        elif transaction_type == "Expense":
            total_expenses += amount

    balance = total_income - total_expenses

    return total_income, total_expenses, balance


def search_transactions(transactions, keyword):
    """Search transactions by description or category."""

    keyword = keyword.lower()

    results = []

    for transaction in transactions:
        description = transaction[5] or ""
        category = transaction[3]

        if (keyword in description.lower()
                or keyword in category.lower()):
            results.append(transaction)

    return results


def filter_by_month(transactions, month):
    """Filter transactions by month (YYYY-MM)."""

    results = []

    for transaction in transactions:
        transaction_date = transaction[4]

        if transaction_date.startswith(month):
            results.append(transaction)

    return results


def calculate_monthly_summary(transactions, month):
    """Calculate income, expenses and balance for a month."""

    monthly_transactions = filter_by_month(transactions, month)

    return calculate_totals(monthly_transactions)


def calculate_category_summary(transactions):
    """Calculate total expenses for each category."""

    category_totals = {}

    for transaction in transactions:
        transaction_type = transaction[1]
        amount = transaction[2]
        category = transaction[3]

        if transaction_type == "Expense":
            if category not in category_totals:
                category_totals[category] = 0

            category_totals[category] += amount

    return category_totals
