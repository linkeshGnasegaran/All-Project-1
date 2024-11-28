import sqlite3

def connect_db(db_name):
    """Connect to a database and return the connection."""
    return sqlite3.connect(db_name)

def get_customer_details(email):
    """Fetch customer details using their email."""
    conn = connect_db('car_rental.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, email, phone FROM customers WHERE email = ?", (email,))
    details = cursor.fetchone()
    conn.close()
    return details

def update_customer_details(email, name, phone):
    """Update customer's profile details."""
    conn = connect_db('car_rental.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE customers SET name = ?, phone = ? WHERE email = ?", (name, phone, email))
    conn.commit()
    conn.close()

def get_booking_history(customer_name):
    """Retrieve the booking history of a customer."""
    conn = connect_db('car_booking.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings WHERE customer_name = ?", (customer_name,))
    bookings = cursor.fetchall()
    conn.close()
    return bookings
