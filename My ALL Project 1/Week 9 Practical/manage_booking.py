import subprocess
from tkinter import Tk, Button, ttk, Label, messagebox, StringVar, Entry, Toplevel
import sqlite3


# Connect to the database
def connect_db():
    conn = sqlite3.connect('car_details.db')
    return conn


# Function to fetch and display booking details based on date range
def show_booking_details(start_date=None, end_date=None):
    conn = connect_db()
    cursor = conn.cursor()

    query = '''
        SELECT b.id, c.registration_number, c.make_and_model, b.customer_name, b.contact_number, 
               b.rental_start_date, b.rental_end_date, b.total_price, 
               COALESCE(julianday(b.rental_end_date) - julianday(b.rental_start_date), 0) AS days, b.status
        FROM bookings b
        JOIN cars c ON b.car_id = c.id
    '''

    # Search by date range
    conditions = []
    params = []

    if start_date and end_date:
        conditions.append('b.rental_start_date >= ? AND b.rental_end_date <= ?')
        params.extend([start_date, end_date])

    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    # Clear previous entries in the Treeview
    for item in treeview_bookings.get_children():
        treeview_bookings.delete(item)

    # Insert the fetched rows into the Treeview
    for row in rows:
        formatted_row = (
            row[0],  # ID
            row[1],  # Reg. No.
            row[2],  # Make & Model
            row[3],  # Customer Name
            row[4],  # Contact No.
            row[5],  # Start Date
            row[6],  # End Date
            row[7],  # Total Price
            row[8],  # No. of Days
            row[9]   # Status
        )
        treeview_bookings.insert("", "end", values=formatted_row)


def search_bookings():
    start_date = entry_start_date.get()
    end_date = entry_end_date.get()

    if start_date and end_date:
        show_booking_details(start_date, end_date)
    else:
        messagebox.showwarning("Input Error", "Please enter both start and end dates.")


def open_booking_detail_window(booking_id):      #to approve/reject
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT b.id, c.registration_number, c.make_and_model, b.customer_name, b.contact_number,
               b.rental_start_date, b.rental_end_date, b.total_price, b.status
        FROM bookings b
        JOIN cars c ON b.car_id = c.id
        WHERE b.id = ?
    ''', (booking_id,))

    booking = cursor.fetchone()
    conn.close()

    if booking:
        detail_window = Toplevel()
        detail_window.title("Booking Details")
        detail_window.geometry("900x900")

        Label(detail_window, text="Customer Booking Details", font=("Times New Roman", 16, "bold")).pack(pady=20)
        frame = ttk.Frame(detail_window)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Left align labels
        Label(frame, text="Booking ID:", font=("Times New Roman", 14)).grid(row=0, column=0, sticky="w", pady=5)
        Label(frame, text=booking[0], font=("Arial", 12)).grid(row=0, column=1, sticky="w", pady=5)

        Label(frame, text="Reg. No.:", font=("Times New Roman", 14)).grid(row=1, column=0, sticky="w", pady=5)
        Label(frame, text=booking[1], font=("Arial", 12)).grid(row=1, column=1, sticky="w", pady=5)

        Label(frame, text="Make & Model:", font=("Times New Roman", 14)).grid(row=2, column=0, sticky="w", pady=5)
        Label(frame, text=booking[2], font=("Arial", 12)).grid(row=2, column=1, sticky="w", pady=5)

        Label(frame, text="Customer Name:", font=("Times New Roman", 14)).grid(row=3, column=0, sticky="w", pady=5)
        Label(frame, text=booking[3], font=("Arial", 12)).grid(row=3, column=1, sticky="w", pady=5)

        Label(frame, text="Contact No.:", font=("Times New Roman", 14)).grid(row=4, column=0, sticky="w", pady=5)
        Label(frame, text=booking[4], font=("Arial", 12)).grid(row=4, column=1, sticky="w", pady=5)

        Label(frame, text="Start Date:", font=("Times New Roman", 14)).grid(row=5, column=0, sticky="w", pady=5)
        Label(frame, text=booking[5], font=("Arial", 12)).grid(row=5, column=1, sticky="w", pady=5)

        Label(frame, text="End Date:", font=("Times New Roman", 14)).grid(row=6, column=0, sticky="w", pady=5)
        Label(frame, text=booking[6], font=("Arial", 12)).grid(row=6, column=1, sticky="w", pady=5)

        Label(frame, text="Total Price:", font=("Times New Roman", 14)).grid(row=7, column=0, sticky="w", pady=5)
        Label(frame, text="RM" + str(booking[7]), font=("Arial", 12)).grid(row=7, column=1, sticky="w", pady=5)

        Label(frame, text="Status:", font=("Times New Roman", 14)).grid(row=8, column=0, sticky="w", pady=5)
        Label(frame, text=booking[8], font=("Arial", 12)).grid(row=8, column=1, sticky="w", pady=5)

        Button(frame, text="Approve", command=lambda: update_booking_status(booking[0], "Approved", detail_window),
               bg="green", fg="black", font=("Arial",11)).grid(row=9, column=0, pady=10, sticky="ew")
        Button(frame, text="Reject", command=lambda: update_booking_status(booking[0], "Rejected", detail_window),
               bg="red", fg="black", font=("Arial",11)).grid(row=9, column=1, pady=10, sticky="ew")


def update_booking_status(booking_id, status, detail_window):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE bookings SET status = ? WHERE id = ?', (status, booking_id))
    conn.commit()
    conn.close()

    show_booking_details()
    detail_window.destroy()  # Close the detail window
    messagebox.showinfo("Success", f"Booking {status.lower()} successfully!")


def go_back():
    window.destroy()  # Close the current window
    subprocess.Popen(["python", "admin_panel.py"])  # Open the admin panel


def view_booking_page():
    global window, treeview_bookings, entry_start_date, entry_end_date
    window = Tk()
    window.geometry("1200x600")
    window.title("Car Rental - Booking Details")

    # Title label
    title_label = Label(window, text="Manage Booking Details", font=("Times New Roman", 14))
    title_label.pack(pady=10)

    # Input fields for date range search
    Label(window, text="Start Date (YYYY-MM-DD):", font=("Arial", 10)).pack(pady=5)
    entry_start_date = Entry(window, font=("Arial", 10))
    entry_start_date.pack(pady=5)

    Label(window, text="End Date (YYYY-MM-DD):", font=("Arial", 10)).pack(pady=5)
    entry_end_date = Entry(window, font=("Arial", 10))
    entry_end_date.pack(pady=5)

    Button(window, text="Search", command=search_bookings, bg="blue", fg="white", font=("Arial", 11)).pack(pady=10)

    # Define the columns for the Treeview
    treeview_bookings = ttk.Treeview(window, columns=("ID", "Reg. No.", "Make & Model", "Customer Name",
                                                      "Contact No.", "Start Date", "End Date", "Total Price",
                                                      "No. of Days", "Status"), show="headings")

    # Define headings
    for col in treeview_bookings["columns"]:
        treeview_bookings.heading(col, text=col)

    # Define column widths
    for col in treeview_bookings["columns"]:
        treeview_bookings.column(col, width=100, anchor="center")

    treeview_bookings.pack(pady=20, fill="x")   #add treeview to GUI

    # Bind double-click event to open booking details
    treeview_bookings.bind("<Double-1>", lambda event: open_booking_detail_window(
        treeview_bookings.item(treeview_bookings.selection())['values'][0]))

    Button(window, text="Back", command=go_back, bg="orange", fg="black", font=("Arial", 11)).pack(pady=10)

    window.mainloop()


view_booking_page()
