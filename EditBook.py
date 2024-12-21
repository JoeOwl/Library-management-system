import customtkinter  # CustomTkinter library for modern GUI components
import tkinter  # Tkinter library for basic GUI components
from database import LMS  # Custom library for database operations related to the library
from tkinter.messagebox import showerror, showwarning, showinfo  # Messagebox for dialog messages
from tkcalendar import DateEntry  # Calendar widget for date selection
import os  # Library for file and directory management
import sys  # Library for accessing system-specific paths

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

# "EditBook" class to create a GUI window for editing book details
class EditBook(customtkinter.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)  # Initialize the parent class
        self.title("Library Management System")  # Set the window title
        self.minsize(500, 490)  # Set the minimum window size
        self.maxsize(500, 490)  # Set the maximum window size
        self.geometry('500x490')  # Set the default window size

        # Create a heading frame for the title
        heading_frame = customtkinter.CTkFrame(master=self, corner_radius=10)
        heading_frame.pack(padx=10, pady=10, ipadx=20, ipady=5, fill="x", anchor="n")

        # Add a label for the heading
        label = customtkinter.CTkLabel(
            master=heading_frame,
            text="Edit Book",
            font=customtkinter.CTkFont(family="Robot", size=25, weight="bold"),
        )
        label.pack(ipady=10)

        # Frame for book search inputs and button
        first_frame = customtkinter.CTkFrame(master=self, corner_radius=10)
        first_frame.pack(padx=10, pady=10, ipadx=5, ipady=5, fill="both", expand=True)

        # Label for "Book ID"
        book_id_lbel1 = customtkinter.CTkLabel(
            master=first_frame,
            text="Book ID",
            font=customtkinter.CTkFont(family="Verdana", size=16, weight="bold"),
        )
        book_id_lbel1.grid(column=1, row=0, padx=10, pady=10)

        # Entry widget to input the Book ID
        self.book_id_input1 = customtkinter.CTkEntry(master=first_frame, width=200)
        self.book_id_input1.grid(column=2, row=0, padx=5, pady=10)

        # Button to search for book details
        search_book_det_btn = customtkinter.CTkButton(
            master=first_frame,
            text="Search",
            font=customtkinter.CTkFont(family="Verdana", size=16, weight="bold"),
            command=self.search_book_detail,  # Binds to the search_book_detail method
        )
        search_book_det_btn.grid(column=3, row=0, padx=5, pady=10)

        # Frame to display and edit book details (initially hidden)
        self.main_frame = customtkinter.CTkFrame(master=self, corner_radius=10)
        self.main_frame.pack_forget()

        # Configure columns for layout alignment
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.columnconfigure(2, weight=1)

        # Labels and inputs for book details
        # Book ID (disabled as it should not be edited)
        book_id_lbel = customtkinter.CTkLabel(master=self.main_frame, text="Book ID")
        book_id_lbel.grid(column=1, row=0, padx=5, pady=5)
        self.id_var = customtkinter.StringVar(self)
        self.book_id_input = customtkinter.CTkEntry(
            master=self.main_frame, width=200, textvariable=self.id_var, state='disabled'
        )
        self.book_id_input.grid(column=2, row=0, padx=5, pady=5)

        # Book Name
        book_nme_lbel = customtkinter.CTkLabel(master=self.main_frame, text="Book Name")
        book_nme_lbel.grid(column=1, row=1, padx=5, pady=5)
        self.name_var = customtkinter.StringVar(self)
        self.book_nme_input = customtkinter.CTkEntry(
            master=self.main_frame, width=200, textvariable=self.name_var
        )
        self.book_nme_input.grid(column=2, row=1, padx=5, pady=5)

        # Book Author
        book_author_lbel = customtkinter.CTkLabel(master=self.main_frame, text="Book Author")
        book_author_lbel.grid(column=1, row=2, padx=5, pady=5)
        self.author_var = customtkinter.StringVar(self)
        self.book_author_input = customtkinter.CTkEntry(
            master=self.main_frame, width=200, textvariable=self.author_var
        )
        self.book_author_input.grid(column=2, row=2, padx=5, pady=5)

        # Book Edition
        book_edition_lbel = customtkinter.CTkLabel(master=self.main_frame, text="Book Edition")
        book_edition_lbel.grid(column=1, row=3, padx=5, pady=5)
        self.edition_var = customtkinter.StringVar(self)
        self.book_edition_input = customtkinter.CTkEntry(
            master=self.main_frame, width=200, textvariable=self.edition_var
        )
        self.book_edition_input.grid(column=2, row=3, padx=5, pady=5)

        # Book Price
        book_price_lbel = customtkinter.CTkLabel(master=self.main_frame, text="Book Price")
        book_price_lbel.grid(column=1, row=4, padx=5, pady=5)
        self.price_var = customtkinter.StringVar(self)
        self.book_price_input = customtkinter.CTkEntry(
            master=self.main_frame, width=200, textvariable=self.price_var
        )
        self.book_price_input.grid(column=2, row=4, padx=5, pady=5)

        # Purchase Date
        purchase_dt_lbel = customtkinter.CTkLabel(master=self.main_frame, text="Purchased Date")
        purchase_dt_lbel.grid(column=1, row=5, padx=5, pady=5)
        self.purchase_dt_var = customtkinter.StringVar(self)
        self.purchase_dt = DateEntry(
            self.main_frame, width=10, borderwidth=2, textvariable=self.purchase_dt_var
        )
        self.purchase_dt.grid(column=2, row=5, padx=5, pady=5)

        # Update button to save changes
        update_new_book_btn = customtkinter.CTkButton(
            master=self.main_frame,
            text="Update",
            font=customtkinter.CTkFont(family="Verdana", size=16, weight="bold"),
            command=self.update_book,  # Binds to the update_book method
        )
        update_new_book_btn.grid(column=2, row=6, padx=10, pady=5, ipadx=10, ipady=10)

    # Method to search for a book by ID and display its details
    def search_book_detail(self):
        book_id = int(self.book_id_input1.get())  # Get Book ID from input
        book_details = db.select_book_detail(book_id)  # Fetch details from the database
        if book_details:  # Check if details are found
            # Populate fields with book details
            self.id_var.set(book_details[0])
            self.name_var.set(book_details[1])
            self.author_var.set(book_details[2])
            self.edition_var.set(book_details[3])
            self.price_var.set(book_details[4])
            self.purchase_dt_var.set(book_details[5])
            # Show the main frame for editing
            self.main_frame.pack(padx=10, pady=10, ipadx=5, ipady=5, fill="both", expand=True)
        else:
            showerror(title="Not Found", message="Book Not Found")  # Show error if not found

    # Method to update book details
    def update_book(self):
        # Get updated details from input fields
        book_id = self.id_var.get()
        book_nme = self.name_var.get()
        book_author = self.author_var.get()
        book_edition = self.edition_var.get()
        book_price = self.price_var.get()
        purchase_dt = self.purchase_dt_var.get()

        # Validate that all fields are filled
        if all([book_id, book_nme, book_author, book_edition, book_price, purchase_dt]):
            data = (book_id, book_nme, book_author, book_edition, book_price, purchase_dt, book_id)
            res = db.update_book_details(data)  # Update details in the database
            if res:  # Check if the update was successful
                showinfo(title="Saved", message="Book updated successfully.")
            else:
                showerror(title="Not Saved", message="Something went wrong. Please try again...")
        else:
            showerror(title="Empty Fields", message="Please fill all the details then submit!")  # Show error for empty fields
