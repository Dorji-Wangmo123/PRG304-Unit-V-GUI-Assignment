from PyQt6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QComboBox,
    QDoubleSpinBox, QDateEdit, QPushButton,
    QFormLayout, QHBoxLayout, QVBoxLayout,
    QMessageBox
)
from PyQt6.QtCore import QDate


class ExpenseDialog(QDialog):

    def __init__(self, transaction=None, parent=None):
        super().__init__(parent)

        self.transaction = transaction
        self.setWindowTitle(
            "Edit Transaction" if transaction else "Add Transaction"
        )
        self.setFixedSize(400, 450)

        # Transaction type
        self.type_input = QComboBox()
        self.type_input.addItems(["Expense", "Income"])

        # Amount: zero is allowed temporarily so validation can show a warning
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setRange(0, 100000000)
        self.amount_input.setDecimals(2)
        self.amount_input.setPrefix("Nu. ")

        # Category
        self.category_input = QComboBox()
        self.category_input.addItem("Select category")
        self.category_input.addItems([
            "Food", "Transport", "Shopping", "Education",
            "Entertainment", "Bills", "Health", "Salary", "Other"
        ])

        # Date
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setDisplayFormat("yyyy-MM-dd")

        # Description
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText(
            "Enter a short description"
        )

        # Form layout
        form_layout = QFormLayout()
        form_layout.addRow("Transaction Type:", self.type_input)
        form_layout.addRow("Amount:", self.amount_input)
        form_layout.addRow("Category:", self.category_input)
        form_layout.addRow("Date:", self.date_input)
        form_layout.addRow("Description:", self.description_input)

        # Buttons
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel("Transaction Details"))
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        # Load existing details when editing
        if transaction:
            self.type_input.setCurrentText(transaction[1])
            self.amount_input.setValue(float(transaction[2]))
            self.category_input.setCurrentText(transaction[3])
            self.date_input.setDate(
                QDate.fromString(str(transaction[4]), "yyyy-MM-dd")
            )
            self.description_input.setText(transaction[5] or "")

        # Button events
        self.save_button.clicked.connect(self.validate_and_save)
        self.cancel_button.clicked.connect(self.reject)

    def validate_and_save(self):
        amount = self.amount_input.value()
        category = self.category_input.currentText()
        description = self.description_input.text().strip()

        if amount <= 0:
            QMessageBox.warning(
                self, "Invalid Amount",
                "Please enter an amount greater than zero."
            )
            return

        if self.category_input.currentIndex() == 0:
            QMessageBox.warning(
                self, "Missing Category",
                "Please select a transaction category."
            )
            return

        if not description:
            QMessageBox.warning(
                self, "Missing Description",
                "Please enter a transaction description."
            )
            return

        self.accept()

    def get_data(self):
        return (
            self.type_input.currentText(),
            self.amount_input.value(),
            self.category_input.currentText(),
            self.date_input.date().toString("yyyy-MM-dd"),
            self.description_input.text().strip()
        )
