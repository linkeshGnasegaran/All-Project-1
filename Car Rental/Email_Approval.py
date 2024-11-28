import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import customtkinter as ctk
from tkinter import messagebox, ttk, Tk
from tkinter.font import Font

# Create the main window
root = Tk()
root.title("Car Booking Management")
root.state('zoomed')  # Maximize the main window

# Function to send an email
def send_email(to_email, subject, message):
    try:
        from_email = "rubini8582@gmail.com"
        from_password = "vsin cbfp crpt dzfa"
        server = smtplib.SMTP(host='smtp.gmail.com', port=587)
        server.starttls()
        server.login(from_email, from_password)
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, _subtype='plain'))
        server.send_message(msg)
        server.quit()
        messagebox.showinfo(title="Success", message="Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")
        messagebox.showerror(title="Error", message=f"Failed to send email: {e}")

# Function to update booking status
def update_status(booking_id, status, customer_email):
    conn = sqlite3.connect('car_rental.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE invoices SET status = ? WHERE id = ?", (status, booking_id))
    conn.commit()
    conn.close()
    messagebox.showinfo(title="Success", message=f"Booking {status} successfully.")
    send_email(to_email=customer_email, subject=f"Booking {status}",
               message=f"Your booking (ID: {booking_id}) has been {status}.")
    fetch_bookings()

# Function to open the booking details window
def open_booking_window(event):
    selected_item = treeview.selection()
    if selected_item:
        booking = treeview.item(selected_item, 'values')
        booking_id = booking[0]
        car_id = booking[1]
        customer_name = booking[2]
        customer_email = booking[3]
        status = booking[4]
        action_window = ctk.CTk()  # Use CustomTkinter for consistency
        action_window.title(f"Booking ID: {booking_id} - Approve or Reject")
        # Maximize the booking details window on opening
        action_window.state('zoomed')

        # Display booking details with spacing
        details_text = (f"Booking Details:\n\n"
                        f"Booking ID: {booking_id}\n"
                        f"Car ID: {car_id}\n"
                        f"Customer Name: {customer_name}\n"
                        f"Email: {customer_email}\n"
                        f"Status: {status}")
        details_label = ctk.CTkLabel(action_window, text=details_text, justify="left", padx=10, pady=10)
        details_label.pack(pady=20)

        # Approve button with green color
        approve_button = ctk.CTkButton(action_window, text="Approve", fg_color="green", hover_color="darkgreen",
                                       command=lambda: update_status(booking_id, "Approved", customer_email))
        approve_button.pack(pady=10)

        # Reject button with red color
        reject_button = ctk.CTkButton(action_window, text="Reject", fg_color="red", hover_color="darkred",
                                      command=lambda: update_status(booking_id, "Rejected", customer_email))
        reject_button.pack(pady=10)
        action_window.mainloop()

# Function to fetch the email from the Register table using contact number
def fetch_email(contact_no):
    conn = sqlite3.connect('car_rental.db')
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM Register WHERE contact = ?", (contact_no,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# Function to fetch and display bookings
def fetch_bookings(status_filter=None):
    # Clear existing treeview entries
    for item in treeview.get_children():
        treeview.delete(item)

    conn = sqlite3.connect('car_booking.db')
    cursor = conn.cursor()

    if status_filter:
        cursor.execute("SELECT ID, RegNo, CustomerName, ContactNo, StartDate, EndDate, TotalPrice, NoOfDays, Status FROM invoices WHERE status = ?",
                       (status_filter,))
    else:
        cursor.execute("SELECT ID, RegNo, CustomerName, ContactNo, StartDate, EndDate, TotalPrice, NoOfDays, Status FROM invoices")

    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        contact_no = row[3]
        email = fetch_email(contact_no)
        treeview.insert("", "end", values=(row[0], row[1], row[2], email, row[8]))

# Function to search bookings by status
def search_by_status():
    selected_status = status_combobox.get()
    fetch_bookings(status_filter=selected_status)

# Set up CustomTkinter widgets for the status search section
form_frame = ctk.CTkFrame(root)
form_frame.pack(pady=20, padx=20, fill="x")

# Status Search Section
status_label = ctk.CTkLabel(form_frame, text="Search by Status:")
status_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
status_combobox = ctk.CTkComboBox(form_frame, values=["Pending", "Approved", "Rejected"])
status_combobox.grid(row=0, column=1, padx=10, pady=10)
search_button = ctk.CTkButton(form_frame, text="Search", command=search_by_status)
search_button.grid(row=1, column=0, columnspan=2, pady=10)

# Set up Treeview for displaying bookings
columns = ("ID", "Car ID", "Customer Name", "Email", "Status")
treeview = ttk.Treeview(root, columns=columns, show="headings")
treeview.pack(padx=10, pady=10, fill="both", expand=True)

for col in columns:
    treeview.heading(col, text=col, anchor="center")
    treeview.column(col, width=150, anchor="center", minwidth=100)

font = Font(family="Helvetica", size=12)
treeview.tag_configure('large_font', font=font)

# Bind event to handle row selection
treeview.bind("<ButtonRelease-1>", open_booking_window)

# Fetch and display bookings (all bookings initially)
fetch_bookings()

# Run the Tkinter event loop
root.mainloop()
