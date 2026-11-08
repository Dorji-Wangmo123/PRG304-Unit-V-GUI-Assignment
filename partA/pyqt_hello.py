
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QMessageBox
)

# Create application
app = QApplication(sys.argv)

# Create main window
window = QWidget()
window.setWindowTitle("PyQt6")
window.resize(400, 250)

# Create heading
label = QLabel("Hello Dorji!")
label.setStyleSheet("font-size: 22px; font-weight: bold;")

# Create button
button = QPushButton("Click Me")

# Button click function
def button_clicked():
    QMessageBox.information(
        window,
        "Message",
        "Hello! Welcome to PyQt6."
    )

# Connect button to function
button.clicked.connect(button_clicked)

# Create layout
layout = QVBoxLayout()
layout.addWidget(label)
layout.addWidget(button)

window.setLayout(layout)

# Display window
window.show()

sys.exit(app.exec())
