from tkinter import Tk, Button, Label
import subprocess

def book_a_car():
    window.destroy()
    subprocess.Popen(["python", "book_cars.py"])

def view_booking_details():
    window.destroy()
    subprocess.Popen(["python", "booking_details.py"])

def print_booking_details():
    window.destroy()
    subprocess.Popen(["python", "print_details.py"])

window = Tk()
window.geometry("900x600")
window.title("Customer Panel")

Label(window, text="Customer Dashboard", font=("Times New Roman", 18, "bold")).pack(pady=20)

btn_book_car = Button(window, text="Book a Car", font=("Arial", 14), width=20, bg="lightgreen", fg="black",
                      command=book_a_car)
btn_book_car.pack(pady=10)

btn_view_booking = Button(window, text="View Booking Details", font=("Arial", 14), width=20, bg="lightcoral", fg="black",
                          command=view_booking_details)
btn_view_booking.pack(pady=10)

btn_view_booking = Button(window, text="Print Booking Details", font=("Arial", 14), width=20, bg="lightcoral", fg="black",
                          command=print_booking_details)
btn_view_booking.pack(pady=10)

window.mainloop()


