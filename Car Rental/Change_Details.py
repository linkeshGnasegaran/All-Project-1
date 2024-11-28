import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3
import subprocess
import sys

def connect_db():
    """Establish a connection to the database."""
    return sqlite3.connect('car_rental.db')

def load_profile_image(img_path):
    """Load and resize the profile image."""
    try:
        profile_img = Image.open(img_path).resize((100, 100))  # Resize image to fit within the label
        return ImageTk.PhotoImage(profile_img)
    except FileNotFoundError:
        messagebox.showerror("Image Error", f"Profile image not found at: {img_path}")
        return None

def fetch_customer_details(email):
    """Fetch customer details from the database."""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT first_name, last_name, email, contact_no FROM Register WHERE email = ?", (email,))
        customer_data = cursor.fetchone()
        conn.close()

        if customer_data:
            return customer_data
        else:
            messagebox.showerror("Error", "Customer not found.")
            return None
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
        return None

def authenticate_and_edit(email=None):
    """Authenticate the user before granting access to edit their details."""

    def back_to_customer_panel():
        """Navigate back to the Customer Panel."""
        root.destroy()  # Close the current window
        subprocess.run([sys.executable, 'Customer_Panel.py', email])  # Pass the email as an argument

    def verify_password():
        """Verify the email and password entered by the user."""
        entered_email = email_entry.get().strip()
        password = password_entry.get().strip()

        if not entered_email or not password:
            messagebox.showerror("Error", "Please enter both email and password")
            return

        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Register WHERE email = ? AND password = ?", (entered_email, password))
            user = cursor.fetchone()

            if user:
                root.destroy()
                edit_user_details(user)  # Pass the authenticated user data to the edit screen
            else:
                messagebox.showerror("Error", "Invalid email or password")

    root = tk.Tk()
    root.title("Authenticate")
    root.geometry("300x400")

    tk.Label(root, text="Enter Email:", font=("Arial", 12)).pack(pady=5)
    email_entry = tk.Entry(root, font=("Arial", 12))
    email_entry.insert(0, email)  # Autofill email (if passed) as read-only
    email_entry.config(state="readonly")  # Make the email field read-only
    email_entry.pack(pady=5)

    tk.Label(root, text="Enter Password:", font=("Arial", 12)).pack(pady=5)
    password_entry = tk.Entry(root, font=("Arial", 12), show="*")
    password_entry.pack(pady=5)

    # Authentication Button
    tk.Button(root, text="Authenticate", font=("Arial", 12), bg="green", fg="white", command=verify_password).pack(pady=10)

    # Back Button to navigate to the Customer Panel
    tk.Button(root, text="Back", font=("Arial", 12), bg="grey", fg="white", command=back_to_customer_panel).pack(pady=5)

    root.mainloop()

def edit_user_details(user):
    """Edit user details, including email and profile picture."""
    user_id = user[0]  # Assuming the user ID is the first column in the Register table

    def update_details():
        """Update user details in the database."""
        updated_data = {
            "first_name": first_name_entry.get().strip(),
            "last_name": last_name_entry.get().strip(),
            "contact_no": contact_no_entry.get().strip(),
            "email": email_entry.get().strip(),
            "security_question": security_question_entry.get(),
            "security_answer": security_answer_entry.get().strip(),
            "password": password_entry.get().strip(),
            "address": address_entry.get().strip(),
            "profile_picture": profile_pic_path.get()
        }

        if not all(updated_data.values()):
            messagebox.showerror("Error", "All fields are required")
            return

        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(""" 
                UPDATE Register
                SET first_name = ?, last_name = ?, contact_no = ?, email = ?, security_question = ?, 
                    security_answer = ?, password = ?, address = ?, profile_picture = ?
                WHERE id = ? 
            """, (*updated_data.values(), user_id))
            conn.commit()

        messagebox.showinfo("Success", "Details updated successfully!")

    def select_profile_picture():
        """Allow the user to select a profile picture."""
        file_path = filedialog.askopenfilename(title="Select Profile Picture",
                                               filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            profile_pic_path.set(file_path)

    def remove_profile_picture():
        """Remove the selected profile picture."""
        profile_pic_path.set("")

    root = tk.Tk()
    root.title("Edit Details")
    root.geometry("500x600")

    profile_pic_path = tk.StringVar(value=user[-1])  # Profile picture path from database

    fields = [
        ("First Name:", user[1]),
        ("Last Name:", user[2]),
        ("Contact No.:", user[3]),
        ("Email:", user[4]),
        ("Security Question:", user[5]),
        ("Security Answer:", user[6]),
        ("Password:", user[7]),
        ("Address:", user[8]),
    ]

    entries = []
    for idx, (label_text, default_value) in enumerate(fields):
        tk.Label(root, text=label_text, font=("Arial", 12)).grid(row=idx, column=0, padx=10, pady=5, sticky="w")
        entry = tk.Entry(root, font=("Arial", 12))
        entry.insert(0, default_value if default_value else "")
        if label_text == "Email:":  # Make the email field read-only
            entry.config(state="readonly")
        entry.grid(row=idx, column=1, padx=10, pady=5)
        entries.append(entry)

    first_name_entry, last_name_entry, contact_no_entry, email_entry, security_question_entry, security_answer_entry, password_entry, address_entry = entries

    # Security Question Dropdown (replaces the Entry field)
    tk.Label(root, text="Security Question:", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=5, sticky="w")
    security_question_entry = ttk.Combobox(root, values=["Select", "Your first pet's name?", "Your hometown?", "Your favorite color?"], font=("Arial", 12))
    security_question_entry.set(user[5])  # Auto fill current security question
    security_question_entry.grid(row=4, column=1, padx=10, pady=5)

    # Profile Picture Section
    tk.Label(root, text="Profile Picture:", font=("Arial", 12)).grid(row=8, column=0, padx=10, pady=5, sticky="w")
    tk.Entry(root, textvariable=profile_pic_path, font=("Arial", 12), state="readonly").grid(row=8, column=1, padx=10, pady=5)
    tk.Button(root, text="Browse", font=("Arial", 10), command=select_profile_picture).grid(row=9, column=0, pady=5)
    tk.Button(root, text="Remove", font=("Arial", 10), command=remove_profile_picture).grid(row=9, column=1, pady=5)

    # Save Changes Button
    tk.Button(root, text="Save Changes", font=("Arial", 12), bg="blue", fg="white", command=update_details).grid(row=10, columnspan=2, pady=10)

    # Back Button to Navigate to Customer Panel
    def back_to_customer_panel():
        """Navigate back to the Customer Panel."""
        root.destroy()  # Close the current window
        subprocess.run([sys.executable, 'Customer_Panel.py', user[4]])  # Pass the email as an argument

    tk.Button(root, text="Back", font=("Arial", 12), bg="grey", fg="white", command=back_to_customer_panel).grid(row=11, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    email = sys.argv[1]  # Get the email passed to the script
    authenticate_and_edit(email)  # Start the authentication window with the email passed
