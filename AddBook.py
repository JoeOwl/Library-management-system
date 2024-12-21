import customtkinter
import tkinter
from database import LMS
from tkinter.messagebox import showerror, showwarning, showinfo
from tkcalendar import DateEntry
import datetime
import os
import sys

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

# "AddBook" GUI window class
class AddBook(customtkinter.CTkToplevel):
    def __init__(self, master=None):
        # Initialize the parent CTkToplevel
        super().__init__(master)
        
        # Set window properties
        self.title("Library Management System")
        self.minsize(500, 400)
        self.maxsize(500, 400)
        self.geometry('500x400')

        # Get the current year for use in the date picker
        dt = datetime.datetime.now()
        dt_year = dt.year
        
        # Create a frame for the heading section
        heading_frame = customtkinter.CTkFrame(master=self, corner_radius=10)
        heading_frame.pack(padx=10, pady=10, ipadx=20, ipady=5, fill="x", anchor="n")

        # Heading label: "Add New Book"
        label = customtkinter.CTkLabel(
            master=heading_frame, 
            text="Add New Book",
            font=customtkinter.CTkFont(family="Robot", size=25, weight="bold")
        )
        label.pack(ipady=10)
        
        # Create a main frame for the input fields
        main_frame = customtkinter.CTkFrame(master=self, corner_radius=10)
        main_frame.pack(padx=10, pady=10, ipadx=5, ipady=5, fill="both", expand=True)
        
        # Configure grid layout for the input fields
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)

        # "Book ID" label
        book_id_lbel = customtkinter.CTkLabel(master=main_frame, text="Book ID")
        book_id_lbel.grid(column=1, row=0, padx=5, pady=5)

        # "Book ID" input field
        self.book_id_input = customtkinter.CTkEntry(master=main_frame, width=200)
        self.book_id_input.grid(column=2, row=0, padx=5, pady=5)

        # "Book Name" label
        book_nme_lbel = customtkinter.CTkLabel(master=main_frame, text="Book Name")
        book_nme_lbel.grid(column=1, row=1, padx=5, pady=5)

        # "Book Name" input field
        self.book_nme_input = customtkinter.CTkEntry(master=main_frame, width=200)
        self.book_nme_input.grid(column=2, row=1, padx=5, pady=5)

        # "Book Author" label
        book_author_lbel = customtkinter.CTkLabel(master=main_frame, text="Book Author")
        book_author_lbel.grid(column=1, row=2, padx=5, pady=5)

        # "Book Author" input field
        self.book_author_input = customtkinter.CTkEntry(master=main_frame, width=200)
        self.book_author_input.grid(column=2, row=2, padx=5, pady=5)

        # "Book Edition" label
        book_edition_lbel = customtkinter.CTkLabel(master=main_frame, text="Book Edition")
        book_edition_lbel.grid(column=1, row=3, padx=5, pady=5)

        # "Book Edition" input field
        self.book_edition_input = customtkinter.CTkEntry(master=main_frame, width=200)
        self.book_edition_input.grid(column=2, row=3, padx=5, pady=5)

        # "Book Price" label
        book_price_lbel = customtkinter.CTkLabel(master=main_frame, text="Book Price")
        book_price_lbel.grid(column=1, row=4, padx=5, pady=5)

        # "Book Price" input field
        self.book_price_input = customtkinter.CTkEntry(master=main_frame, width=200)
        self.book_price_input.grid(column=2, row=4, padx=5, pady=5)

        # "Purchased Date" label
        purchase_dt_lbel = customtkinter.CTkLabel(master=main_frame, text="Purchased Date")
        purchase_dt_lbel.grid(column=1, row=5, padx=5, pady=5)

        # Date picker for "Purchased Date"
        self.purch_dt_var = customtkinter.StringVar(self)
        self.purchase_dt = DateEntry(
            main_frame, 
            width=10, 
            borderwidth=2, 
            year=dt_year, 
            textvariable=self.purch_dt_var
        )
        self.purchase_dt.grid(column=2, row=5, padx=5, pady=5)

        # "Add Book" button
        add_new_book_btn = customtkinter.CTkButton(
            master=main_frame, 
            text="Add Book", 
            font=customtkinter.CTkFont(family="Verdana", size=16, weight="bold"), 
            command=self.save_new_book
        )
        add_new_book_btn.grid(column=2, row=6, padx=10, pady=5, ipadx=10, ipady=10)

    # Method to save the book information into the database
    def save_new_book(self):
        # Collect input data
        book_id = self.book_id_input.get()
        book_nme = self.book_nme_input.get()
        book_author = self.book_author_input.get()
        book_edition = self.book_edition_input.get()
        book_price = self.book_price_input.get()
        purchase_dt = self.purch_dt_var.get()

        # Validate inputs
        if book_id != "" and book_nme != "" and book_author != "" and book_edition != "" and book_price != "" and purchase_dt != "":
            data = (
                book_id,
                book_nme,
                book_author,
                book_edition,
                book_price,
                purchase_dt,
                "available"  # Default status
            )
            
            # Save the data to the database
            res = db.add_new_book(data)
            
            # Clear input fields and display success message if the book is saved
            if res is not None and res != '':
                self.book_id_input.delete(0, 'end')
                self.book_nme_input.delete(0, 'end')
                self.book_author_input.delete(0, 'end')
                self.book_edition_input.delete(0, 'end')
                self.book_price_input.delete(0, 'end')
                showinfo(title="Saved", message="New book saved successfully.")
            else:
                # Display error message if the save fails
                showerror(title="Not Saved", message="Something went wrong. Please try again...")
        else:
            # Display error if any field is empty
            showerror(title="Empty Fields", message="Please fill all the details then submit!")
