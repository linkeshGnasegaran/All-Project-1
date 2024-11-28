import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os
import sys


# Connect to the database
def connect_db():
    conn = sqlite3.connect('car_booking.db')
    return conn


# Fetch booking details based on the contact number passed from customer profile
def show_booking_details(contact_no):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(''' 
        SELECT ID, RegNo, CustomerName, ContactNo, StartDate, EndDate, TotalPrice, NoOfDays, Status
        FROM invoices
        WHERE ContactNo = ? 
    ''', (contact_no,))

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
def display_booking_details(contact_no):
    bookings = show_booking_details(contact_no)

    for booking in bookings:
        treeview_bookings.insert("", "end", values=(
            booking[0], booking[1], booking[2], booking[3], booking[4], booking[5], booking[6], booking[7], booking[8]
        ))


# GUI for displaying booking information
def booking_info_page(contact_no):
    window = tk.Tk()
    window.geometry("1000x500")
    window.title("Customer Booking Details")

    global treeview_bookings
    treeview_bookings = ttk.Treeview(window, columns=("ID", "Reg. No.", "Customer Name",
                                                      "Contact No.", "Start Date", "End Date",
                                                      "Total Price", "No Of Days", "Status"), show="headings")

    headers = ["ID", "Reg. No.", "Customer Name", "Contact No.", "Start Date", "End Date",
               "Total Price", "No Of Days", "Status"]

    # Define headings and center alignment
    for header in headers:
        treeview_bookings.heading(header, text=header)
        treeview_bookings.column(header, anchor="center", width=100)

    treeview_bookings.pack(pady=20, fill="x")

    # Combined Save and Print button
    tk.Button(window, text="Save as PDF", command=save_and_print_selected_booking,
              bg="blue", fg="white").pack(pady=10)

    # Display the booking details filtered by contact number
    display_booking_details(contact_no)

    window.mainloop()


# Run the function to display the booking details page
if __name__ == "__main__":
    # Assuming contact_no and email are passed as command-line arguments
    if len(sys.argv) < 3:
        messagebox.showerror("Error", "Email or contact number not provided as arguments.")
    else:
        email = sys.argv[1]
        contact_no = sys.argv[2]
        booking_info_page(contact_no)
