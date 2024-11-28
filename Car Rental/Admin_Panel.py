from tkinter import Tk, Button, Label, Frame
from PIL import Image, ImageTk
import subprocess


def print_details():
    window.destroy()
    subprocess.Popen(["python", "Print_Details.py"])


def manage_cars():
    window.destroy()
    subprocess.Popen(["python", "Manage_Car.py"])


def manage_booking():
    window.destroy()
    subprocess.Popen(["python", "manage_booking.py"])


# Initialize the main window
window = Tk()
window.geometry("900x600")
window.title("Admin Panel")

# Load and set the background image
image_path = r"C:\Users\Honor\PycharmProjects\ALL 1 Project\Car Rental\bg.jpg"
background_image = Image.open(image_path)
background_photo = ImageTk.PhotoImage(background_image)

# Create a label for the background and place it
background_label = Label(window, image=background_photo)
background_label.place(relwidth=1, relheight=1)

# Top frame for the Admin Dashboard label
top_frame = Frame(window)
top_frame.pack(side="top", fill="x", pady=20)

# Place a background image for the "Admin Dashboard" label
dashboard_label_bg = Label(top_frame, image=background_photo)
dashboard_label_bg.place(relwidth=1, relheight=1)

# Admin Dashboard label styled with a background overlay
Label(
    top_frame,
    text="Admin Dashboard",
    font=("Times New Roman", 18, "bold"),
    fg="black",  # Text color
    bg="white",  # Background color for better visibility
    padx=10,
    pady=5,
).pack()

# Center frame for the buttons
center_frame = Frame(window)
center_frame.pack(expand=True)

# Set the background of the center frame to the image
background_frame_label = Label(center_frame, image=background_photo)
background_frame_label.place(relwidth=1, relheight=1)

# Buttons with background
btn_manage_cars = Button(
    center_frame,
    text="Manage Cars",
    font=("Arial", 14),
    width=20,
    bg="green",
    fg="black",
    command=manage_cars,
)
btn_manage_cars.pack(pady=10)

btn_manage_booking = Button(
    center_frame,
    text="Manage Booking",
    font=("Arial", 14),
    width=20,
    bg="lightcoral",
    fg="black",
    command=manage_booking,
)
btn_manage_booking.pack(pady=10)

btn_print_details = Button(
    center_frame,
    text="Print Details",
    font=("Arial", 14),
    width=20,
    bg="orange",
    fg="black",
    command=print_details,
)
btn_print_details.pack(pady=10)

# Run the Tkinter main loop
window.mainloop()
