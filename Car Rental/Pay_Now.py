import random
import string
import sqlite3
from tkinter import Tk, Button, Label, Entry, messagebox, Frame
import sys
from datetime import datetime

# Function to connect to the database and fetch car details
def connect_db():
    try:
        conn = sqlite3.connect('car_details.db')  # Adjust your database name and path if necessary
        cursor = conn.cursor()
        return conn, cursor
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None, None

# Function to fetch car details from the database
def fetch_car_details():
    conn, cursor = connect_db()
    if conn is None or cursor is None:
        return []
    try:
        cursor.execute('''SELECT registration_number, make_and_model, seating_capacity, daily_rate, fuel_type, 
                                 manufacturer_year, transmission_type, car_type, mileage, color, image_path 
                          FROM cars''')
        cars = cursor.fetchall()
        conn.close()
        return cars
    except Exception as e:
        print(f"Error fetching car details: {e}")
        return []

# Function to connect to the database for invoice operations
def connect_db_for_invoice():
    try:
        conn = sqlite3.connect('car_booking.db', timeout=10)
        cursor = conn.cursor()
        return conn, cursor
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error connecting to the database: {e}")
        return None, None

# Function to create the invoices table if it doesn't exist
def create_invoices_table():
    conn, cursor = connect_db_for_invoice()
    if conn is None or cursor is None:
        return

    try:
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS invoices (
                ID TEXT PRIMARY KEY,
                RegNo TEXT,
                CustomerName TEXT,
                ContactNo TEXT,
                StartDate TEXT,
                EndDate TEXT,
                TotalPrice REAL,
                NoOfDays INTEGER,
                Status TEXT
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error creating invoices table: {e}")
    finally:
        conn.close()

# Function to generate a unique receipt ID
def generate_receipt_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

# Function to calculate the number of days between start and end date
def calculate_no_of_days(start_date, end_date):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    delta = end_date - start_date
    return delta.days

# Function to create invoice dynamically using the passed values
def create_invoice(car_id, reg_no, customer_name, contact_no, start_date, end_date, total_price, no_of_days):
    conn, cursor = connect_db_for_invoice()
    if conn is None or cursor is None:
        return None

    invoice_id = generate_receipt_id()

    try:
        cursor.execute(''' 
            INSERT INTO invoices (ID, RegNo, CustomerName, ContactNo, StartDate, EndDate, TotalPrice, NoOfDays, Status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (invoice_id, reg_no, customer_name, contact_no, start_date, end_date, total_price, no_of_days, "Pending"))
        conn.commit()
        return invoice_id
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error creating invoice: {e}")
        return None
    finally:
        conn.close()

# Submit payment function to create an invoice and simulate payment
def submit_payment(first_name, last_name, card_number, expiry_date, cvv, car_id, reg_no, start_date, end_date, daily_rate, no_of_days, contact_no, window):
    total_price = daily_rate * no_of_days

    # Combine first name and last name
    customer_name = f"{first_name} {last_name}"

    if process_payment(card_number, expiry_date, cvv, customer_name):
        # Create invoice using the details from the payment form
        invoice_id = create_invoice(car_id, reg_no, customer_name, contact_no, start_date, end_date, total_price, no_of_days)
        if invoice_id:
            messagebox.showinfo("Payment Completed", f"Payment Successful!\nInvoice ID: {invoice_id}")
            # Close the payment window after successful payment
            window.destroy()  # Close the window after payment is successful
        else:
            messagebox.showerror("Invoice Error", "Failed to generate invoice. Please try again.")
    else:
        messagebox.showerror("Payment Error", "Payment failed. Please check your details and try again.")
        window.destroy()

# Function to simulate payment (this would be replaced with actual payment API integration)
def process_payment(card_number, expiry_date, cvv, customer_name):
    if len(card_number) != 16 or not card_number.isdigit():
        messagebox.showerror("Payment Error", "Invalid card number.")
        return False

    if len(cvv) != 3 or not cvv.isdigit():
        messagebox.showerror("Payment Error", "Invalid CVV.")
        return False

    messagebox.showinfo("Payment Success", f"Payment processed successfully for {customer_name}!")
    return True

# Function to handle the payment window
def create_payment_window(car_id, reg_no, first_name, last_name, start_date, end_date, daily_rate, no_of_days, total_amount, contact_no):
    window = Tk()
    window.geometry("500x600")
    window.title("Payment - Car Booking System")
    window.config(bg="#2C3E50")

    # Main frame to hold the payment form
    main_frame = Frame(window, bg="#ECF0F1")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Title text
    title_label = Label(main_frame, text="Payment Details", font=("Helvetica", 25, "bold"), bg="#ECF0F1", fg="#2C3E50")
    title_label.pack(pady=20)

    # First Name entry
    first_name_label = Label(main_frame, text="First Name", font=("Helvetica", 14), bg="#ECF0F1")
    first_name_label.pack(pady=5)
    first_name_entry = Entry(main_frame, font=("Helvetica", 14))
    first_name_entry.pack(pady=5)

    # Last Name entry
    last_name_label = Label(main_frame, text="Last Name", font=("Helvetica", 14), bg="#ECF0F1")
    last_name_label.pack(pady=5)
    last_name_entry = Entry(main_frame, font=("Helvetica", 14))
    last_name_entry.pack(pady=5)

    # Card details (card number, expiry, cvv)
    card_number_label = Label(main_frame, text="Card Number", font=("Helvetica", 14), bg="#ECF0F1")
    card_number_label.pack(pady=5)
    card_number_entry = Entry(main_frame, font=("Helvetica", 14))
    card_number_entry.pack(pady=5)

    expiry_label = Label(main_frame, text="Expiry Date", font=("Helvetica", 14), bg="#ECF0F1")
    expiry_label.pack(pady=5)
    expiry_entry = Entry(main_frame, font=("Helvetica", 14))
    expiry_entry.pack(pady=5)

    cvv_label = Label(main_frame, text="CVV", font=("Helvetica", 14), bg="#ECF0F1")
    cvv_label.pack(pady=5)
    cvv_entry = Entry(main_frame, font=("Helvetica", 14))
    cvv_entry.pack(pady=5)

    pay_button = Button(main_frame, text="Pay Now", font=("Helvetica", 14), bg="#1ABC9C", fg="white",
                        command=lambda: submit_payment(first_name_entry.get(), last_name_entry.get(),
                                                       card_number_entry.get(),
                                                       expiry_entry.get(), cvv_entry.get(), car_id, reg_no, start_date,
                                                       end_date,
                                                       daily_rate, no_of_days, contact_no, window))

    pay_button.pack(pady=20)

    window.mainloop()

# Main function to execute Pay_Now.py
if __name__ == "__main__":
    # Check if the correct number of arguments is passed
    if len(sys.argv) < 6:
        print("Error: Missing arguments. Please ensure that car number, total amount, customer phone, start date, and end date are passed.")
        sys.exit(1)

    selected_car_number = sys.argv[1]
    total_amount = float(sys.argv[2])
    contact_no = sys.argv[3]
    start_date = sys.argv[4]
    end_date = sys.argv[5]

    # Fetch car details based on the selected car number
    car_details = fetch_car_details()
    car_detail = next((car for car in car_details if car[0] == selected_car_number), None)

    if car_detail:
        reg_no, make_and_model, seating_capacity, daily_rate, fuel_type, manufacturer_year, transmission_type, \
        car_type, mileage, color, image_path = car_detail
        no_of_days = calculate_no_of_days(start_date, end_date)
        first_name = " "
        last_name = "  "  # Temporary static data for first name and last name
        create_payment_window(selected_car_number, reg_no, first_name, last_name, start_date, end_date,
                              daily_rate, no_of_days, total_amount, contact_no)
