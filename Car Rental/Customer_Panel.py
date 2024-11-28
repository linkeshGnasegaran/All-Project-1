import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import subprocess
import os
import sys

def load_profile_image(img_path):
    """Load profile image from the given path, or use a fallback image if not found."""
    try:
        if img_path and os.path.exists(img_path):  # Check if img_path is not None and file exists
            profile_img = Image.open(img_path).resize((100, 100))  # Resize image
        else:
            raise FileNotFoundError  # Trigger fallback if img_path is None or file does not exist
    except (FileNotFoundError, TypeError):  # Catch both file not found and NoneType errors
        # Use a relative path for the fallback image
        fallback_img_path = os.path.join(os.path.dirname(__file__), "C:/Users/Honor/PycharmProjects/ALL 1 Project/Car Rental/i4.png")
        profile_img = Image.open(fallback_img_path).resize((100, 100))
    return ImageTk.PhotoImage(profile_img)


def fetch_customer_details(email):
    """Fetch customer details, including profile picture path, from the database."""
    try:
        conn = sqlite3.connect("car_rental.db")  # Connect to your database
        cursor = conn.cursor()

        # Query to get customer details and profile picture path
        cursor.execute("""SELECT first_name, last_name, email, contact_no, profile_picture 
                          FROM Register WHERE email = ?""", (email,))
        customer_data = cursor.fetchone()

        conn.close()

        if customer_data:
            return customer_data
        else:
            messagebox.showerror("Error", "Customer not found.")
            return None
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
        return None


def customer_profile(email):
    """Display the customer profile window."""
    customer_data = fetch_customer_details(email)

    if not customer_data:
        return

    # Unpack customer details
    first_name, last_name, email, contact_no, profile_pic_path = customer_data
    full_name = f"{first_name} {last_name}"

    # Create the main window
    window = tk.Tk()
    window.title("Customer Profile")
    window.geometry("800x600")

    # Load and display the profile picture
    profile_img = load_profile_image(profile_pic_path)
    profile_pic_label = tk.Label(window, image=profile_img)
    profile_pic_label.image = profile_img
    profile_pic_label.grid(row=0, column=0, padx=20, pady=20)

    # Title
    title_label = tk.Label(window, text="Customer Profile", font=("Arial", 16, "bold"))
    title_label.grid(row=0, column=1, padx=20, pady=20)

    # Customer info section
    info_frame = tk.Frame(window)
    info_frame.grid(row=1, column=1, padx=20, pady=10)

    tk.Label(info_frame, text="Name: " + full_name, font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
    tk.Label(info_frame, text="Email: " + email, font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
    tk.Label(info_frame, text="Phone: " + contact_no, font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)

    # Buttons
    buttons_frame = tk.Frame(window)
    buttons_frame.grid(row=2, column=1, padx=20, pady=20)

    def print_details():
        """Navigate to print_details."""
        print(f"Passing email: {email}, contact_no: {contact_no}")  # Debugging
        subprocess.Popen(
            ["python", "Print_Your_Details.py", email, contact_no]  # Pass contact_no correctly
        )

    def chatbot():
        """Navigate to chatbot."""
        print(f"Passing email: {email}, contact_no: {contact_no}")  # Debugging
        subprocess.Popen(
            ["python", "Chatbot.py", email, contact_no]  # Pass contact_no correctly
        )

    def booking_panel():
        """Navigate to booking panel."""
        print(f"Passing email: {email}, contact_no: {contact_no}")  # Debugging
        subprocess.Popen(
            ["python", "Booking_Panel.py", email, contact_no]  # Pass contact_no correctly
        )

    def booking_history():
        """View booking history."""
        print(f"Passing email: {email}, contact_no: {contact_no}")  # Debugging
        window.destroy()
        subprocess.Popen(
            ["python", "Booking_Details.py", email, contact_no]  # Pass contact_no correctly
        )

    def change_details():
        """Navigate to change details."""
        window.destroy()
        subprocess.Popen(["python", "Change_Details.py", email, contact_no])  # Pass email and contact_no correctly

    tk.Button(buttons_frame, text="Book Car", command=booking_panel, font=("Arial", 12), bg="blue", fg="white", width=15).grid(row=0, column=0, pady=10)
    tk.Button(buttons_frame, text="Booking History", command=booking_history, font=("Arial", 12), bg="green", fg="white", width=15).grid(row=1, column=0, pady=10)
    tk.Button(buttons_frame, text="Change Details", command=change_details, font=("Arial", 12), bg="orange", fg="white", width=15).grid(row=2, column=0, pady=10)
    tk.Button(buttons_frame, text="Your Chatbot", command=chatbot, font=("Arial", 12), bg="purple", fg="white", width=15).grid(row=5, column=0, pady=10)
    tk.Button(buttons_frame, text="Print Your Details", command=print_details, font=("Arial", 12), bg="purple", fg="white", width=15).grid(row=6, column=0, pady=10)

    window.mainloop()


if __name__ == "__main__":
    # Get the email passed as a command-line argument
    if len(sys.argv) < 2:
        messagebox.showerror("Error", "Email not provided as argument.")
    else:
        email = sys.argv[1]
        customer_profile(email)
