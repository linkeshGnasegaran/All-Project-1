import tkinter as tk
from tkinter import messagebox

def show_success_message():
    # Create a root window (hidden)
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Show success message box
    messagebox.showinfo("Registration Successful", "You have registered successfully! You can now login.")

    # Close the root window after showing the message
    root.quit()

# Call the function to show the message box
show_success_message()
