from tkinter import Tk, Button, ttk, messagebox
import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os
import subprocess

# Connect to the database
def connect_db():
    conn = sqlite3.connect('car_booking.db')
    return conn

# Set up database and create tables if they don't exist
def setup_database():
    conn = connect_db()
    cursor = conn.cursor()

    # Create cars table
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS cars (
            ID INTEGER PRIMARY KEY,
            RegNo TEXT NOT NULL,
            contactNo TEXT NOT NULL
        )
    ''')

    # Create invoices table
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

    # Insert sample data if invoices table is empty
    cursor.execute("SELECT COUNT(*) FROM invoices")
    if cursor.fetchone()[0] == 0:
        # Insert example data
        cursor.execute(''' 
            INSERT INTO invoices (ID, RegNo, CustomerName, ContactNo, StartDate, EndDate, TotalPrice, NoOfDays, Status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', ('B001', 'AB1234CD', 'John Doe', '0123456789', '2024-11-20', '2024-11-25', 150.0, 5, 'Confirmed'))

    conn.commit()
    conn.close()

# Fetch booking details from the database
def show_booking_details():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(''' 
        SELECT ID, RegNo, CustomerName, ContactNo, StartDate, EndDate, TotalPrice, NoOfDays, Status
        FROM invoices
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows

# Add header and footer to the PDF
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
    fields = ["Booking ID", "Registration No.", "Customer Name", "Contact Number",
              "Rental Start Date", "Rental End Date", "Total Price (RM)", "No Of Days", "Status"]

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


def go_back(event=None):  # Accept the implicit event argument
    window.destroy()  # Close the current window
    subprocess.Popen(["python", "Admin_Panel.py"])  # Open the admin panel


# Save and print the selected booking details
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

# Display booking details in the treeview
def display_booking_details():
    bookings = show_booking_details()

    for booking in bookings:
        treeview_bookings.insert("", "end", values=(
            booking[0], booking[1], booking[2], booking[3], booking[4], booking[5], booking[6], booking[7], booking[8]
        ))

# GUI for displaying booking information
def booking_info_page():
    setup_database()  # Ensure database and tables are set up before displaying the UI

    global window
    window = Tk()
    window.geometry("1000x500")
    window.title("Customer Booking Details")

    global treeview_bookings
    treeview_bookings = ttk.Treeview(window, columns=("ID", "Reg_No", "Customer_Name",
                                                      "Contact_No", "Start_Date", "End_Date",
                                                      "Total_Price", "No_Of_Days", "Status"), show="headings")

    headers = ["ID", "Reg. No.", "Customer Name", "Contact No.", "Start Date", "End Date",
               "Total Price", "No Of Days", "Status"]

    # Define headings and center alignment
    for header, column in zip(headers, treeview_bookings["columns"]):
        treeview_bookings.heading(column, text=header)
        treeview_bookings.column(column, anchor="center", width=100)

    treeview_bookings.pack(pady=20, fill="x")

    # Combined Save and Print button
    Button(window, text="Save as PDF", command=save_and_print_selected_booking,
           bg="blue", fg="white").pack(pady=10)

    Button(window, text="Back", command=lambda: go_back(), bg="grey", fg="white", font=("Arial", 11)).pack(pady=20)

    display_booking_details()
    window.mainloop()


# Run the function to display the booking details page
if __name__ == "__main__":
    booking_info_page()
