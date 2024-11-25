from tkinter import Tk, Button, Label
import subprocess

def manage_cars():
    window.destroy()
    subprocess.Popen(["python", "manage_cars.py"])


def manage_booking():
    window.destroy()
    subprocess.Popen(["python", "manage_booking.py"])

window = Tk()
window.geometry("900x600")
window.title("Admin Panel")

Label(window, text="Admin Dashboard", font=("Times New Roman", 18, "bold")).pack(pady=20)

btn_manage_cars = Button(window, text="Manage Cars", font=("Arial", 14), width=20, bg="green", fg="black",
                          command=manage_cars)
btn_manage_cars.pack(pady=10)

btn_manage_booking = Button(window, text="Manage Booking", font=("Arial", 14), width=20, bg="lightcoral", fg="black",
                          command=manage_booking)
btn_manage_booking.pack(pady=10)



window.mainloop()



