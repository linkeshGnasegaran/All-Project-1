import tkinter as tk
from tkinter import messagebox
import subprocess

def open_booking_panel():
    subprocess.Popen(["python", "booking_panel.py"])  # Opens the booking panel script

def open_view_booking():
    subprocess.Popen(["python", "view_booking.py"])  # Opens the booking history script

def quit_app():
    if messagebox.askyesno("Quit", "Are you sure you want to exit?"):
        root.destroy()

# Create the main window
root = tk.Tk()
root.title("Car Rental System")
root.geometry("400x300")

# Title Label
title_label = tk.Label(root, text="Car Rental System", font=("Arial", 18, "bold"))
title_label.pack(pady=20)

# Buttons for navigation
btn_booking_panel = tk.Button(root, text="Book a Car", command=open_booking_panel, font=("Arial", 12), bg="blue", fg="white", width=20)
btn_booking_panel.pack(pady=10)

btn_view_booking = tk.Button(root, text="View Booking History", command=open_view_booking, font=("Arial", 12), bg="green", fg="white", width=20)
btn_view_booking.pack(pady=10)

btn_exit = tk.Button(root, text="Exit", command=quit_app, font=("Arial", 12), bg="red", fg="white", width=20)
btn_exit.pack(pady=10)

# Run the main loop
root.mainloop()
