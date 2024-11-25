from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import subprocess


def initialize_database():
    # Initialize user database
    connection = sqlite3.connect('pr2.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Register (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        contact TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        security_q TEXT NOT NULL,
        security_a TEXT NOT NULL,
        password TEXT NOT NULL
    )''')
    connection.commit()
    connection.close()


def check_login(email, password, root):
    # Admin Login
    if email == "admin@example.com" and password == "admin123":
        messagebox.showinfo("Login", "Welcome Admin!")
        root.destroy()
        subprocess.Popen(["python", "Admin_Panel.py"])  # Replace with your admin dashboard script
        return

    # User Login
    connection = sqlite3.connect('pr2.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Register WHERE email=? AND password=?", (email, password))
    user = cursor.fetchone()
    connection.close()

    if user:
        messagebox.showinfo("Login", "Welcome User!")
        show_user_dashboard(root)
    else:
        messagebox.showerror("Error", "Invalid email or password.")


def show_user_dashboard(root):
    # Hide login frame and show dashboard frame
    login_frame.pack_forget()

    dashboard_frame = Frame(root)
    dashboard_frame.pack(fill="both", expand=True)

    Label(dashboard_frame, text="Welcome to the User Dashboard", font=("times new roman", 14)).pack(pady=20)

    # Function to go back to Login page
    def go_back_to_login():
        dashboard_frame.pack_forget()  # Hide dashboard frame
        show_login_page(root)  # Show login frame again

    # Back to Login button
    back_button = Button(dashboard_frame, text="Back to Login", command=go_back_to_login,
                         font=("times new roman", 12, "bold"), bg="blue", fg="white")
    back_button.pack(pady=20)


def show_login_page(root):
    # Create the login page frame
    global login_frame
    login_frame = Frame(root)
    login_frame.pack(fill="both", expand=True)

    Label(login_frame, text="Login", font=("times new roman", 20, "bold")).pack(pady=10)

    # Username and Password fields
    Label(login_frame, text="Email", font=("times new roman", 12, "bold")).pack(pady=5)
    email_entry = ttk.Entry(login_frame, font=("times new roman", 12))
    email_entry.pack(pady=5)

    Label(login_frame, text="Password", font=("times new roman", 12, "bold")).pack(pady=5)
    password_entry = ttk.Entry(login_frame, font=("times new roman", 12), show="*")
    password_entry.pack(pady=5)

    # Login button
    login_button = Button(login_frame, text="Login",
                          command=lambda: check_login(email_entry.get(), password_entry.get(), root),
                          font=("times new roman", 12))
    login_button.pack(pady=10)


def main():
    initialize_database()
    root = Tk()
    root.title("Login")
    root.geometry("400x300")

    show_login_page(root)  # Start with the login page

    root.mainloop()


if __name__ == "__main__":
    main()
