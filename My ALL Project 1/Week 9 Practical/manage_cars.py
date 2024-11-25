from tkinter import Tk, Canvas, Entry, Button, StringVar, filedialog, OptionMenu, Label, ttk, messagebox
from PIL import Image, ImageTk
import sqlite3

selected_car_id = None
image_path = None  # To store the uploaded image path

# Connect to the database and create the table
def connect_db():
    conn = sqlite3.connect('car_details.db')
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_number TEXT UNIQUE,  -- Ensure uniqueness
            make_and_model TEXT,
            seating_capacity TEXT,
            daily_rate REAL,
            fuel_type TEXT,
            manufacturer_year TEXT,
            transmission_type TEXT,
            car_type TEXT,
            mileage TEXT,
            color TEXT,
            image_path TEXT
        )
    ''')
    conn.commit()
    return conn

# Function to save data to the database
def save_data():
    registration_number = entry_registration.get()
    make_and_model = make_and_model_var.get()
    seating_capacity = entry_seating.get()
    daily_rate = entry_rate.get()
    fuel_type = fuel_type_var.get()
    manufacturer_year = entry_year.get()
    transmission_type = transmission_var.get()
    car_type = car_type_var.get()
    mileage = entry_mileage.get()
    color = entry_color.get()

    if not registration_number:
        messagebox.showwarning("Warning", "Registration number cannot be empty.")
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM cars WHERE registration_number = ?', (registration_number,))
    if cursor.fetchone() is not None:
        messagebox.showwarning("Warning", "Registration number must be unique.")
        conn.close()
        return

    cursor.execute(''' 
        INSERT INTO cars (registration_number, make_and_model, seating_capacity, daily_rate, fuel_type,
                          manufacturer_year, transmission_type, car_type, mileage, color, image_path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (registration_number, make_and_model, seating_capacity, daily_rate, fuel_type, manufacturer_year,
          transmission_type, car_type, mileage, color, image_path))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Data saved successfully!")
    refresh_treeview()
def refresh_treeview():
    for row in treeview.get_children():
        treeview.delete(row)

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, registration_number, make_and_model, seating_capacity, daily_rate, fuel_type, manufacturer_year, transmission_type, car_type, mileage, color FROM cars')
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        treeview.insert("", "end", values=row)


# Function to upload an image
def browse_image():
    global image_path
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if image_path:
        upload_image()

