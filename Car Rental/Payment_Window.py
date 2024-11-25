import tkinter as tk
from tkinter import messagebox
import sys

# Function to simulate payment process
def process_payment(car_number, total_amount):
    # For simplicity, this just shows a message box
    messagebox.showinfo("Payment Successful", f"Payment of RM {total_amount} for Car {car_number} has been processed.")

# Payment Window
def create_payment_window(car_number, total_amount):
    window = tk.Tk()
    window.geometry("400x300")
    window.title("Payment Window")

    label = tk.Label(window, text=f"Payment for Car {car_number}", font=("Helvetica", 14))
    label.pack(pady=20)

    amount_label = tk.Label(window, text=f"Total Amount: RM {total_amount:.2f}", font=("Helvetica", 12))
    amount_label.pack(pady=10)

    pay_button = tk.Button(window, text="Pay Now", command=lambda: process_payment(car_number, total_amount))
    pay_button.pack(pady=20)import sys
import sqlite3
from tkinter import Tk, Label, Button


# Function to connect to the database and fetch car details by registration number
def get_car_details(car_number):
    try:
        conn = sqlite3.connect('car_details.db')  # Adjust your database name and path if necessary
        cursor = conn.cursor()
        cursor.execute('''SELECT registration_number, make_and_model, seating_capacity, daily_rate, fuel_type, 
                                 manufacturer_year, transmission_type, car_type, mileage, color 
                          FROM cars WHERE registration_number = ?''', (car_number,))
        car_details = cursor.fetchone()
        conn.close()
        return car_details
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None


# Function to display payment details
def show_payment_details(car_number, total_amount):
    # Get the car details from the database
    car_details = get_car_details(car_number)

    if not car_details:
        print("Error: Car details not found.")
        return

    window = Tk()
    window.title("Payment Window")
    window.geometry("600x400")

    # Title
    title_label = Label(window, text="Payment Details", font=("Helvetica", 20, "bold"))
    title_label.pack(pady=20)

    # Display car information
    car_info_labels = [
        f"Registration Number: {car_details[0]}",
        f"Make & Model: {car_details[1]}",
        f"Seating Capacity: {car_details[2]}",
        f"Daily Rate (RM): {car_details[3]}",
        f"Fuel Type: {car_details[4]}",
        f"Manufacturer Year: {car_details[5]}",
        f"Transmission Type: {car_details[6]}",
        f"Car Type: {car_details[7]}",
        f"Mileage (km): {car_details[8]}",
        f"Color: {car_details[9]}",
    ]

    # Display each car info label in the window
    for info in car_info_labels:
        car_info_label = Label(window, text=info, font=("Helvetica", 12))
        car_info_label.pack(pady=5)

    # Display total amount
    amount_label = Label(window, text=f"Total Amount: RM {total_amount}", font=("Helvetica", 12))
    amount_label.pack(pady=10)

    # Button to proceed with payment (Placeholder)
    Button(window, text="Proceed with Payment", bg="#1ABC9C", fg="#ffffff", font=("Helvetica", 12, "bold")).pack(
        pady=20)

    window.mainloop()


# Main function to handle arguments passed from the booking window
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Error: Missing arguments")
        sys.exit(1)

    car_number = sys.argv[1]  # Registration number passed from the booking window
    total_amount = sys.argv[2]  # Total amount passed from the booking window

    show_payment_details(car_number, total_amount)


    cancel_button = tk.Button(window, text="Cancel", command=window.quit)
    cancel_button.pack(pady=10)

    window.mainloop()

# Get car number and amount from arguments passed in the command line
if __name__ == "__main__":
    try:
        car_number = sys.argv[1]
        total_amount = float(sys.argv[2])
        create_payment_window(car_number, total_amount)
    except IndexError:
        print("Error: Missing arguments. Expected car number and total amount.")
