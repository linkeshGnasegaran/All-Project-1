import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import subprocess

def initialize_db():
    connection = sqlite3.connect('car_rental.db')
    cursor = connection.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS Register (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            contact TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            security_q TEXT NOT NULL,
            security_a TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()

    # Initialize admin_password database
    connection = sqlite3.connect('admin_password.db')
    cursor = connection.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS admin_password (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()

def main():
    win = tk.Tk()
    app = Login_Window(win)
    win.mainloop()

class Login_Window:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("1550x800+0+0")

        # Background image
        self.bg = ImageTk.PhotoImage(file=r"C:\Users\Honor\PycharmProjects\ALL 1 Project\Car Rental\bg.jpg")
        lbl_bg = tk.Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        # Frame for login
        frame = tk.Frame(self.root, bg="black")
        frame.place(x=610, y=170, width=340, height=430)

        # Logo image
        img1 = Image.open(r"C:\Users\Honor\PycharmProjects\ALL 1 Project\Car Rental\loginlogo.png")
        img1 = img1.resize((90, 90), Image.BICUBIC)
        self.photoimage1 = ImageTk.PhotoImage(img1)
        lbl_img1 = tk.Label(frame, image=self.photoimage1, bg="black", borderwidth=0)
        lbl_img1.place(x=125, y=10, width=90, height=90)

        # Get Started text
        get_str = tk.Label(frame, text="Get Started", font=("times new roman", 20, "bold"), fg="white", bg="black")
        get_str.place(x=95, y=100)

        # Username label and entry
        username = tk.Label(frame, text="Username", font=("times new roman", 12, "bold"), fg="white", bg="black")
        username.place(x=70, y=150)

        self.txtuser = ttk.Entry(frame, font=("times new roman", 12, "bold"))
        self.txtuser.place(x=40, y=180, width=270)

        # Password label and entry
        password = tk.Label(frame, text="Password", font=("times new roman", 12, "bold"), fg="white", bg="black")
        password.place(x=70, y=230)

        self.txtpass = ttk.Entry(frame, font=("times new roman", 12, "bold"), show='*')
        self.txtpass.place(x=40, y=260, width=270)

        # Icon Images
        img2 = Image.open(r"C:\Users\Honor\PycharmProjects\ALL 1 Project\Car Rental\loginlogo.png")
        img2 = img2.resize((25, 25), Image.BICUBIC)
        self.photoimage2 = ImageTk.PhotoImage(img2)
        lbl_img1 = tk.Label(frame, image=self.photoimage2, bg="black", borderwidth=0)
        lbl_img1.place(x=30, y=150, width=25, height=25)

        img3 = Image.open(r"C:\Users\Honor\PycharmProjects\ALL 1 Project\Car Rental\lock.jpg")
        img3 = img3.resize((25, 25), Image.BICUBIC)
        self.photoimage3 = ImageTk.PhotoImage(img3)
        lbl_img1 = tk.Label(frame, image=self.photoimage3, bg="black", borderwidth=0)
        lbl_img1.place(x=30, y=230, width=25, height=25)

        # Login Button
        loginbtn = tk.Button(frame, command=self.login, text="Login", font=("times new roman", 12, "bold"), bd=3, relief="ridge", fg="white", bg="red", activeforeground="white", activebackground="red")
        loginbtn.place(x=110, y=300, width=120, height=35)

        # Register Button
        registerbtn = tk.Button(frame, text="New User Register", command=self.register, font=("times new roman", 10, "bold"), borderwidth=0, fg="white", bg="black", activeforeground="white", activebackground="black")
        registerbtn.place(x=15, y=350, width=160)

        # Admin Login Button
        admin_login_btn = tk.Button(frame, text="Admin Login", command=self.admin_login, font=("times new roman", 10, "bold"), borderwidth=0, fg="white", bg="black", activeforeground="white", activebackground="black")
        admin_login_btn.place(x=0, y=370, width=160)

        # Forget Password Button
        forgetbtn = tk.Button(frame, text="Forget Password", command=self.forget_password, font=("times new roman", 10, "bold"), borderwidth=0, fg="white", bg="black", activeforeground="white", activebackground="black")
        forgetbtn.place(x=10, y=390, width=160)

    def login(self):
        if self.txtuser.get() == "" or self.txtpass.get() == "":
            messagebox.showerror("Error", "All fields required to be filled")
        else:
            connection = sqlite3.connect('car_rental.db')
            my_cursor = connection.cursor()
            my_cursor.execute("SELECT * FROM Register WHERE email=? AND password=?", (
                self.txtuser.get(),
                self.txtpass.get()
            ))
            row = my_cursor.fetchone()
            if row is None:
                messagebox.showerror("Error", "Invalid Username & password")
            else:
                # Pass the email to the Customer_Panel.py script
                subprocess.Popen(["python", "customer_panel.py", self.txtuser.get()])
            connection.commit()
            connection.close()

    def register(self):
        subprocess.Popen(["python", "Register.py"])  # Opens Register.py as a new process

    def admin_login(self):
        # Open the Admin login window in a new process
        subprocess.Popen(["python", "Admin_Login.py"])

    def forget_password(self):
        subprocess.Popen(["python", "Forget_Password.py"])  # Opens Register.py as a new process


if __name__ == "__main__":
    initialize_db()
    main()
