import customtkinter  # CustomTkinter library for modern-looking GUI elements
import tkinter  # Standard Tkinter library for basic GUI components
from database import LMS  # Custom database class for managing library operations
from tkinter.messagebox import showerror, showinfo  # Dialog boxes for error and success messages
import os  # Library for file and directory management
import sys  # Library for accessing system-specific parameters and paths

def get_executable_directory():
    # Get the directory of the executable (or script during development)
    if getattr(sys, 'frozen', False):  # Check if the program is frozen (packaged as .exe)
        return os.path.dirname(sys.executable)  # Path to the .exe
    else:
        return os.path.dirname(os.path.abspath(__file__))  # Path to the script during development

# Get the directory where the .exe is located
executable_directory = get_executable_directory()
# Initialize the database with the path to the SQLite file
db = LMS(os.path.join(executable_directory, "lms.db"))

# Define a GUI class for the "Delete Book" feature
class DeleteBook(customtkinter.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)  # Initialize the parent class
        self.title("Library Management System")  # Set the window title
        self.minsize(400, 250)  # Set minimum window size
        self.maxsize(400, 250)  # Set maximum window size
        self.geometry('400x250')  # Set default window size
        
        # Create a frame for the heading section
        heading_frame = customtkinter.CTkFrame(master=self, corner_radius=10)
        heading_frame.pack(padx=10, pady=10, ipadx=20, ipady=5, fill="x", anchor="n")

        # Add a label for the heading text
        label = customtkinter.CTkLabel(
            master=heading_frame,
            text="Delete Book",
            font=customtkinter.CTkFont(family="Robot", size=25, weight="bold"),
        )
        label.pack(ipady=10)

        # Create a frame for the main content (inputs and button)
        main_frame = customtkinter.CTkFrame(master=self, corner_radius=10)
        main_frame.pack(padx=10, pady=10, ipadx=5, ipady=5, fill="both", expand=True)

        # Add a label for the "Book ID" input
        book_id_lbel = customtkinter.CTkLabel(
            master=main_frame,
            text="Book ID",
            font=customtkinter.CTkFont(family="Verdana", size=18),
        )
        book_id_lbel.pack()

        # Add an entry widget for the user to input the book ID
        self.book_id_input = customtkinter.CTkEntry(master=main_frame, width=200)
        self.book_id_input.pack(padx=5, pady=10)

        # Add a button to trigger the delete operation
        delete_book_btn = customtkinter.CTkButton(
            master=main_frame,
            text="Delete Book",
            command=self.delete_book,  # Bind the button to the delete_book method
        )
        delete_book_btn.pack(padx=10, pady=10)

    # Method to delete a book from the database
    def delete_book(self):
        # Fetch all existing book IDs from the database
        id_lists = db.all_book_id()
        # Convert the fetched tuples into a list of IDs
        new_id_lists = [t[0] for t in id_lists]
        
        # Check if the entered Book ID exists in the database
        try:
            entered_id = int(self.book_id_input.get())  # Get the input and convert to integer
        except ValueError:
            showerror(title="Error", message="Invalid Book ID. Please enter a numeric ID.")
            return

        if entered_id in new_id_lists:
            # Attempt to delete the book from the database
            res = db.delete_book(self.book_id_input.get())
            if res == 'deleted':
                # Show success message if deletion is successful
                showinfo(
                    title="Deleted",
                    message=f"Book ID: {self.book_id_input.get()} deleted successfully.",
                )
                self.book_id_input.delete(0, 'end')  # Clear the input field
            else:
                # Show error message if deletion fails
                showerror(
                    title="Error",
                    message=f"Book ID: {self.book_id_input.get()} not deleted. Try again!",
                )
        else:
            # Show error message if the entered Book ID is not found
            showerror(title="Not Found", message="Book not found.")
