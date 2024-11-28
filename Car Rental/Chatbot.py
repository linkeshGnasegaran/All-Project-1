import customtkinter as ctk

# Set appearance mode and color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Questions and answers
questions_and_answers = [
    ("how do i search for available cars for my desired rental dates?", "You can search by selecting your desired rental dates in the app's search field."),
    ("what documents do i need to upload or present to complete the booking process?", "You need to present your valid driving license and a form of identification."),
    ("are there any additional charges for late returns?", "Yes, late returns may incur additional charges as per the rental agreement."),
    ("what insurance coverage is provided with the rental, and can i add extra coverage?", "Basic insurance is provided, and you have the option to add extra coverage at an additional cost."),
    ("how do i know if my booking is confirmed?", "You will receive a confirmation email and notification in the app once your booking is confirmed."),
    ("what are the cancellation or refund policies if i need to cancel my booking?", "Cancellation policies vary, but most bookings allow free cancellation within 24 hours of booking."),
    ("can i select specific features or models of cars (e.g., suv, sedan) when booking?", "Yes, you can filter and select the type of car model during the search process."),
    ("what is the process for extending my rental period if needed?", "You can extend the rental period through the app or by contacting customer support."),
    ("how do i report a problem with the car during my rental period?", "Contact the rental company's support service using the emergency contact in the app."),
    ("what payment methods are accepted, and is there a deposit required?", "Most major credit/debit cards and online payments are accepted.")
]

# Function to display a message in the chatbox
def update_chat(message):
    chat_display.configure(state="normal")
    chat_display.insert("end", f"{message}\n")  # Corrected syntax
    chat_display.configure(state="disabled")
    chat_display.see("end")

# Function to handle user questions and respond
def ask_question():
    user_question = input_field.get().lower().strip()  # Corrected input handling
    if not user_question:
        return
    update_chat(f"You: {user_question}")
    answered = False
    # Check if the user's question matches any known question
    for question, answer in questions_and_answers:
        if user_question in question.lower():  # Made it case insensitive
            update_chat(f"Chatbot: {answer}")
            answered = True
            break  # Corrected the `Break` to `break`

    if not answered:
        update_chat("Chatbot: I'm sorry, I don't have an answer for that question. Please contact customer support for more details car@example.com or dial 04-2342342.")
    # Clear the input field
    input_field.delete(0, "end")  # Corrected delete method

# Create the main window
root = ctk.CTk()
root.title("Car Rental Booking FAQ Chatbot")
root.geometry("600x450")

# Create the chat display and input field
chat_display = ctk.CTkTextbox(root, height=280, width=550, state="disabled", wrap="word")
chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

input_field = ctk.CTkEntry(root, width=400)
input_field.grid(row=1, column=0, padx=10, pady=10)

send_button = ctk.CTkButton(root, text="Ask", width=120, command=ask_question)
send_button.grid(row=1, column=1, padx=10, pady=10)

# Initial message from the chatbot
update_chat("Chatbot: Welcome! Ask me any questions about our car rental booking process.\n")

# Start the main loop
root.mainloop()
