import tkinter as tk
from tkcalendar import DateEntry

root = tk.Tk()

# Use 'y-mm-dd' instead of '%Y-%m-%d'
cal = DateEntry(root, selectmode='day', date_pattern="yy-mm-dd")
cal.pack()

root.mainloop()
