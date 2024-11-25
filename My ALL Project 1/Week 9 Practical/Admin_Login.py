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


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x300")

        Label(self.root, text="Login", font=("times new roman", 20, "bold")).pack(pady=10)

        # Username and Password fields
        Label(self.root, text="Email", font=("times new roman", 12, "bold")).pack(pady=5)
        self.email_entry = ttk.Entry(self.root, font=("times new roman", 12))
        self.email_entry.pack(pady=5)

        Label(self.root, text="Password", font=("times new roman", 12, "bold")).pack(pady=5)
        self.password_entry = ttk.Entry(self.root, font=("times new roman", 12), show="*")
        self.password_entry.pack(pady=5)

        # Login button
        Button(self.root, text="Login", command=self.check_login, font=("times new roman", 12)).pack(pady=10)

    def check_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Admin Login
        if email == "admin@example.com" and password == "admin123":
            messagebox.showinfo("Login", "Welcome Admin!")
            self.root.destroy()
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
            self.root.destroy()
            self.open_user_dashboard()
        else:
            messagebox.showerror("Error", "Invalid email or password.")

    def open_user_dashboard(self):
        # Placeholder function for opening the user dashboard
        user_dashboard = Toplevel(self.root)
        user_dashboard.title("User Dashboard")
        user_dashboard.geometry("300x200")
        Label(user_dashboard, text="Welcome to the User Dashboard", font=("times new roman", 14)).pack(pady=20)


def main():
    initialize_database()
    win = Tk()
    app = LoginWindow(win)
    win.mainloop()


if __name__ == "__main__":
    main()
