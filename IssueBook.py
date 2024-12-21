import customtkinter  # CustomTkinter library for modern GUI components
import tkinter  # Tkinter library for basic GUI components
from database import LMS  # Custom library for database operations related to the library
from tkinter.messagebox import showerror, showinfo  # Messagebox for dialog messages
from tkinter import ttk  # Additional widget library for Tkinter
import datetime  # Library for working with dates and times
import json  # Library for handling JSON data
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

# Load settings from a JSON file
settings_file_path = os.path.join(executable_directory, 'settings.json')
with open(settings_file_path, "r") as settings_file:
    settings = json.load(settings_file)

# IssueBook GUI window class
class IssueBook(customtkinter.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)  # Initialize the parent class
        self.title("Library Management System")  # Set the window title
        self.minsize(400, 250)  # Set the minimum window size
        self.maxsize(400, 250)  # Set the maximum window size
        self.geometry('300x250')  # Set the default window size

        # Retrieve the issue duration from the settings file
        self.no_expiry_days = settings["issue_duration"]

        # Create a heading frame for the title
        heading_frame = customtkinter.CTkFrame(master=self, corner_radius=10)
        heading_frame.pack(padx=10, pady=10, ipadx=20, ipady=5, fill="x", anchor="n")

        # "Issue Book" label
        self.label = customtkinter.CTkLabel(
            master=heading_frame,
            text="Issue Book",
            font=customtkinter.CTkFont(family="Robot", size=25, weight="bold")
        )
        self.label.pack(ipady=10)

        # Create a main frame for the input fields and button
        main_frame = customtkinter.CTkFrame(master=self, corner_radius=10)
        main_frame.pack(padx=10, pady=10, ipadx=5, ipady=5, fill="both", expand=True)

        # Configure columns for layout alignment
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)

        # "Book ID" label
        book_id_lbel = customtkinter.CTkLabel(master=main_frame, text="Book ID")
        book_id_lbel.grid(column=1, row=0, padx=5, pady=5)

        # "Book ID" input
        self.book_id_var = customtkinter.StringVar(self)  # Variable to hold Book ID input
        self.book_id_input = customtkinter.CTkEntry(master=main_frame, width=200, textvariable=self.book_id_var)
        self.book_id_input.grid(column=2, row=0, padx=5, pady=10)

        # "Student ID" label
        student_id_lbel = customtkinter.CTkLabel(master=main_frame, text="Student ID")
        student_id_lbel.grid(column=1, row=1, padx=5, pady=5)

        # "Student ID" input
        self.student_id_var = customtkinter.StringVar(self)  # Variable to hold Student ID input
        self.student_id_input = customtkinter.CTkEntry(master=main_frame, width=200, textvariable=self.student_id_var)
        self.student_id_input.grid(column=2, row=1, padx=5, pady=5)

        # "Issue Book" Button
        issue_book_btn = customtkinter.CTkButton(
            master=main_frame,
            text="Issue Book",
            command=self.issue_book  # Bind button to issue_book method
        )
        issue_book_btn.grid(column=2, row=2, padx=10, pady=5)

    # Method to issue a book
    def issue_book(self):
        # Get input values for Book ID and Student ID
        book_id = self.book_id_var.get()
        book_id = int(book_id)  # Convert to integer
        student_id = self.student_id_var.get()
        student_id = int(student_id)  # Convert to integer

        # Check if the provided Book ID and Student ID exist in the database
        if book_id in self.all_book_id() and student_id in self.all_student_id():
            status = 'available'  # Expected status for the book to be issued

            # Check if the book is available for issuing
            if status in db.select_book_status(book_id):
                cur_dt = datetime.datetime.now()  # Get current date and time
                std_cur_dt = cur_dt.isoformat(' ', 'seconds')  # Format the date and time

                # Prepare data for issuing the book
                data = (
                    book_id,
                    student_id,
                    std_cur_dt,
                    self.expiry_datetime()  # Calculate expiry date
                )

                # Update the database with issue details and book status
                res1 = db.issue_book(data)
                res2 = db.update_book_status(book_id, "issued")

                # Show success or error messages based on operation results
                if res1 is not None:
                    showinfo(title="Issued", message=f"Book issued successfully to {student_id}")
                else:
                    showerror(title="Error", message="Something went wrong! Try Again..")
            else:
                showerror(title="Not Available", message="This book is not available or it is issued to another one.")
        else:
            showerror(title="Not Found", message="Book not found! or Student Not found! Please check Book ID or Student ID and try again...")

    # Method to return all book IDs
    def all_book_id(self):
        all_bookID = []  # List to store all Book IDs
        for i in db.all_book_id():  # Fetch all Book IDs from the database
            all_bookID.append(i[0])
        return all_bookID

    # Method to return all student IDs
    def all_student_id(self):
        all_studentID = []  # List to store all Student IDs
        for i in db.all_student_id():  # Fetch all Student IDs from the database
            all_studentID.append(i[0])
        return all_studentID

    # Method to calculate the expiry date for the issued book
    def expiry_datetime(self):
        exp_datetime = datetime.datetime.now()  # Get the current date and time
        exp_datetime += datetime.timedelta(days=self.no_expiry_days)  # Add the issue duration
        std_exp_dt = exp_datetime.isoformat(' ', 'seconds')  # Format the expiry date
        return std_exp_dt
