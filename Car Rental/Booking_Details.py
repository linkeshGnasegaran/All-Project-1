import sys
import sqlite3
from tkinter import Tk, Button, ttk, Label, messagebox
import subprocess


class BookingManager:
    def __init__(self, email):
        self.email = email
        self.contact_no = None
        self.window = None
        self.treeview_bookings = None
        self.clear_button = None

    def connect_db(self):
        """Establish a connection to the database."""
        return sqlite3.connect("car_booking.db")

    def fetch_customer_details(self):
        """Fetch customer details using the provided email."""
        try:
            conn = sqlite3.connect("car_rental.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT first_name, last_name, email, contact_no
                FROM Register WHERE email = ?
            """, (self.email,))
            customer_data = cursor.fetchone()
            conn.close()
            if customer_data:
                self.contact_no = customer_data[3]
                return customer_data
            else:
                messagebox.showerror("Error", "Customer not found.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
        return None

    def show_booking_details(self):
        """Display booking details in the Treeview and show status updates."""
        if not self.contact_no:
            messagebox.showwarning("Error", "Contact number not found.")
            return

        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ID, RegNo, CustomerName, ContactNo, StartDate, EndDate, TotalPrice, NoOfDays, Status
            FROM invoices
            WHERE ContactNo = ?
        """, (self.contact_no,))
        rows = cursor.fetchall()
        conn.close()

        # Clear previous data in Treeview
        self.treeview_bookings.delete(*self.treeview_bookings.get_children())

        # Insert fetched data into Treeview
        if rows:
            for row in rows:
                self.treeview_bookings.insert("", "end", values=row)

                # Check if the booking is "approved" or "rejected"
                booking_status = row[8]  # Status is the last column (index 8)
                if booking_status.lower() in ["approved", "rejected"]:
                    self.display_status_update(row, booking_status)
        else:
            messagebox.showinfo("No Bookings", "No bookings found.")

    def display_status_update(self, row, status):
        """Display the booking details in a separate window with the status update."""
        status_window = Tk()
        status_window.title(f"Booking {status.capitalize()}")

        Label(status_window, text=f"Booking {status.capitalize()}", font=("Arial", 16)).pack(pady=10)

        details = [
            ("Booking ID", row[0]),
            ("Registration No.", row[1]),
            ("Customer Name", row[2]),
            ("Contact No.", row[3]),
            ("Start Date", row[4]),
            ("End Date", row[5]),
            ("Total Price", row[6]),
            ("No. of Days", row[7]),
            ("Status", row[8])
        ]

        for detail in details:
            Label(status_window, text=f"{detail[0]}: {detail[1]}", font=("Arial", 12)).pack(pady=5)

        Button(status_window, text="Close", command=status_window.destroy, bg="orange", fg="white").pack(pady=10)
        status_window.mainloop()

    def clear_booking(self):
        """Clear an individual booking with confirmation."""
        selected_item = self.treeview_bookings.selection()
        if selected_item:
            item = self.treeview_bookings.item(selected_item)
            booking_id = item["values"][0]
            if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this booking?"):
                conn = self.connect_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM invoices WHERE ID = ?", (booking_id,))
                conn.commit()
                conn.close()
                self.show_booking_details()
                messagebox.showinfo("Success", "Booking cleared successfully.")

    def clear_all_bookings(self):
        """Clear all bookings with confirmation."""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all booking history?"):
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM invoices WHERE ContactNo = ?", (self.contact_no,))
            conn.commit()
            conn.close()
            self.show_booking_details()
            messagebox.showinfo("Success", "All booking history cleared.")

    def on_treeview_select(self, event):
        """Handle Treeview selection."""
        selected_item = self.treeview_bookings.selection()
        if selected_item:
            item = self.treeview_bookings.item(selected_item)
            booking_status = item["values"][8]
            self.clear_button.config(state="normal" if booking_status.lower() == "pending" else "disabled")

    def back_to_customer_panel(self):
        """Navigate back to the Customer Panel."""
        self.window.destroy()
        subprocess.run([sys.executable, "Customer_Panel.py", self.email])

    def view_booking_page(self):
        """Display the main booking page."""
        self.window = Tk()
        self.window.geometry("1200x500")
        self.window.title("Booking Details")

        Label(self.window, text="Your Booking Details", font=("Times New Roman", 18)).pack(pady=10)

        # Treeview setup
        self.treeview_bookings = ttk.Treeview(
            self.window,
            columns=("ID", "Reg. No.", "Customer Name", "Contact No.",
                     "Start Date", "End Date", "Total Price", "No. of Days", "Booking Status"),
            show="headings"
        )

        # Define Treeview columns
        for col in self.treeview_bookings["columns"]:
            self.treeview_bookings.heading(col, text=col)
            self.treeview_bookings.column(col, anchor="center", width=100)

        self.treeview_bookings.pack(pady=20, fill="x")
        self.treeview_bookings.bind("<<TreeviewSelect>>", self.on_treeview_select)

        # Buttons
        self.clear_button = Button(self.window, text="Clear Booking", command=self.clear_booking, bg="red", fg="white")
        self.clear_button.pack(pady=10)

        Button(self.window, text="Clear All Bookings", command=self.clear_all_bookings, bg="red", fg="white").pack(
            pady=10)
        Button(self.window, text="Back", command=self.back_to_customer_panel, bg="orange", fg="white").pack(pady=10)

        # Load booking details
        self.show_booking_details()

        self.window.mainloop()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        email = sys.argv[1]
        manager = BookingManager(email)
        if manager.fetch_customer_details():
            manager.view_booking_page()
    else:
        messagebox.showerror("Error", "Email not provided.")
