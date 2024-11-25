from tkinter import Tk, Button, ttk, messagebox
import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os


def connect_db():
    conn = sqlite3.connect('car_details.db')
    return conn


def setup_database():
    conn = connect_db()
    cursor = conn.cursor()

    # Create cars table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY,
            registration_number TEXT NOT NULL,
            make_and_model TEXT NOT NULL
        )
    ''')

    # Create bookings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY,
            car_id INTEGER NOT NULL,
            customer_name TEXT NOT NULL,
            contact_number TEXT NOT NULL,
            rental_start_date TEXT NOT NULL,
            rental_end_date TEXT NOT NULL,
            total_price REAL NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY(car_id) REFERENCES cars(id)
        )
    ''')

    # Optional: Insert example data if the tables are empty (for testing)
    cursor.execute("SELECT COUNT(*) FROM cars")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO cars (registration_number, make_and_model) VALUES ('ABC123', 'Toyota Camry')")

    cursor.execute("SELECT COUNT(*) FROM bookings")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO bookings (car_id, customer_name, contact_number, rental_start_date, rental_end_date, total_price, status) VALUES (1, 'John Doe', '1234567890', '2024-10-01', '2024-10-10', 500.00, 'Completed')")

    conn.commit()
    conn.close()


def show_booking_details():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT b.id, c.registration_number, c.make_and_model, b.customer_name, b.contact_number, 
               b.rental_start_date, b.rental_end_date, b.total_price, b.status
        FROM bookings b
        JOIN cars c ON b.car_id = c.id
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows


def add_header_footer(c, doc_title):
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, height - 50, doc_title)  # Title at the top
    c.setFont("Helvetica", 10)
    c.drawString(40, height - 65, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.line(40, height - 70, width - 40, height - 70)  # Horizontal line under the header

    # Add footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(40, 40, "Car Rental Services")
    c.drawString(width - 200, 40, "Contact: info@carrental.com")
    c.line(40, 60, width - 40, 60)  # Horizontal line above the footer

    # Page number
    c.setFont("Helvetica", 10)
    c.drawString(width - 100, 20, f"Page {c.getPageNumber()}")


# Generate PDF for selected booking
def save_selected_as_pdf(selected_booking):
    if not selected_booking:
        messagebox.showwarning("No Selection", "Please select a booking to save.")
        return None

    pdf_filename = f"selected_booking_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=A4)
    width, height = A4

    doc_title = "Car Rental Booking Details"
    add_header_footer(c, doc_title)

    c.setFont("Helvetica", 12)
    y_position = height - 100  # Start text below the header

    # Display each field vertically
    fields = ["Booking ID", "Registration No.", "Make & Model", "Customer Name", "Contact Number",
              "Rental Start Date", "Rental End Date", "Total Price (RM)", "Status"]

    for i, field in enumerate(fields):
        value = selected_booking[i]
        c.drawString(40, y_position, f"{field}: {value}")
        y_position -= 20  # Move down for the next line

        # Move to next page if out of space
        if y_position < 100:
            c.showPage()
            add_header_footer(c, doc_title)
            y_position = height - 100

    c.showPage()
    c.save()

    return pdf_filename


def save_and_print_selected_booking():
    selected_item = treeview_bookings.selection()

    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a booking to save and print.")
        return

    selected_booking = treeview_bookings.item(selected_item)["values"]

    pdf_filename = save_selected_as_pdf(selected_booking)

    if pdf_filename:
        if os.name == 'posix':  # For Linux/macOS
            os.system(f'lpr {pdf_filename}')
        elif os.name == 'nt':  # For Windows
            os.startfile(pdf_filename, "print")

        messagebox.showinfo("PDF Saved", f"Selected booking details saved as {pdf_filename}.")


def display_booking_details():
    bookings = show_booking_details()

    for booking in bookings:
        treeview_bookings.insert("", "end", values=(
            booking[0], booking[1], booking[2], booking[3], booking[4], booking[5], booking[6], booking[7], booking[8]
        ))


# GUI for displaying booking information
def booking_info_page():
    setup_database()  # Ensure database and tables are set up before displaying the UI

    window = Tk()
    window.geometry("1000x500")
    window.title("Customer Booking Details")

    global treeview_bookings
    treeview_bookings = ttk.Treeview(window, columns=("ID", "Reg. No.", "Make & Model", "Customer Name",
                                                      "Contact No.", "Start Date", "End Date",
                                                      "Total Price", "Status"), show="headings")

    headers = ["ID", "Reg. No.", "Make & Model", "Customer Name", "Contact No.", "Start Date", "End Date",
               "Total Price", "Status"]

    # Define headings and center alignment
    for header in headers:
        treeview_bookings.heading(header, text=header)
        treeview_bookings.column(header, anchor="center", width=100)

    treeview_bookings.pack(pady=20, fill="x")

    # Combined Save and Print button
    Button(window, text="Save as PDF", command=save_and_print_selected_booking,
           bg="blue", fg="white").pack(pady=10)

    display_booking_details()
    window.mainloop()


booking_info_page()
