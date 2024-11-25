import subprocess
from tkinter import Tk, Button, ttk, Label, messagebox, StringVar, Entry, Toplevel
import sqlite3


# Connect to the database
def connect_db():
    conn = sqlite3.connect('car_booking.db')
    return conn


# Function to fetch and display booking details based on registration number
def show_booking_details(registration_number=None):
    conn = connect_db()
    cursor = conn.cursor()

    query = '''
       SELECT ID, RegNo, CustomerName, ContactNo, StartDate, EndDate, TotalPrice, NoOfDays, Status
        FROM invoices b
    '''

    # Search by registration number
    conditions = []
    params = []

    if registration_number:
        conditions.append('RegNo = ?')
        params.append(registration_number)

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
            row[2],  # Customer Name
            row[3],  # Contact No.
            row[4],  # Start Date
            row[5],  # End Date
            row[6],  # Total Price
            row[7],  # No. of Days
            row[8]   # Status
        )
        treeview_bookings.insert("", "end", values=formatted_row)


def search_bookings():
    registration_number = entry_registration_number.get()

    if registration_number:
        show_booking_details(registration_number)
    else:
        messagebox.showwarning("Input Error", "Please enter a registration number.")


def open_booking_detail_window(booking_id):  # to approve/reject
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT ID, RegNo, CustomerName, ContactNo, StartDate, EndDate, TotalPrice, NoOfDays, Status
        FROM invoices b WHERE ID = ?
    ''', (booking_id,))

    booking = cursor.fetchone()
    conn.close()

    if booking:
        detail_window = Toplevel()
        detail_window.title("Booking Details")
        detail_window.geometry("900x600")

        Label(detail_window, text="Customer Booking Details", font=("Times New Roman", 16, "bold")).pack(pady=20)
        frame = ttk.Frame(detail_window)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Left align labels
        Label(frame, text="Booking ID:", font=("Times New Roman", 14)).grid(row=0, column=0, sticky="w", pady=5)
        Label(frame, text=booking[0], font=("Arial", 12)).grid(row=0, column=1, sticky="w", pady=5)

        Label(frame, text="Reg. No.:", font=("Times New Roman", 14)).grid(row=1, column=0, sticky="w", pady=5)
        Label(frame, text=booking[1], font=("Arial", 12)).grid(row=1, column=1, sticky="w", pady=5)

        Label(frame, text="Customer Name:", font=("Times New Roman", 14)).grid(row=2, column=0, sticky="w", pady=5)
        Label(frame, text=booking[2], font=("Arial", 12)).grid(row=2, column=1, sticky="w", pady=5)

        Label(frame, text="Contact No.:", font=("Times New Roman", 14)).grid(row=3, column=0, sticky="w", pady=5)
        Label(frame, text=booking[3], font=("Arial", 12)).grid(row=3, column=1, sticky="w", pady=5)

        Label(frame, text="Start Date:", font=("Times New Roman", 14)).grid(row=4, column=0, sticky="w", pady=5)
        Label(frame, text=booking[4], font=("Arial", 12)).grid(row=4, column=1, sticky="w", pady=5)

        Label(frame, text="End Date:", font=("Times New Roman", 14)).grid(row=5, column=0, sticky="w", pady=5)
        Label(frame, text=booking[5], font=("Arial", 12)).grid(row=5, column=1, sticky="w", pady=5)

        Label(frame, text="Total Price:", font=("Times New Roman", 14)).grid(row=6, column=0, sticky="w", pady=5)
        Label(frame, text="RM" + str(booking[6]), font=("Arial", 12)).grid(row=6, column=1, sticky="w", pady=5)

        Label(frame, text="Status:", font=("Times New Roman", 14)).grid(row=7, column=0, sticky="w", pady=5)
        Label(frame, text=booking[7], font=("Arial", 12)).grid(row=7, column=1, sticky="w", pady=5)

        # Approve and Reject buttons
        Button(frame, text="Approve", command=lambda: update_booking_status(booking[0], "Approved", detail_window),
               bg="green", fg="white", font=("Arial", 12)).grid(row=8, column=0, pady=20, padx=5, sticky="ew")

        Button(frame, text="Reject", command=lambda: update_booking_status(booking[0], "Rejected", detail_window),
               bg="red", fg="white", font=("Arial", 12)).grid(row=8, column=1, pady=20, padx=5, sticky="ew")


def update_booking_status(booking_id, status, detail_window):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE invoices SET Status = ? WHERE ID = ?', (status, booking_id))
    conn.commit()
    conn.close()

    show_booking_details()  # Refresh the bookings
    detail_window.destroy()  # Close the detail window
    messagebox.showinfo("Success", f"Booking {status.lower()} successfully!")


def go_back():
    window.destroy()  # Close the current window
    subprocess.Popen(["python", "Admin_Panel.py"])  # Open the admin panel


def view_booking_page():
    global window, treeview_bookings, entry_registration_number
    window = Tk()
    window.geometry("1200x600")
    window.title("Car Rental - Booking Details")

    # Title label
    title_label = Label(window, text="Manage Booking Details", font=("Times New Roman", 14))
    title_label.pack(pady=10)

    # Input field for registration number search
    Label(window, text="Registration No.:", font=("Arial", 10)).pack(pady=5)
    entry_registration_number = Entry(window, font=("Arial", 10))
    entry_registration_number.pack(pady=5)

    Button(window, text="Search", command=search_bookings, bg="blue", fg="white", font=("Arial", 11)).pack(pady=10)

    # Define the columns for the Treeview
    treeview_bookings = ttk.Treeview(window, columns=("ID", "Reg. No.", "Customer Name",
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

    Button(window, text="Back", command=go_back, bg="grey", fg="white", font=("Arial", 11)).pack(pady=20)

    window.mainloop()


view_booking_page()
