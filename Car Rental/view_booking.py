import tkinter as tk
from db_manager import get_booking_history

def launch_booking_history():
    """Launch the booking history window."""
    history_window = tk.Toplevel()
    history_window.title("Booking History")
    history_window.geometry("800x600")

    customer_name = "John Doe"  # Replace with the logged-in user's name
    bookings = get_booking_history(customer_name)

    if not bookings:
        tk.Label(history_window, text="No bookings found.", font=("Arial", 16)).pack()
        return

    for idx, booking in enumerate(bookings, start=1):
        tk.Label(history_window, text=f"Booking {idx}:", font=("Arial", 14)).pack(anchor=tk.W, padx=20, pady=5)
        tk.Label(history_window, text=f"Car ID: {booking[1]}", font=("Arial", 12)).pack(anchor=tk.W, padx=40)
        tk.Label(history_window, text=f"Booking Date: {booking[2]}", font=("Arial", 12)).pack(anchor=tk.W, padx=40)
        tk.Label(history_window, text="---").pack()

    history_window.mainloop()