# Function to upload and display the image
def upload_image():
    img = Image.open(image_path)
    img = img.resize((150, 150), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    image_display.config(image=img)
    image_display.image = img

# Function to delete a car from the database
def delete_data():
    global selected_car_id
    if selected_car_id is not None:
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this car?")
        if confirm:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM cars WHERE id = ?', (selected_car_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Car deleted successfully!")
            refresh_treeview()
            clear_selection()
    else:
        messagebox.showwarning("Warning", "Please select a car to delete.")

# Function to update a car's details
def update_data():
    global selected_car_id
    if selected_car_id is not None:
        registration_number = entry_registration.get()
        make_and_model = make_and_model_var.get()
        seating_capacity = entry_seating.get()
        daily_rate = entry_rate.get()
        fuel_type = fuel_type_var.get()
        manufacturer_year = entry_year.get()
        transmission_type = transmission_var.get()
        car_type = car_type_var.get()
        mileage = entry_mileage.get()
        color = entry_color.get()

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(''' 
            UPDATE cars 
            SET registration_number = ?, make_and_model = ?, seating_capacity = ?, daily_rate = ?, fuel_type = ?, 
                manufacturer_year = ?, transmission_type = ?, car_type = ?, mileage = ?, color = ?, image_path = ?
            WHERE id = ?
        ''', (registration_number, make_and_model, seating_capacity, daily_rate, fuel_type, manufacturer_year,
              transmission_type, car_type, mileage, color, image_path, selected_car_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Car updated successfully!")
        refresh_treeview()
        clear_selection()
    else:
        messagebox.showwarning("Warning", "Please select a car to update.")

def select_item(event):
    global selected_car_id, image_path
    selected_item = treeview.selection()
    if selected_item:
        item = treeview.item(selected_item)
        values = item['values']
        selected_car_id = values[0]

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cars WHERE id = ?', (selected_car_id,))
        car_data = cursor.fetchone()
        conn.close()

        if car_data:
            entry_registration.delete(0, 'end')
            entry_registration.insert(0, car_data[1])
            make_and_model_var.set(car_data[2])
            entry_seating.set(car_data[3])
            entry_rate.delete(0, 'end')
            entry_rate.insert(0, car_data[4])
            fuel_type_var.set(car_data[5])
            entry_year.delete(0, 'end')
            entry_year.insert(0, car_data[6])
            transmission_var.set(car_data[7])
            car_type_var.set(car_data[8])
            entry_mileage.delete(0, 'end')
            entry_mileage.insert(0, car_data[9])
            entry_color.delete(0, 'end')
            entry_color.insert(0, car_data[10])

            image_path = car_data[11]
            if image_path:
                upload_image()

def clear_selection():
    global selected_car_id
    selected_car_id = None
    entry_registration.delete(0, 'end')
    make_and_model_var.set("Select")
    entry_seating.set("Select")
    entry_rate.delete(0, 'end')
    fuel_type_var.set("Select")
    entry_year.delete(0, 'end')
    transmission_var.set("Select")
    car_type_var.set("Select")
    entry_mileage.delete(0, 'end')
    entry_color.delete(0, 'end')
    image_display.config(image="")

# Setting up the main window
window = Tk()
window.geometry("1300x750")
window.configure(bg="light green")

# Canvas for layout
canvas = Canvas(
    window,
    bg="light green",
    height=600,
    width=800,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# Title
canvas.create_text(400, 28, anchor="center", text="MANAGE CAR DETAILS", fill="#000000",
                   font=("Times New Roman ExtraBold", 18))

# Input fields (including new fields)
canvas.create_text(37.0, 98.0, anchor="nw", text="Registration Number:", fill="#000000", font=("Inter Bold", 14 * -1))
entry_registration = Entry(bd=2, bg="#D9D9D9", fg="#000716", highlightthickness=0)
entry_registration.place(x=193.0, y=96.0, width=180.0, height=22.0)

canvas.create_text(37.0, 138.0, anchor="nw", text="Make & Model:", fill="#000000", font=("Inter Bold", 14 * -1))
make_and_model_var = StringVar(window)
make_and_model_var.set("Select")
make_and_model_options = ["Toyota Camry", "Honda Civic", "BMW 3 Series", "Ford Focus", "Audi A4"]
make_and_model_dropdown = OptionMenu(window, make_and_model_var, *make_and_model_options)
make_and_model_dropdown.place(x=193.0, y=136.0, width=180.0)

canvas.create_text(37.0, 178.0, anchor="nw", text="Seating Capacity:", fill="#000000", font=("Inter Bold", 14 * -1))
entry_seating = StringVar(window)
entry_seating.set("Select")
seating_options = ["2", "4", "5", "7", "8"]
seating_dropdown = OptionMenu(window, entry_seating, *seating_options)
seating_dropdown.place(x=193.0, y=176.0, width=180.0)

canvas.create_text(37.0, 218.0, anchor="nw", text="Daily Rate (RM):", fill="#000000", font=("Inter Bold", 14 * -1))
entry_rate = Entry(bd=2, bg="#D9D9D9", fg="#000716", highlightthickness=0)
entry_rate.place(x=193.0, y=216.0, width=180.0, height=22.0)

canvas.create_text(37.0, 258.0, anchor="nw", text="Fuel Type:", fill="#000000", font=("Inter Bold", 14 * -1))
fuel_type_var = StringVar(window)
fuel_type_var.set("Select")
fuel_type_options = ["Petrol", "Diesel", "Electric", "Hybrid"]
fuel_type_dropdown = OptionMenu(window, fuel_type_var, *fuel_type_options)
fuel_type_dropdown.place(x=193.0, y=256.0, width=180.0)

canvas.create_text(37.0, 298.0, anchor="nw", text="Manufacturer Year:", fill="#000000", font=("Inter Bold", 14 * -1))
entry_year = Entry(bd=2, bg="#D9D9D9", fg="#000716", highlightthickness=0)
entry_year.place(x=193.0, y=296.0, width=180.0, height=22.0)

canvas.create_text(37.0, 338.0, anchor="nw", text="Transmission Type:", fill="#000000", font=("Inter Bold", 14 * -1))
transmission_var = StringVar(window)
transmission_var.set("Select")
transmission_options = ["Automatic", "Manual"]
transmission_dropdown = OptionMenu(window, transmission_var, *transmission_options)
transmission_dropdown.place(x=193.0, y=336.0, width=180.0)

canvas.create_text(37.0, 378.0, anchor="nw", text="Car Type:", fill="#000000", font=("Inter Bold", 14 * -1))
car_type_var = StringVar(window)
car_type_var.set("Select")
car_type_options = ["Sedan", "SUV", "Hatchback", "Truck"]
car_type_dropdown = OptionMenu(window, car_type_var, *car_type_options)
car_type_dropdown.place(x=193.0, y=376.0, width=180.0)

canvas.create_text(37.0, 418.0, anchor="nw", text="Mileage (km):", fill="#000000", font=("Inter Bold", 14 * -1))
entry_mileage = Entry(bd=2, bg="#D9D9D9", fg="#000716", highlightthickness=0)
entry_mileage.place(x=193.0, y=416.0, width=180.0, height=22.0)

canvas.create_text(37.0, 458.0, anchor="nw", text="Color:", fill="#000000", font=("Inter Bold", 14 * -1))
entry_color = Entry(bd=2, bg="#D9D9D9", fg="#000716", highlightthickness=0)
entry_color.place(x=193.0, y=456.0, width=180.0, height=22.0)

# Browse image button
button_browse = Button(
    text="Browse Image",
    command=browse_image,
    bg="#64C4ED",  # Light blue background
    fg="black"
)
button_browse.place(x=193.0, y=496.0, width=100.0, height=30.0)

# Image display area
image_display = Label(window)
image_display.place(x=450, y=130, width=150, height=150)

# Treeview configuration (add more fields if needed in columns)
treeview = ttk.Treeview(window, columns=("ID", "Registration Number", "Make & Model", "Seating Capacity", "Daily Rate", "Fuel Type", "Manufacturer Year", "Transmission Type", "Car Type", "Mileage Km", "Color"), show="headings")
treeview.heading("ID", text="ID")
treeview.heading("Registration Number", text="Reg. No.")
treeview.heading("Make & Model", text="Make & Model")
treeview.heading("Seating Capacity", text="Seats")
treeview.heading("Daily Rate", text="Rate (RM)")
treeview.heading("Fuel Type", text="Fuel Type")
treeview.heading("Transmission Type", text="Transmission Type")
treeview.heading("Manufacturer Year", text="Manufacturer Year")
treeview.heading("Car Type", text="Car Type")
treeview.heading("Mileage Km", text="Mileage Km")
treeview.heading("Color", text="Color")



treeview.column("ID", width=50, anchor="center")
treeview.column("Registration Number", width=100, anchor="center")
treeview.column("Make & Model", width=100, anchor="center")
treeview.column("Seating Capacity", width=100, anchor="center")
treeview.column("Daily Rate", width=100, anchor="center")
treeview.column("Fuel Type", width=100, anchor="center")
treeview.column("Manufacturer Year", width=100, anchor="center")
treeview.column("Transmission Type", width=100, anchor="center")
treeview.column("Car Type", width=100, anchor="center")
treeview.column("Mileage Km", width=100, anchor="center")
treeview.column("Color", width=100, anchor="center")

treeview.place(x=50, y=550, width=1200, height=150)
treeview.bind("<<TreeviewSelect>>", select_item)

# Buttons for saving, updating, deleting, and clearing (below the image)
button_save = Button(
    text="Save",
    command=save_data,
    bg="green",  # Light blue background
    fg="#FFFFFF"
)
button_save.place(x=485, y=300, width=80, height=30)

button_update = Button(
    text="Update",
    command=update_data,
    bg="#FFA500",  # Orange background for update
    fg="#FFFFFF"
)
button_update.place(x=485, y=350, width=80, height=30)

button_delete = Button(
    text="Delete",
    command=delete_data,
    bg="#D9534F",  # Red background for delete
    fg="#FFFFFF"
)
button_delete.place(x=485, y=400, width=80, height=30)

button_clear = Button(
    text="Clear",
    command=clear_selection,
    bg="#DCDCDC",  # Light gray background for clear
    fg="#000000"
)
button_clear.place(x=485, y=450, width=80, height=30)

refresh_treeview()
window.mainloop()
