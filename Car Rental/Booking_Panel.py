import sqlite3
from tkinter import Tk, ttk, Canvas, Button, Label, Frame
from tkcalendar import DateEntry
from datetime import datetime
from PIL import Image, ImageTk
import subprocess
import os
import sys


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


# Function to display the car image in the GUI
def display_image(image_path, label):
    try:
        img = Image.open(image_path)
        img = img.resize((150, 150), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        label.config(image=img)
        label.image = img
    except Exception as e:
        label.config(text="No Image Available", anchor="center")
        label.image = None


# Function to calculate the booking price based on the dates
def calculate_price(start_date, end_date, daily_rate):
    if end_date < start_date:
        return 0  # Invalid date range, no price
    days_diff = (end_date - start_date).days
    return days_diff * daily_rate


# Function to handle car booking and trigger the payment process
def book_car(selected_car_number, total_amount, start_date, end_date, contact_no, email):
    print(
        f"Booking car with number: {selected_car_number}, Total amount: {total_amount}, Contact No: {contact_no}")  # Debugging line

    payment_window_path = r"C:\Users\Honor\PycharmProjects\ALL 1 Project\Car Rental\Payment.py"
    if os.path.exists(payment_window_path):
        subprocess.run([
            'python', payment_window_path, selected_car_number, str(total_amount), contact_no, email,
            str(start_date), str(end_date)])  # Pass the correct arguments
    else:
        print("Error: Payment.py file not found.")


# Function to update the displayed price when dates are selected
def update_price(start_entry, end_entry, price_label, daily_rate):
    start_date = start_entry.get_date()
    end_date = end_entry.get_date()

    if start_date and end_date:
        if end_date >= start_date:
            total_days = (end_date - start_date).days
            total_price = total_days * daily_rate
            price_label.config(text=f"Total Price: RM {total_price:.2f}")
            return total_price
        else:
            price_label.config(text="End date must be after the start date.")
            return 0
    else:
        price_label.config(text="Please select both dates.")
        return 0


# Function to create the car frame for each car listing
def create_car_frame(car, second_frame, contact_no, email):
    car_frame = Frame(second_frame, bg="#ffffff", bd=2, relief="raised")
    car_frame.pack(fill="x", expand=False, padx=10, pady=10)
    car_frame.config(width=900, height=300)
    car_frame.pack_propagate(False)

    car_image_label = Label(car_frame, bg="#F4F6F6", width=200, height=200)
    car_image_label.place(x=10, y=25)
    display_image(car[10], car_image_label)

    car_details = f"Registration Number: {car[0]}\nMake & Model: {car[1]}\nSeating Capacity: {car[2]}\n" \
                  f"Daily Rate (RM): {car[3]}\nFuel Type: {car[4]}\nManufacturer Year: {car[5]}\n" \
                  f"Transmission Type: {car[6]}\nCar Type: {car[7]}\nMileage (km): {car[8]}\nColor: {car[9]}"
    details_label = Label(car_frame, text=car_details, font=("Helvetica", 12), bg="#ffffff", anchor="w",
                          justify="left")
    details_label.place(x=220, y=20)

    today = datetime.today().date()
    Label(car_frame, text="Start Date:", font=("Helvetica", 10), bg="#ffffff").place(x=500, y=80)
    start_entry = DateEntry(car_frame, date_pattern="yyyy-mm-dd", mindate=today)
    start_entry.place(x=580, y=80)

    Label(car_frame, text="End Date:", font=("Helvetica", 10), bg="#ffffff").place(x=500, y=120)
    end_entry = DateEntry(car_frame, date_pattern="yyyy-mm-dd", mindate=today)
    end_entry.place(x=580, y=120)

    price_label = Label(car_frame, text="Total Price: RM 0", font=("Helvetica", 12), bg="#ffffff")
    price_label.place(x=700, y=140)

    daily_rate = car[3]

    def update_end_date(*args):
        selected_start_date = start_entry.get_date()
        end_entry.config(mindate=selected_start_date)  # Update the mindate
        if end_entry.get_date() < selected_start_date:  # Adjust the end date if it's earlier than the start date
            end_entry.set_date(selected_start_date)

    start_entry.bind("<<DateEntrySelected>>", lambda e: (update_end_date(),
                                                         update_price(start_entry, end_entry, price_label, daily_rate)))
    end_entry.bind("<<DateEntrySelected>>", lambda e: update_price(start_entry, end_entry, price_label, daily_rate))

    Button(car_frame, text="Book Now",
           command=lambda c=car[0]: book_car(c, update_price(start_entry, end_entry, price_label, daily_rate),
                                             start_entry.get_date(), end_entry.get_date(), contact_no, email),
           bg="#1ABC9C", fg="#ffffff", font=("Helvetica", 12, "bold")).place(x=720, y=220)


# Function to create the booking window
def create_booking_window(contact_no, email):
    window = Tk()
    window.geometry("1000x700")
    window.title("Car Booking System")
    window.config(bg="#2C3E50")

    main_frame = Frame(window, bg="#ECF0F1")
    main_frame.pack(fill='both', expand=True)

    my_canvas = Canvas(main_frame, bg="#ECF0F1", highlightthickness=3)
    my_canvas.pack(side='left', fill='both', expand=1)

    scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=my_canvas.yview)
    scrollbar.pack(side='right', fill='y')

    my_canvas.configure(yscrollcommand=scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    second_frame = Frame(my_canvas, bg="#ECF0F1")
    my_canvas.create_window((40, 40), window=second_frame, anchor="nw")

    title_label = Label(second_frame, text="Car Booking System", font=("Helvetica", 30, "bold"), bg="#ECF0F1",
                        fg="#2C3E50")
    title_label.pack(pady=20)

    cars = fetch_car_details()
    if not cars:
        Label(second_frame, text="No cars available for booking.", font=("Helvetica", 14), bg="#ECF0F1").pack(pady=20)
        return

    for car in cars:
        create_car_frame(car, second_frame, contact_no, email)

    window.mainloop()


# Ensure we are getting the correct email and contact_no
if __name__ == "__main__":
    email = sys.argv[1] if len(sys.argv) > 1 else "default@example.com"
    contact_no = sys.argv[2] if len(sys.argv) > 2 else "1234567890"
    create_booking_window(contact_no, email)
