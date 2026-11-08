# Unit V – Exploring GUI Frameworks

**Student Name:** Dorji Wangmo  
**Roll Number:** 6  
**Student ID:** 08230124  
**Course:** PRG304 – GUI Programming

## 1. Project Overview

This project was developed as part of the Unit V assignment, Exploring GUI Frameworks. It explores three Python GUI frameworks: PyQt6, Kivy and Tkinter.

The project also includes a Personal Expense Tracker desktop application developed using PyQt6. The application allows users to manage income and expenses, view financial summaries, analyse spending categories and manage budget limits.

## 2. Project Structure

- **Part A:** Contains basic Hello World applications developed using PyQt6, Kivy and Tkinter.
- **Part B:** Contains the Personal Expense Tracker application developed using PyQt6 and SQLite.

### Part B Files

- `main.py` – Main application window and interface.
- `database.py` – Database connection and database operations.
- `logic.py` – Application logic.
- `expense_dialog.py` – Dialog for adding and editing transactions.
- `expenses.db` – SQLite database containing application data.

## 3. Technologies Used

- Python 3.12
- PyQt6
- Kivy
- Tkinter
- SQLite3
- Visual Studio Code

## 4. Features of the Personal Expense Tracker

- Dashboard displaying total income, expenses and balance.
- Add income and expense transactions.
- Edit and delete transactions.
- Search transactions by description or category.
- Filter transactions by month.
- View monthly financial summaries.
- Analyse spending by category.
- Create and view category budgets.
- Input validation and error messages.
- Store transaction and budget information using SQLite.

## 5. Installation Requirements

Make sure Python 3.12 is installed.

Install the required packages using:

```bash
pip install PyQt6 Kivy
```

Tkinter is included with most standard Python installations.

## 6. How to Run the Applications

### Part A

Run each Python file from its respective folder:

```bash
python pyqt_hello.py
```

```bash
python kivy_hello.py
```

```bash
python tkinter_hello.py
```

### Part B – Personal Expense Tracker

Open the terminal in VS Code and navigate to the Part B folder:

```bash
cd partB
```

Run the application:

```bash
python main.py
```

## 7. Database

The application uses SQLite to store transaction and budget information locally in `expenses.db`.

The saved records remain available when the application is closed and reopened.

## 8. Testing

The application was tested for:

- Adding income and expense transactions.
- Editing and deleting transactions.
- Searching and filtering transactions.
- Displaying dashboard summaries.
- Viewing reports and analytics.
- Managing budgets.
- Rejecting invalid transaction amounts.
- Rejecting empty descriptions.
- Rejecting zero budget limits.
- Saving and retrieving data after restarting the application.

## 9. Student Information

**Name:** Dorji Wangmo  
**Roll Number:** 6  
**Student ID:** 08230124