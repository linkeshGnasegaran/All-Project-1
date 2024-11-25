import subprocess
from tkinter import Tk, Button, ttk, Label, messagebox
import sqlite3

def connect_db():
    conn = sqlite3.connect('car_details.db')
    return conn

#retrieve the booking and ar details
def show_booking_details():
    conn = connect_db()\

    cursor = conn.cursor()    #allow the execution of SQL syntax
    cursor.execute(''' 
        SELECT b.id, c.registration_number, c.make_and_model, b.customer_name, b.contact_number, 
               b.rental_start_date, b.rental_end_date, b.total_price, 
               COALESCE(julianday(b.rental_end_date) - julianday(b.rental_start_date), 0) AS days,
               b.status
        FROM bookings b
        JOIN cars c ON b.car_id = c.id
    ''') #julianday function use to count the difference between the start and end date.
    rows = cursor.fetchall()
    conn.close()

    # Clear existing data in the Treeview before inserting new rows
    for item in treeview_bookings.get_children():
        treeview_bookings.delete(item)

    # Insert fetched data into the Treeview
    for row in rows:
        treeview_bookings.insert("", "end", values=row)


# Function to handle Treeview selection
def on_treeview_select(event):
    selected_item = treeview_bookings.selection()
    if selected_item:
        item = treeview_bookings.item(selected_item)
        booking_status = item['values'][9]  # Get the status of the selected booking

        # Disable the "Clear Booking" button if the status is not "Pending"
        if booking_status.lower() != "pending":
            clear_button.config(state="disabled")  # Disable the button
        else:
            clear_button.config(state="normal")  # Enable the button


# Function to clear individual booking
def clear_booking():
    selected_item = treeview_bookings.selection()
    if selected_item:
        item = treeview_bookings.item(selected_item)
        booking_id = item['values'][0]  # booking ID
        booking_status = item['values'][9]  # booking status

        # Confirmation for pending bookings
        if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this booking?"):
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM bookings WHERE id = ?', (booking_id,))
            conn.commit()
            conn.close()

            # Refresh the booking details after deletion
            show_booking_details()
            messagebox.showinfo("Success", "Booking cleared successfully!")
    else:
        messagebox.showwarning("Selection Error", "Please select a booking to clear.")

# Function to clear all booking history
def clear_all_bookings():
    # Confirm before clearing all booking history
    if messagebox.askyesno("Clear All Bookings",
                           "Are you sure you want to clear all booking history? This action cannot be undone."):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM bookings')
        conn.commit()
        conn.close()

        # Refresh the booking details after clearing all history
        show_booking_details()
        messagebox.showinfo("Success", "All booking history cleared successfully!")


# Function to go back to the previous panel
def go_back():
    window.destroy()  # Close the current window
    subprocess.Popen(["python", "customer_panel.py"])  # Open the customer panel


# Main function to display the booking page
def view_booking_page():
    global window
    window = Tk()
    window.geometry("1200x500")
    window.title("Car Rental - Booking Details")

    Label(window, text="Your Booking Details", font=("Times New Roman", 18)).pack(pady=10)

    global treeview_bookings
    treeview_bookings = ttk.Treeview(window, columns=("ID", "Reg. No.", "Make & Model", "Customer Name",
                                                      "Contact No.", "Start Date", "End Date", "Total Price",
                                                      "No. of Days", "Booking Status"), show="headings")

    # Define headings for the Treeview
    treeview_bookings.heading("ID", text="ID")
    treeview_bookings.heading("Reg. No.", text="Reg. No.")
    treeview_bookings.heading("Make & Model", text="Make & Model")
    treeview_bookings.heading("Customer Name", text="Customer Name")
    treeview_bookings.heading("Contact No.", text="Contact No.")
    treeview_bookings.heading("Start Date", text="Start Date")
    treeview_bookings.heading("End Date", text="End Date")
    treeview_bookings.heading("Total Price", text="Total Price (RM)")
    treeview_bookings.heading("No. of Days", text="No. of Days")
    treeview_bookings.heading("Booking Status", text="Booking Status")

    # Define column widths and alignment
    treeview_bookings.column("ID", width=50, anchor="center")
    treeview_bookings.column("Reg. No.", width=100, anchor="center")
    treeview_bookings.column("Make & Model", width=150, anchor="center")
    treeview_bookings.column("Customer Name", width=150, anchor="center")
    treeview_bookings.column("Contact No.", width=100, anchor="center")
    treeview_bookings.column("Start Date", width=100, anchor="center")
    treeview_bookings.column("End Date", width=100, anchor="center")
    treeview_bookings.column("Total Price", width=100, anchor="center")
    treeview_bookings.column("No. of Days", width=100, anchor="center")
    treeview_bookings.column("Booking Status", width=100, anchor="center")

    # Pack Treeview
    treeview_bookings.pack(pady=20, fill="x")

    # Bind the selection event to on_treeview_select
    treeview_bookings.bind("<<TreeviewSelect>>", on_treeview_select)

    # Button to clear individual booking
    global clear_button
    clear_button = Button(window, text="Clear Booking", command=clear_booking, bg="red", fg="white")
    clear_button.pack(pady=10)

    # Button to clear all booking history
    clear_history_button = Button(window, text="Clear All History", command=clear_all_bookings, bg="red", fg="white")
    clear_history_button.pack(pady=10)

    # Back button
    Button(window, text="Back", command=go_back, bg="orange", fg="white").pack(pady=10)

    # Load and display booking details
    show_booking_details()

    # Start the Tkinter main loop
    window.mainloop()


view_booking_page()
