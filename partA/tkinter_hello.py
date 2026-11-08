
import tkinter as tk
from tkinter import messagebox

# Create main window
root = tk.Tk()
root.title("Tkinter")
root.geometry("400x250")

# Create heading
label = tk.Label(
    root,
    text="Hello Dorji!",
    font=("Arial", 20)
)
label.pack(pady=40)

# Button click function
def button_clicked():
    messagebox.showinfo(
        "Message",
        "Hello! Welcome to Tkinter."
    )

# Create button
button = tk.Button(
    root,
    text="Click Me",
    font=("Arial", 12),
    command=button_clicked
)
button.pack(fill="x", padx=20)

# Run application
root.mainloop()
