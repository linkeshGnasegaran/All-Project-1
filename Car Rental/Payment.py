import sys
import sqlite3
from tkinter import Tk, Label, Button, messagebox
import subprocess
from datetime import datetime

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
def show_payment_details(car_number, total_amount, customer_phone, start_date, end_date):
    # Get the car details from the database
    car_details = get_car_details(car_number)

    if not car_details:
        messagebox.showerror("Error", "Car details not found.")
        return

    window = Tk()
    window.title("Payment Window")
    window.geometry("500x700")

    # Title
    title_label = Label(window, text="Booking Details", font=("Helvetica", 20, "bold"))
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

    # Display customer phone number
    phone_label = Label(window, text=f"Customer Phone: {customer_phone}", font=("Helvetica", 12))
    phone_label.pack(pady=10)

    # Display booking dates as Start Date and End Date
    start_date_label = Label(window, text=f"Start Date: {start_date}", font=("Helvetica", 12))
    start_date_label.pack(pady=5)

    end_date_label = Label(window, text=f"End Date: {end_date}", font=("Helvetica", 12))
    end_date_label.pack(pady=5)

    def proceed_to_payment():
        try:
            subprocess.run(
                [
                    "python",
                    "Pay_Now.py",  # Adjust this to your payment processing script
                    str(car_number),  # Car registration number
                    str(total_amount),  # Total amount
                    str(customer_phone),  # Customer phone number
                    str(start_date),  # Start date
                    str(end_date)  # End date
                ],
                check=True,
            )

            # Close the current window after proceeding to payment
            window.destroy()

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Payment Error", f"Error during payment process: {e}")
            window.destroy()

    # Button to proceed with payment
    Button(window, text="Proceed with Payment", command=proceed_to_payment, bg="#1ABC9C", fg="#ffffff", font=("Helvetica", 12, "bold")).pack(pady=20)

    window.mainloop()

# Main function to handle arguments passed from the booking window
if __name__ == "__main__":
    # Debugging: Print the received arguments
    print(f"Arguments received in Payment.py: {sys.argv}")

    if len(sys.argv) < 6:
        print("Error: Missing arguments. Please ensure that car number, total amount, customer phone, start date, and end date are passed.")
        sys.exit(1)

    selected_car_number = sys.argv[1]
    total_amount = sys.argv[2]
    contact_no = sys.argv[3]
    start_date = sys.argv[5]
    end_date = sys.argv[6]

    print(f"Selected Car: {selected_car_number}, Total Amount: RM {total_amount}, Contact: {contact_no}, Dates: {start_date} to {end_date}")

    show_payment_details(selected_car_number, total_amount, contact_no, start_date, end_date)
