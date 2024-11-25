from tkinter import Tk, Entry, Button, Label, ttk, messagebox
import sqlite3
from datetime import datetime
from PIL import Image, ImageTk
import subprocess

def connect_db():
    conn = sqlite3.connect('car_details.db')
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_id INTEGER,
            customer_name TEXT,
            contact_number TEXT,
            rental_start_date TEXT,
            rental_end_date TEXT,
            total_price REAL,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY(car_id) REFERENCES cars(id)
        )
    ''')
    conn.commit()
    return conn

def show_available_cars():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(''' 
        SELECT id, registration_number, make_and_model, daily_rate, image_path 
        FROM cars 
        WHERE id NOT IN (SELECT car_id FROM bookings)
    ''')
    rows = cursor.fetchall()
    conn.close()

    # Clear the current entries in the treeview
    for item in treeview_cars.get_children():
        treeview_cars.delete(item)

    # Insert the available cars into the treeview
    for row in rows:
        treeview_cars.insert("", "end", values=row)

def calculate_total_price():
    selected_item = treeview_cars.selection()
    if selected_item:
        item = treeview_cars.item(selected_item)
        daily_rate = float(item['values'][3])  # Fetch the daily rate from the selected car

        rental_start_date_str = entry_start_date.get()
        rental_end_date_str = entry_end_date.get()

        try:
            rental_start_date = datetime.strptime(rental_start_date_str, '%Y-%m-%d')
            rental_end_date = datetime.strptime(rental_end_date_str, '%Y-%m-%d')

            # Calculate rental duration
            duration = (rental_end_date - rental_start_date).days
            if duration <= 0:
                raise ValueError("Rental end date must be after start date.")

            total_price = daily_rate * duration

            breakdown_message = (
                f"Daily Rate: RM {daily_rate:.2f}\n"
                f"Rental Days: {duration}\n"
                f"Total Price: RM {total_price:.2f}"
            )
            label_breakdown.config(text=breakdown_message)
            return total_price

        except ValueError as e:
            return None
    else:
        messagebox.showwarning("Selection Error", "Please select a car to book.")
        return None

def update_total_price(event=None):
    calculate_total_price()

def book_car():
    selected_item = treeview_cars.selection()
    if selected_item:
        item = treeview_cars.item(selected_item)
        car_id = item['values'][0]  # Get car ID from the selected row
        customer_name = entry_name.get()
        contact_number = entry_contact.get()
        rental_start_date = entry_start_date.get()
        rental_end_date = entry_end_date.get()

        if customer_name and contact_number and rental_start_date and rental_end_date:
            total_price = calculate_total_price()
            if total_price is None:
                return

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(''' 
                INSERT INTO bookings (car_id, customer_name, contact_number, rental_start_date, rental_end_date, total_price)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (car_id, customer_name, contact_number, rental_start_date, rental_end_date, total_price))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Car booked successfully!")

            show_available_cars()

        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
    else:
        messagebox.showwarning("Selection Error", "Please select a car to book.")

def display_selected_image(event):
    selected_item = treeview_cars.selection()
    if selected_item:
        item = treeview_cars.item(selected_item)
        car_id = item['values'][0]  # Get car ID from the selected row

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT image_path FROM cars WHERE id = ?", (car_id,))
        image_path = cursor.fetchone()

        if image_path and image_path[0]:
            try:
                img = Image.open(image_path[0])
                img = img.resize((200, 150), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(img)

                # Display the image
                label_image.config(image=img)
                label_image.image = img
            except Exception as e:
                print(f"Error loading image: {e}")
                label_image.config(image='')
        else:
            label_image.config(image='')

def go_back():
    window.destroy()
    subprocess.Popen(["python", "customer_panel.py"])

#Window design
window = Tk()
window.geometry("800x700")  # Increase window height
window.title("Car Rental - Customer Booking")

Label(window, text="Car Rental Booking", font=("Times New Roman", 18)).place(x=300, y=10)

Label(window, text="Available Cars:", font=("Inter Bold", 14)).place(x=50, y=60)

treeview_cars = ttk.Treeview(window, columns=("ID", "Reg. No.", "Make & Model", "Rate (RM)"), show="headings")
treeview_cars.heading("ID", text="ID")
treeview_cars.heading("Reg. No.", text="Reg. No.")
treeview_cars.heading("Make & Model", text="Make & Model")
treeview_cars.heading("Rate (RM)", text="Rate (RM)")
treeview_cars.column("ID", width=50, anchor="center")
treeview_cars.column("Reg. No.", width=100, anchor="center")
treeview_cars.column("Make & Model", width=150, anchor="center")
treeview_cars.column("Rate (RM)", width=100, anchor="center")
treeview_cars.place(x=50, y=100, width=700, height=150)

treeview_cars.bind("<<TreeviewSelect>>", display_selected_image)

Label(window, text="Book a Car:", font=("Inter Bold", 14)).place(x=50, y=280)

Label(window, text="Customer Name:").place(x=50, y=320)
entry_name = Entry(window, width=30)
entry_name.place(x=180, y=320)

Label(window, text="Contact Number:").place(x=50, y=360)
entry_contact = Entry(window, width=30)
entry_contact.place(x=180, y=360)

Label(window, text="Rental Start Date (YYYY-MM-DD):").place(x=50, y=400)
entry_start_date = Entry(window, width=30)
entry_start_date.place(x=250, y=400)
entry_start_date.bind("<FocusOut>", update_total_price)  # Auto update price when date is entered

Label(window, text="Rental End Date (YYYY-MM-DD):").place(x=50, y=440)
entry_end_date = Entry(window, width=30)
entry_end_date.place(x=250, y=440)
entry_end_date.bind("<FocusOut>", update_total_price)  # Auto update price when date is entered

label_breakdown = Label(window, text="", font=("Times New Roman", 12), justify="left")
label_breakdown.place(x=50, y=480)

# Label to display the selected car image
label_image = Label(window)
label_image.place(x=500, y=280, width=200, height=150)

# Add button to calculate total price
button_add = Button(window, text="Calculate Total Price", command=calculate_total_price, bg="blue", fg="white")
button_add.place(x=50, y=550)

# Button to book the selected car
button_book = Button(window, text="Book Car", command=book_car, bg="green", fg="white")
button_book.place(x=200, y=550)

# Button to go back to the previous page
button_back = Button(window, text="Back", command=go_back, bg="orange", fg="white")
button_back.place(x=350, y=550)

show_available_cars()

window.mainloop()
