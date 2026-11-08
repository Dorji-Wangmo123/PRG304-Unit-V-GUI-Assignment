
import sqlite3

DATABASE_NAME = "expenses.db"


def get_connection():
    """Create a connection to the SQLite database."""
    return sqlite3.connect(DATABASE_NAME)


def create_table():
    """Create the transactions and budgets tables."""
    connection = get_connection()
    cursor = connection.cursor()

    # Transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_type TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        )
    """)

    # Monthly budgets table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            month TEXT NOT NULL,
            amount REAL NOT NULL,
            UNIQUE(category, month)
        )
    """)

    connection.commit()
    connection.close()


def add_transaction(transaction_type, amount, category, date, description):
    """Save a new income or expense transaction."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO transactions
        (transaction_type, amount, category, date, description)
        VALUES (?, ?, ?, ?, ?)
    """, (transaction_type, amount, category, date, description))

    connection.commit()
    connection.close()


def get_all_transactions():
    """Retrieve all transactions."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
    records = cursor.fetchall()

    connection.close()
    return records


def update_transaction(transaction_id, transaction_type, amount,
                       category, date, description):
    """Update an existing transaction."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE transactions
        SET transaction_type = ?, amount = ?, category = ?,
            date = ?, description = ?
        WHERE id = ?
    """, (transaction_type, amount, category, date,
          description, transaction_id))

    connection.commit()
    connection.close()


def delete_transaction(transaction_id):
    """Delete a transaction."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM transactions WHERE id = ?",
        (transaction_id,)
    )

    connection.commit()
    connection.close()


# BUDGET FUNCTIONS

def add_budget(category, month, amount):
    """Add a monthly budget for a category."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO budgets (category, month, amount)
        VALUES (?, ?, ?)
    """, (category, month, amount))

    connection.commit()
    connection.close()


def get_all_budgets():
    """Retrieve all monthly budgets."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM budgets ORDER BY month DESC")
    records = cursor.fetchall()

    connection.close()
    return records


def update_budget(budget_id, category, month, amount):
    """Update an existing monthly budget."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE budgets
        SET category = ?, month = ?, amount = ?
        WHERE id = ?
    """, (category, month, amount, budget_id))

    connection.commit()
    connection.close()


def delete_budget(budget_id):
    """Delete a monthly budget."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM budgets WHERE id = ?",
        (budget_id,)
    )

    connection.commit()
    connection.close()
