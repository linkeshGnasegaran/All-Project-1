import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk

def create_table():
    """Creates or recreates the Register table with the correct schema."""
    with sqlite3.connect('car_rental.db') as connection:
        cursor = connection.cursor()
        # Drop the table if it exists
        cursor.execute("DROP TABLE IF EXISTS Register")
        # Create the table with the correct schema
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Register (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  
                first_name TEXT,
                last_name TEXT,
                contact_no TEXT,
                email TEXT UNIQUE,  
                security_question TEXT,
                security_answer TEXT,
                password TEXT,
                address TEXT,
                profile_picture TEXT
            )
        ''')
        connection.commit()
        cursor.close()

def create_window():
    """Creates the registration window."""
    create_table()  # Ensure the table is created with the correct schema

    root = tk.Tk()
    root.title("Register")
    root.resizable(True, True)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")

    # Background image setup
    try:
        image_path = "C:/Users/Honor/PycharmProjects/ALL 1 Project/Car Rental/bg.jpg"
        image = Image.open(image_path)
        background_image = ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"Error loading image: {e}")
        background_image = None

    if background_image:
        background_label = tk.Label(root, image=background_image)
        background_label.place(relwidth=1, relheight=1)

    frame_width = 450
    frame_height = 350
    frame = tk.Frame(root, bg="white", padx=30, pady=30, width=frame_width, height=frame_height)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    title_label = tk.Label(frame, text="REGISTER HERE", font=("Arial", 18, "bold"), fg="black", bg="white")
    title_label.grid(row=0, columnspan=2, pady=20)

    # Form fields
    fields = [
        ("First Name", 1, 0), ("Last Name", 1, 1),
        ("Contact No.", 2, 0), ("Email", 2, 1),
        ("Select Security Question", 3, 0), ("Security Answer", 3, 1),
        ("Password", 4, 0), ("Confirm Password", 4, 1)
    ]

    entries = {}
    for label_text, row, col in fields:
        label = tk.Label(frame, text=label_text, font=("Arial", 12), bg="white")
        label.grid(row=row, column=col * 2, padx=10, pady=10, sticky="w")

        if "Security Question" in label_text:
            entry = ttk.Combobox(frame, font=("Arial", 12))
            entry["values"] = ["Select", "Your first pet's name?", "Your hometown?", "Your favorite color?"]
        elif "Password" in label_text:
            entry = tk.Entry(frame, show="*")
        else:
            entry = tk.Entry(frame, font=("Arial", 12))

        entry.grid(row=row, column=col * 2 + 1, padx=10, pady=10)
        entries[label_text] = entry

    # Register user function
    def register_user():
        """Registers a new user to the database."""
        form_data = {field: entries[field].get() for field, row, col in fields}

        if any(value == "" for value in form_data.values()):
            messagebox.showerror("Error", "All fields are required")
            return

        if form_data["Password"] != form_data["Confirm Password"]:
            messagebox.showerror("Error", "Passwords do not match")
            return

        try:
            # Establish connection and insert data
            with sqlite3.connect('car_rental.db') as connection:
                cursor = connection.cursor()
                cursor.execute('''
                    INSERT INTO Register (first_name, last_name, contact_no, email, security_question, security_answer, password)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (form_data["First Name"], form_data["Last Name"], form_data["Contact No."],
                      form_data["Email"], form_data["Select Security Question"], form_data["Security Answer"], form_data["Password"]))
                connection.commit()
                cursor.close()
            messagebox.showinfo("Success", "Registration Successful")
            root.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Email already exists")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Register button
    register_btn = tk.Button(frame, text="Register", font=("Arial", 14), bg="green", fg="white", command=register_user)
    register_btn.grid(row=5, columnspan=2, pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_window()
