import sys
import sqlite3

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QTableWidget,
    QTableWidgetItem, QLineEdit, QMessageBox, QHeaderView,
    QDateEdit, QDialog, QCheckBox, QStackedWidget, QProgressBar,
    QFrame, QComboBox, QDoubleSpinBox, QScrollArea
)
from PyQt6.QtCore import QDate, Qt

import database
import logic
from expense_dialog import ExpenseDialog


class ExpenseTracker(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Personal Expense Tracker")
        self.setGeometry(100, 100, 1150, 800)

        database.create_table()
        self.transactions = []
        self.budgets = []
        self.editing_budget_id = None

        self.create_interface()
        self.load_transactions()
        self.load_budgets()

    def create_interface(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # SIDEBAR
        sidebar_widget = QWidget()
        sidebar_widget.setFixedWidth(210)
        sidebar_widget.setStyleSheet("""
            QWidget {
                background-color: #263445;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                background-color: transparent;
                color: white;
                text-align: left;
                padding: 13px 18px;
                border: none;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3B4D63;
            }
            QPushButton:checked {
                background-color: #3B82F6;
                font-weight: bold;
            }
        """)

        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setContentsMargins(15, 25, 15, 20)
        sidebar_layout.setSpacing(12)

        app_title = QLabel("MY EXPENSES")
        app_title.setStyleSheet(
            "font-size: 21px; font-weight: bold; padding: 8px 5px;"
        )

        self.dashboard_button = QPushButton("Dashboard")
        self.transactions_button = QPushButton("Transactions")
        self.analytics_button = QPushButton("Reports & Analytics")
        self.budget_button = QPushButton("Budget Planner")
        self.about_button = QPushButton("About")

        self.nav_buttons = [
            self.dashboard_button,
            self.transactions_button,
            self.analytics_button,
            self.budget_button,
            self.about_button
        ]

        for button in self.nav_buttons:
            button.setCheckable(True)

        self.dashboard_button.setChecked(True)

        sidebar_layout.addWidget(app_title)
        sidebar_layout.addSpacing(25)
        for button in self.nav_buttons:
            sidebar_layout.addWidget(button)
        sidebar_layout.addStretch()

        main_layout.addWidget(sidebar_widget)

        # PAGE STACK
        self.pages = QStackedWidget()
        self.dashboard_page = self.create_dashboard_page()
        self.transactions_page = self.create_transactions_page()
        self.analytics_page = self.create_analytics_page()
        self.budget_page = self.create_budget_page()
        self.about_page = self.create_about_page()

        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.transactions_page)
        self.pages.addWidget(self.analytics_page)
        self.pages.addWidget(self.budget_page)
        self.pages.addWidget(self.about_page)
        main_layout.addWidget(self.pages)

        self.dashboard_button.clicked.connect(self.show_dashboard)
        self.transactions_button.clicked.connect(self.show_transactions)
        self.analytics_button.clicked.connect(self.show_analytics)
        self.budget_button.clicked.connect(self.show_budgets)
        self.about_button.clicked.connect(self.show_about)

        # GENERAL STYLING
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F4F6F9;
            }
            QLabel {
                color: #263445;
            }
            QPushButton {
                background-color: #3B82F6;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
            QLineEdit, QDateEdit, QComboBox, QDoubleSpinBox {
                padding: 9px;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                background-color: white;
            }
            QCheckBox {
                color: #263445;
                font-weight: bold;
                spacing: 6px;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #DDDDDD;
                gridline-color: #EEEEEE;
            }
            QHeaderView::section {
                background-color: #263445;
                color: white;
                padding: 8px;
                font-weight: bold;
            }
            QProgressBar {
                border: none;
                border-radius: 6px;
                background-color: #E8EDF3;
                text-align: center;
                height: 16px;
            }
            QProgressBar::chunk {
                background-color: #3B82F6;
                border-radius: 6px;
            }
        """)

    def create_heading(self, title, subtitle):
        layout = QVBoxLayout()
        heading = QLabel(title)
        heading.setStyleSheet(
            "font-size: 26px; font-weight: bold; color: #263445;"
        )
        description = QLabel(subtitle)
        description.setStyleSheet("font-size: 13px; color: #667085;")
        layout.addWidget(heading)
        layout.addWidget(description)
        return layout

    def create_summary_card(self, title, value_label, color):
        card_layout = QVBoxLayout()
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 12px; font-weight: bold;")
        value_label.setStyleSheet(
            "font-size: 22px; font-weight: bold; color: #263445;"
        )
        card_layout.addWidget(title_label)
        card_layout.addWidget(value_label)

        card = QWidget()
        card.setLayout(card_layout)
        card.setStyleSheet(
            f"background-color: {color}; padding: 15px; border-radius: 8px;"
        )
        return card

    def create_dashboard_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 25, 28, 25)
        layout.setSpacing(18)

        layout.addLayout(self.create_heading(
            "Dashboard",
            "An overview of your income, expenses and balance."
        ))

        cards_layout = QGridLayout()
        self.income_label = QLabel("Nu. 0.00")
        self.expense_label = QLabel("Nu. 0.00")
        self.balance_label = QLabel("Nu. 0.00")

        cards = [
            ("TOTAL INCOME", self.income_label, "#DFF3E4"),
            ("TOTAL EXPENSES", self.expense_label, "#FCE1E1"),
            ("BALANCE", self.balance_label, "#DFEAFE")
        ]

        for column, (title, value, color) in enumerate(cards):
            cards_layout.addWidget(
                self.create_summary_card(title, value, color), 0, column
            )
        layout.addLayout(cards_layout)

        monthly_heading = QLabel("Monthly Summary")
        monthly_heading.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: #263445;"
        )
        layout.addWidget(monthly_heading)

        month_layout = QHBoxLayout()
        month_layout.addWidget(QLabel("Select Month:"))

        self.month_selector = QDateEdit()
        self.month_selector.setCalendarPopup(True)
        self.month_selector.setDate(QDate.currentDate())
        self.month_selector.setDisplayFormat("MMMM yyyy")
        month_layout.addWidget(self.month_selector)
        month_layout.addStretch()
        layout.addLayout(month_layout)

        monthly_cards_layout = QGridLayout()
        self.month_income_label = QLabel("Nu. 0.00")
        self.month_expense_label = QLabel("Nu. 0.00")
        self.month_balance_label = QLabel("Nu. 0.00")

        monthly_cards = [
            ("MONTHLY INCOME", self.month_income_label, "#DFF3E4"),
            ("MONTHLY EXPENSES", self.month_expense_label, "#FCE1E1"),
            ("MONTHLY BALANCE", self.month_balance_label, "#DFEAFE")
        ]

        for column, (title, value, color) in enumerate(monthly_cards):
            monthly_cards_layout.addWidget(
                self.create_summary_card(title, value, color), 0, column
            )
        layout.addLayout(monthly_cards_layout)

        layout.addStretch()
        self.month_selector.dateChanged.connect(self.month_changed)
        return page

    def create_transactions_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 25, 28, 25)
        layout.setSpacing(15)

        layout.addLayout(self.create_heading(
            "Transactions",
            "Add, view, search, edit and delete your records."
        ))

        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search by description or category..."
        )

        self.month_filter = QCheckBox(
            "Show selected month's transactions only"
        )

        self.add_button = QPushButton("+ Add Transaction")
        self.edit_button = QPushButton("Edit Selected")
        self.delete_button = QPushButton("Delete Selected")
        self.category_button = QPushButton("Category Summary")

        search_layout.addWidget(self.search_input, 2)
        search_layout.addWidget(self.month_filter, 1)
        layout.addLayout(search_layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addWidget(self.category_button)
        layout.addLayout(buttons_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Type", "Amount", "Category", "Date", "Description"
        ])
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.table.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.table.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.table.setVerticalScrollMode(
            QTableWidget.ScrollMode.ScrollPerPixel
        )
        self.table.setMinimumHeight(250)
        layout.addWidget(self.table, 1)

        self.add_button.clicked.connect(self.add_transaction)
        self.edit_button.clicked.connect(self.edit_transaction)
        self.delete_button.clicked.connect(self.delete_transaction)
        self.category_button.clicked.connect(self.show_category_summary)
        self.search_input.textChanged.connect(self.search_transactions)
        self.month_filter.stateChanged.connect(self.search_transactions)

        return page

    # REPORTS AND ANALYTICS PAGE - SCROLLABLE VERSION
    def create_analytics_page(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 25, 28, 25)
        layout.setSpacing(16)

        layout.addLayout(self.create_heading(
            "Reports & Analytics",
            "Understand your spending patterns and monthly finances."
        ))

        month_row = QHBoxLayout()
        month_row.addWidget(QLabel("Report month:"))
        self.analytics_month_selector = QDateEdit()
        self.analytics_month_selector.setCalendarPopup(True)
        self.analytics_month_selector.setDate(QDate.currentDate())
        self.analytics_month_selector.setDisplayFormat("MMMM yyyy")
        month_row.addWidget(self.analytics_month_selector)
        month_row.addStretch()
        layout.addLayout(month_row)

        summary_row = QGridLayout()
        self.report_income_label = QLabel("Nu. 0.00")
        self.report_expense_label = QLabel("Nu. 0.00")
        self.report_balance_label = QLabel("Nu. 0.00")

        summary_row.addWidget(self.create_summary_card(
            "MONTHLY INCOME", self.report_income_label, "#DFF3E4"
        ), 0, 0)
        summary_row.addWidget(self.create_summary_card(
            "MONTHLY EXPENSES", self.report_expense_label, "#FCE1E1"
        ), 0, 1)
        summary_row.addWidget(self.create_summary_card(
            "MONTHLY BALANCE", self.report_balance_label, "#DFEAFE"
        ), 0, 2)
        layout.addLayout(summary_row)

        comparison_frame = QFrame()
        comparison_frame.setStyleSheet(
            "QFrame { background: white; border-radius: 9px; "
            "border: 1px solid #E1E6ED; }"
        )
        comparison_layout = QVBoxLayout(comparison_frame)
        comparison_layout.setContentsMargins(18, 15, 18, 15)

        comparison_title = QLabel("Income vs Expenses")
        comparison_title.setStyleSheet(
            "font-size: 18px; font-weight: bold; border: none;"
        )
        comparison_layout.addWidget(comparison_title)

        self.income_bar_title = QLabel("Income")
        self.income_bar = QProgressBar()
        self.income_bar.setRange(0, 100)
        self.income_bar.setTextVisible(False)
        self.income_bar.setStyleSheet(
            "QProgressBar { background: #E8EDF3; border: none; "
            "border-radius: 6px; height: 18px; }"
            "QProgressBar::chunk { background: #22A06B; border-radius: 6px; }"
        )

        self.expense_bar_title = QLabel("Expenses")
        self.expense_bar = QProgressBar()
        self.expense_bar.setRange(0, 100)
        self.expense_bar.setTextVisible(False)
        self.expense_bar.setStyleSheet(
            "QProgressBar { background: #E8EDF3; border: none; "
            "border-radius: 6px; height: 18px; }"
            "QProgressBar::chunk { background: #E76F51; border-radius: 6px; }"
        )

        comparison_layout.addWidget(self.income_bar_title)
        comparison_layout.addWidget(self.income_bar)
        comparison_layout.addWidget(self.expense_bar_title)
        comparison_layout.addWidget(self.expense_bar)
        layout.addWidget(comparison_frame)

        category_frame = QFrame()
        category_frame.setStyleSheet(
            "QFrame { background: white; border-radius: 9px; "
            "border: 1px solid #E1E6ED; }"
        )
        category_layout = QVBoxLayout(category_frame)
        category_layout.setContentsMargins(18, 15, 18, 15)

        category_heading = QLabel("Expense Breakdown by Category")
        category_heading.setStyleSheet(
            "font-size: 18px; font-weight: bold; border: none;"
        )
        category_layout.addWidget(category_heading)

        self.category_report_layout = QVBoxLayout()
        self.category_report_layout.setSpacing(10)
        category_layout.addLayout(self.category_report_layout)
        layout.addWidget(category_frame)
        layout.addStretch()

        self.analytics_month_selector.dateChanged.connect(
            self.update_analytics
        )

        scroll.setWidget(page)
        return scroll

    # BUDGET PLANNER PAGE
    def create_budget_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 25, 28, 25)
        layout.setSpacing(15)

        layout.addLayout(self.create_heading(
            "Budget Planner",
            "Set monthly spending limits and keep track of your expenses."
        ))

        month_row = QHBoxLayout()
        month_row.addWidget(QLabel("Budget month:"))
        self.budget_month_selector = QDateEdit()
        self.budget_month_selector.setCalendarPopup(True)
        self.budget_month_selector.setDate(QDate.currentDate())
        self.budget_month_selector.setDisplayFormat("MMMM yyyy")
        month_row.addWidget(self.budget_month_selector)
        month_row.addStretch()
        layout.addLayout(month_row)

        form_frame = QFrame()
        form_frame.setStyleSheet(
            "QFrame { background: white; border: 1px solid #E1E6ED; "
            "border-radius: 9px; }"
        )
        form_layout = QVBoxLayout(form_frame)
        form_layout.setContentsMargins(16, 14, 16, 14)

        form_title = QLabel("Set a Category Budget")
        form_title.setStyleSheet(
            "font-size: 17px; font-weight: bold; border: none;"
        )
        form_layout.addWidget(form_title)

        fields_layout = QHBoxLayout()

        category_column = QVBoxLayout()
        category_column.addWidget(QLabel("Category"))
        self.budget_category = QComboBox()
        self.budget_category.addItems([
            "Food", "Transport", "Shopping", "Education",
            "Entertainment", "Bills", "Health", "Other"
        ])
        category_column.addWidget(self.budget_category)

        amount_column = QVBoxLayout()
        amount_column.addWidget(QLabel("Monthly limit (Nu.)"))
        self.budget_amount = QDoubleSpinBox()
        self.budget_amount.setRange(0.01, 1000000000)
        self.budget_amount.setDecimals(2)
        self.budget_amount.setValue(1000.00)
        amount_column.addWidget(self.budget_amount)

        fields_layout.addLayout(category_column, 1)
        fields_layout.addLayout(amount_column, 1)

        self.save_budget_button = QPushButton("Save Budget")
        self.cancel_budget_edit_button = QPushButton("Cancel Edit")
        fields_layout.addWidget(self.save_budget_button)
        fields_layout.addWidget(self.cancel_budget_edit_button)
        form_layout.addLayout(fields_layout)
        layout.addWidget(form_frame)

        table_heading = QLabel("Your Monthly Budgets")
        table_heading.setStyleSheet(
            "font-size: 19px; font-weight: bold; color: #263445;"
        )
        layout.addWidget(table_heading)

        self.budget_table = QTableWidget()
        self.budget_table.setColumnCount(6)
        self.budget_table.setHorizontalHeaderLabels([
            "ID", "Category", "Budget Limit", "Spent",
            "Remaining", "Usage"
        ])
        self.budget_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.budget_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.budget_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        layout.addWidget(self.budget_table)

        action_row = QHBoxLayout()
        self.edit_budget_button = QPushButton("Edit Selected Budget")
        self.delete_budget_button = QPushButton("Delete Selected Budget")
        action_row.addWidget(self.edit_budget_button)
        action_row.addWidget(self.delete_budget_button)
        action_row.addStretch()
        layout.addLayout(action_row)

        self.save_budget_button.clicked.connect(self.save_budget)
        self.cancel_budget_edit_button.clicked.connect(
            self.cancel_budget_edit
        )
        self.edit_budget_button.clicked.connect(self.edit_budget)
        self.delete_budget_button.clicked.connect(self.delete_budget)
        self.budget_month_selector.dateChanged.connect(
            self.budget_month_changed
        )

        self.cancel_budget_edit_button.setEnabled(False)
        return page

    def create_about_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(18)

        layout.addLayout(self.create_heading(
            "About Personal Expense Tracker",
            "Project information and developer details."
        ))

        description = QLabel(
            "Personal Expense Tracker is a desktop application designed "
            "to help users record and manage their income and expenses. "
            "It stores records locally using an SQLite database and provides "
            "summaries to support better monthly financial planning."
        )
        description.setWordWrap(True)
        description.setStyleSheet(
            "font-size: 15px; line-height: 1.5; padding: 18px; "
            "background-color: white; border-radius: 8px;"
        )
        layout.addWidget(description)

        features_title = QLabel("Main Features")
        features_title.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: #263445;"
        )
        layout.addWidget(features_title)

        features = QLabel(
            "• Record income and expenses\n"
            "• Edit and delete transactions\n"
            "• Search transactions and filter by month\n"
            "• View dashboard summaries and reports\n"
            "• Set monthly budgets by expense category\n"
            "• Track budget usage and remaining amounts\n"
            "• Save information locally with SQLite"
        )
        features.setStyleSheet(
            "font-size: 14px; padding: 18px; background-color: white; "
            "border-radius: 8px;"
        )
        layout.addWidget(features)

        developer_title = QLabel("Developer Information")
        developer_title.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: #263445;"
        )
        layout.addWidget(developer_title)

        developer = QLabel(
            "Name: Dorji Wangmo\n"
            "Roll Number: 6\n"
            "Student ID: 08230124"
        )
        developer.setStyleSheet(
            "font-size: 15px; padding: 18px; background-color: white; "
            "border-radius: 8px;"
        )
        layout.addWidget(developer)
        layout.addStretch()
        return page

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            child_layout = item.layout()
            if widget is not None:
                widget.deleteLater()
            elif child_layout is not None:
                self.clear_layout(child_layout)

    def update_analytics(self):
        selected_month = self.analytics_month_selector.date().toString(
            "yyyy-MM"
        )

        month_transactions = [
            record for record in self.transactions
            if str(record[4]).startswith(selected_month)
        ]

        income = sum(
            float(record[2]) for record in month_transactions
            if record[1] == "Income"
        )
        expenses = sum(
            float(record[2]) for record in month_transactions
            if record[1] == "Expense"
        )
        balance = income - expenses

        self.report_income_label.setText(f"Nu. {income:.2f}")
        self.report_expense_label.setText(f"Nu. {expenses:.2f}")
        self.report_balance_label.setText(f"Nu. {balance:.2f}")

        largest_value = max(income, expenses, 1)
        self.income_bar.setValue(round(income / largest_value * 100))
        self.expense_bar.setValue(round(expenses / largest_value * 100))
        self.income_bar_title.setText(f"Income — Nu. {income:.2f}")
        self.expense_bar_title.setText(f"Expenses — Nu. {expenses:.2f}")

        category_totals = {}
        for record in month_transactions:
            if record[1] == "Expense":
                category = str(record[3])
                category_totals[category] = (
                    category_totals.get(category, 0) + float(record[2])
                )

        self.clear_layout(self.category_report_layout)

        if not category_totals:
            empty_label = QLabel(
                "No expense records found for this month."
            )
            empty_label.setStyleSheet(
                "color: #667085; border: none; padding: 8px;"
            )
            self.category_report_layout.addWidget(empty_label)
            return

        max_category_value = max(category_totals.values()) or 1

        for category, amount in sorted(
            category_totals.items(), key=lambda item: item[1], reverse=True
        ):
            row = QHBoxLayout()
            name_label = QLabel(category)
            name_label.setMinimumWidth(115)
            name_label.setStyleSheet("border: none; font-weight: bold;")

            bar = QProgressBar()
            bar.setRange(0, 100)
            bar.setValue(round(amount / max_category_value * 100))
            bar.setTextVisible(False)

            amount_label = QLabel(f"Nu. {amount:.2f}")
            amount_label.setMinimumWidth(115)
            amount_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            amount_label.setStyleSheet("border: none;")

            row.addWidget(name_label)
            row.addWidget(bar, 1)
            row.addWidget(amount_label)
            self.category_report_layout.addLayout(row)

    # BUDGET PLANNER FUNCTIONS
    def load_budgets(self):
        self.budgets = database.get_all_budgets()
        self.update_budget_table()

    def budget_month_changed(self):
        self.cancel_budget_edit()
        self.update_budget_table()

    def update_budget_table(self):
        if not hasattr(self, "budget_table"):
            return

        selected_month = self.budget_month_selector.date().toString(
            "yyyy-MM"
        )
        month_budgets = [
            budget for budget in self.budgets
            if budget[2] == selected_month
        ]

        self.budget_table.setRowCount(0)

        for row_number, budget in enumerate(month_budgets):
            budget_id, category, month, limit_amount = budget
            spent = sum(
                float(record[2]) for record in self.transactions
                if record[1] == "Expense"
                and record[3] == category
                and str(record[4]).startswith(month)
            )
            remaining = float(limit_amount) - spent

            self.budget_table.insertRow(row_number)
            values = [
                str(budget_id),
                category,
                f"Nu. {float(limit_amount):.2f}",
                f"Nu. {spent:.2f}",
                f"Nu. {remaining:.2f}"
            ]

            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                if column in (0, 2, 3, 4):
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignCenter
                    )
                self.budget_table.setItem(row_number, column, item)

            progress = QProgressBar()
            progress.setRange(0, 100)
            if float(limit_amount) > 0:
                percentage = round(spent / float(limit_amount) * 100)
            else:
                percentage = 0
            progress.setValue(min(percentage, 100))
            progress.setFormat(f"{percentage}%")
            if percentage > 100:
                progress.setStyleSheet(
                    "QProgressBar::chunk { background-color: #DC5656; }"
                )
            self.budget_table.setCellWidget(row_number, 5, progress)

    def save_budget(self):
        category = self.budget_category.currentText()
        month = self.budget_month_selector.date().toString("yyyy-MM")
        amount = self.budget_amount.value()

        try:
            if self.editing_budget_id is not None:
                database.update_budget(
                    self.editing_budget_id, category, month, amount
                )
                message = "Budget updated successfully!"
            else:
                existing_budget = next(
                    (
                        budget for budget in self.budgets
                        if budget[1] == category and budget[2] == month
                    ),
                    None
                )
                if existing_budget is not None:
                    QMessageBox.warning(
                        self,
                        "Budget Already Exists",
                        "A budget for this category and month already "
                        "exists. Select it and use Edit Selected Budget."
                    )
                    return

                database.add_budget(category, month, amount)
                message = "Budget added successfully!"

        except sqlite3.IntegrityError:
            QMessageBox.warning(
                self,
                "Duplicate Budget",
                "A budget for this category and month already exists."
            )
            return

        self.cancel_budget_edit()
        self.load_budgets()
        QMessageBox.information(self, "Success", message)

    def edit_budget(self):
        selected_row = self.budget_table.currentRow()

        if selected_row < 0:
            QMessageBox.warning(
                self, "No Selection",
                "Please select a budget to edit."
            )
            return

        budget_id = int(self.budget_table.item(selected_row, 0).text())
        budget = next(
            (item for item in self.budgets if item[0] == budget_id),
            None
        )

        if budget is None:
            return

        self.editing_budget_id = budget_id
        category_index = self.budget_category.findText(budget[1])
        if category_index >= 0:
            self.budget_category.setCurrentIndex(category_index)

        self.budget_amount.setValue(float(budget[3]))
        self.save_budget_button.setText("Update Budget")
        self.cancel_budget_edit_button.setEnabled(True)

    def cancel_budget_edit(self):
        self.editing_budget_id = None
        if hasattr(self, "budget_category"):
            self.budget_category.setCurrentIndex(0)
            self.budget_amount.setValue(1000.00)
            self.save_budget_button.setText("Save Budget")
            self.cancel_budget_edit_button.setEnabled(False)

    def delete_budget(self):
        selected_row = self.budget_table.currentRow()

        if selected_row < 0:
            QMessageBox.warning(
                self, "No Selection",
                "Please select a budget to delete."
            )
            return

        budget_id = int(self.budget_table.item(selected_row, 0).text())
        confirmation = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this budget?"
        )

        if confirmation == QMessageBox.StandardButton.Yes:
            database.delete_budget(budget_id)
            self.cancel_budget_edit()
            self.load_budgets()
            QMessageBox.information(
                self, "Deleted", "Budget deleted successfully!"
            )

    # SIDEBAR NAVIGATION
    def set_active_navigation(self, active_button, active_page):
        self.pages.setCurrentWidget(active_page)
        for button in self.nav_buttons:
            button.setChecked(button is active_button)

    def show_dashboard(self):
        self.set_active_navigation(self.dashboard_button, self.dashboard_page)
        self.update_summary()
        self.update_monthly_summary()

    def show_transactions(self):
        self.set_active_navigation(
            self.transactions_button, self.transactions_page
        )
        self.search_input.clear()
        self.month_filter.setChecked(False)
        self.search_transactions()

    def show_analytics(self):
        self.set_active_navigation(
            self.analytics_button, self.analytics_page
        )
        self.update_analytics()

    def show_budgets(self):
        self.set_active_navigation(self.budget_button, self.budget_page)
        self.cancel_budget_edit()
        self.load_budgets()

    def show_about(self):
        self.set_active_navigation(self.about_button, self.about_page)

    # LOAD AND DISPLAY DATA
    def load_transactions(self):
        self.transactions = database.get_all_transactions()
        self.update_summary()
        self.update_monthly_summary()
        self.search_transactions()
        self.update_analytics()
        if hasattr(self, "budget_table"):
            self.update_budget_table()

    def display_transactions(self, transactions):
        self.table.setRowCount(0)

        for row_number, transaction in enumerate(transactions):
            self.table.insertRow(row_number)

            for column, value in enumerate(transaction):
                item = QTableWidgetItem(str(value))
                if column == 2:
                    item.setText(f"Nu. {float(value):.2f}")
                self.table.setItem(row_number, column, item)

    # SUMMARY CALCULATIONS
    def update_summary(self):
        income, expenses, balance = logic.calculate_totals(
            self.transactions
        )
        self.income_label.setText(f"Nu. {income:.2f}")
        self.expense_label.setText(f"Nu. {expenses:.2f}")
        self.balance_label.setText(f"Nu. {balance:.2f}")

    def update_monthly_summary(self):
        selected_month = self.month_selector.date().toString("yyyy-MM")
        income, expenses, balance = logic.calculate_monthly_summary(
            self.transactions, selected_month
        )
        self.month_income_label.setText(f"Nu. {income:.2f}")
        self.month_expense_label.setText(f"Nu. {expenses:.2f}")
        self.month_balance_label.setText(f"Nu. {balance:.2f}")

    def month_changed(self):
        self.update_monthly_summary()
        self.search_transactions()

    # CATEGORY SUMMARY DIALOG
    def show_category_summary(self):
        category_totals = logic.calculate_category_summary(
            self.transactions
        )

        dialog = QDialog(self)
        dialog.setWindowTitle("Category-wise Expense Summary")
        dialog.setMinimumSize(550, 400)
        dialog.resize(650, 500)

        layout = QVBoxLayout(dialog)
        heading = QLabel("Your Spending by Category")
        heading.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: #263445;"
        )
        layout.addWidget(heading)

        if not category_totals:
            layout.addWidget(QLabel("No expense records available yet."))
        else:
            table = QTableWidget()
            table.setColumnCount(2)
            table.setHorizontalHeaderLabels(["Category", "Total Spent"])
            table.horizontalHeader().setSectionResizeMode(
                QHeaderView.ResizeMode.Stretch
            )

            sorted_categories = sorted(
                category_totals.items(),
                key=lambda item: item[1],
                reverse=True
            )
            table.setRowCount(len(sorted_categories))

            for row, (category, amount) in enumerate(sorted_categories):
                table.setItem(row, 0, QTableWidgetItem(category))
                table.setItem(
                    row, 1, QTableWidgetItem(f"Nu. {amount:.2f}")
                )

            table.setEditTriggers(
                QTableWidget.EditTrigger.NoEditTriggers
            )
            table.setVerticalScrollBarPolicy(
                Qt.ScrollBarPolicy.ScrollBarAsNeeded
            )
            table.setHorizontalScrollBarPolicy(
                Qt.ScrollBarPolicy.ScrollBarAsNeeded
            )
            table.setVerticalScrollMode(
                QTableWidget.ScrollMode.ScrollPerPixel
            )
            table.setMinimumHeight(220)
            layout.addWidget(table, 1)

        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)
        dialog.exec()

    # ADD TRANSACTION
    def add_transaction(self):
        dialog = ExpenseDialog(parent=self)

        if dialog.exec():
            data = dialog.get_data()
            database.add_transaction(*data)
            self.load_transactions()
            QMessageBox.information(
                self, "Success", "Transaction added successfully!"
            )

    # EDIT TRANSACTION
    def edit_transaction(self):
        selected_row = self.table.currentRow()

        if selected_row < 0:
            QMessageBox.warning(
                self, "No Selection",
                "Please select a transaction to edit."
            )
            return

        transaction_id = int(self.table.item(selected_row, 0).text())
        transaction = next(
            (record for record in self.transactions
             if record[0] == transaction_id),
            None
        )

        if transaction is None:
            return

        dialog = ExpenseDialog(transaction, self)
        if dialog.exec():
            data = dialog.get_data()
            database.update_transaction(transaction_id, *data)
            self.load_transactions()
            QMessageBox.information(
                self, "Success", "Transaction updated successfully!"
            )

    # DELETE TRANSACTION
    def delete_transaction(self):
        selected_row = self.table.currentRow()

        if selected_row < 0:
            QMessageBox.warning(
                self, "No Selection",
                "Please select a transaction to delete."
            )
            return

        transaction_id = int(self.table.item(selected_row, 0).text())
        confirmation = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this transaction?"
        )

        if confirmation == QMessageBox.StandardButton.Yes:
            database.delete_transaction(transaction_id)
            self.load_transactions()
            QMessageBox.information(
                self, "Deleted", "Transaction deleted successfully!"
            )

    # SEARCH AND MONTH FILTER
    def search_transactions(self):
        results = self.transactions

        if self.month_filter.isChecked():
            selected_month = self.month_selector.date().toString("yyyy-MM")
            results = logic.filter_by_month(results, selected_month)

        keyword = self.search_input.text().strip()
        if keyword:
            results = logic.search_transactions(results, keyword)

        self.display_transactions(results)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpenseTracker()
    window.show()
    sys.exit(app.exec())
