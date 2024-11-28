import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from tkinter import Label, Button
import subprocess


def forget_password_window():
    def reset_password():
        # Validate user input
        if combo_securityQ.get() == "Select" or txt_security.get().strip() == "" or txt_newpass.get().strip() == "":
            messagebox.showerror("Error", "Please fill all fields to reset the password")
            return

        email = txtuser.get().strip()
        security_question = combo_securityQ.get().strip()
        security_answer = txt_security.get().strip().lower()
        new_password = txt_newpass.get().strip()

        try:
            # Open database connection
            connection = sqlite3.connect('car_rental.db')
            my_cursor = connection.cursor()

            # Fetch user details based on email
            query = "SELECT security_question, security_answer FROM Register WHERE email=?"
            my_cursor.execute(query, (email,))
            row = my_cursor.fetchone()

            if row is None:
                messagebox.showerror("Error", "Email address not found!")
                return

            # Check security question and answer
            db_security_question, db_security_answer = row
            if db_security_question.strip() != security_question or db_security_answer.strip().lower() != security_answer:
                messagebox.showerror("Error", "Incorrect security question or answer")
                return

            # Update the password
            update_query = "UPDATE Register SET password=? WHERE email=?"
            my_cursor.execute(update_query, (new_password, email))
            connection.commit()

            if my_cursor.rowcount > 0:
                messagebox.showinfo("Success", "Password reset successfully!")
                root.destroy()  # Close the forget password window
                subprocess.Popen(["python", "Login.py"])  # Open the Login.py script after reset
            else:
                messagebox.showerror("Error", "Password update failed. Try again.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            connection.close()

    def go_back():
        root.destroy()
        subprocess.Popen(["python", "Login.py"])  # Open the Login.py script when going back

    root = tk.Tk()
    root.title("Forget Password")
    root.geometry("340x500+610+170")

    # UI Elements
    label = Label(root, text="Forget Password", font=("times new roman", 12, "bold"), fg="red", bg="white")
    label.place(x=0, y=10, relwidth=1)

    email_label = Label(root, text="Enter Email", font=("times new roman", 15, "bold"), bg="white", fg="black")
    email_label.place(x=50, y=50)

    txtuser = ttk.Entry(root, font=("times new roman", 15, "bold"))
    txtuser.place(x=50, y=80, width=250)

    securityQ = Label(root, text="Select Security Question", font=("times new roman", 15, "bold"), bg="white",
                      fg="black")
    securityQ.place(x=50, y=130)

    combo_securityQ = ttk.Combobox(root, font=("times new roman", 15, "bold"), state="readonly")
    combo_securityQ["values"] = ("Select", "Your first pet's name?", "Your hometown?", "Your favorite color?")
    combo_securityQ.place(x=50, y=160, width=250)
    combo_securityQ.current(0)

    securityA = Label(root, text="Security Answer", font=("times new roman", 15, "bold"), bg="white", fg="black")
    securityA.place(x=50, y=210)

    txt_security = ttk.Entry(root, font=("times new roman", 15, "bold"))
    txt_security.place(x=50, y=240, width=250)

    new_password = Label(root, text="New Password", font=("times new roman", 15, "bold"), bg="white", fg="black")
    new_password.place(x=50, y=310)

    txt_newpass = ttk.Entry(root, font=("times new roman", 15, "bold"), show="*")
    txt_newpass.place(x=50, y=340, width=250)

    btn = Button(root, text="Reset Password", font=("times new roman", 15, "bold"), fg="white", bg="green",
                 command=reset_password)
    btn.place(x=100, y=380)

    # Back Button
    back_btn = Button(root, text="Back", font=("times new roman", 15, "bold"), fg="white", bg="blue",
                      command=go_back)
    back_btn.place(x=130, y=440)

    root.mainloop()


# Call the function to open the forget password window
forget_password_window()
