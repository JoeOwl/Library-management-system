import customtkinter  # CustomTkinter library for modern-looking GUI elements
import tkinter  # Standard Tkinter library for additional GUI features
from database import LMS  # Custom database class for library management
from tkinter.messagebox import showerror, showinfo  # Dialog boxes for success/error messages
from tkinter import filedialog  # Module for file/folder selection dialogs
import pandas as pd  # Pandas library for data manipulation and exporting
import os  # Library for file path operations
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

# Define a GUI class for the "Book Report" feature
class BookReport(customtkinter.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)  # Initialize the parent class
        self.title("Library Management System")  # Set the window title
        self.minsize(400, 300)  # Set minimum window size
        self.maxsize(400, 300)  # Set maximum window size
        self.geometry('400x300')  # Set default window size

        # Create a frame for the heading section
        heading_frame = customtkinter.CTkFrame(master=self, corner_radius=10)
        heading_frame.pack(padx=10, pady=10, ipadx=20, ipady=5, fill="x", anchor="n")

        # Add a label for the heading text
        label = customtkinter.CTkLabel(
            master=heading_frame,
            text="Generate Book Report",
            font=customtkinter.CTkFont(family="Robot", size=25, weight="bold"),
        )
        label.pack(ipady=10)

        # Create a frame for the main content (buttons)
        main_frame = customtkinter.CTkFrame(master=self, corner_radius=10)
        main_frame.pack(padx=10, pady=10, ipadx=5, ipady=5, fill="both", expand=True)

        # Add a button to export available books
        avlb_book_export_btn = customtkinter.CTkButton(
            master=main_frame,
            text="Export Available Book",
            command=self.export_available_book,
        )
        avlb_book_export_btn.pack(padx=10, pady=10)

        # Add a button to export issued books
        issue_book_exp_btn = customtkinter.CTkButton(
            master=main_frame,
            text="Export Issued Book",
            command=self.export_issued_book,
        )
        issue_book_exp_btn.pack(padx=10, pady=10)

        # Add a button to export all books
        export_all_book_btn = customtkinter.CTkButton(
            master=main_frame,
            text="Export All Book",
            command=self.export_all_book,
        )
        export_all_book_btn.pack(padx=10, pady=10)

        # Add a button to export fine details
        export_fine_btn = customtkinter.CTkButton(
            master=main_frame,
            text="Export Fine Details",
            command=self.export_fine_detail,
        )
        export_fine_btn.pack(padx=10, pady=10)

    # Method to export available books to an Excel file
    def export_available_book(self):
        dbt = db.all_available_book()  # Query to fetch available books
        data = pd.read_sql_query(dbt[0], dbt[1])  # Convert the result into a Pandas DataFrame
        try:
            selected_folder = filedialog.askdirectory()  # Ask user to select a folder
            data.to_excel(f"{selected_folder}/available_books.xlsx")  # Save as Excel file
            showinfo(title="Success", message="Exported successfully")  # Success message
        except:
            showerror(title="Error", message="Location not selected...")  # Error message

    # Method to export issued books to an Excel file
    def export_issued_book(self):
        dbt = db.all_issued_book()  # Query to fetch issued books
        data = pd.read_sql_query(dbt[0], dbt[1])  # Convert the result into a Pandas DataFrame
        try:
            selected_folder = filedialog.askdirectory()  # Ask user to select a folder
            data.to_excel(f"{selected_folder}/issued_books.xlsx")  # Save as Excel file
            showinfo(title="Success", message="Exported successfully")  # Success message
        except:
            showerror(title="Error", message="Location not selected...")  # Error message

    # Method to export all books to an Excel file
    def export_all_book(self):
        dbt = db.all_books()  # Query to fetch all books
        data = pd.read_sql_query(dbt[0], dbt[1])  # Convert the result into a Pandas DataFrame
        try:
            selected_folder = filedialog.askdirectory()  # Ask user to select a folder
            data.to_excel(f"{selected_folder}/all_books.xlsx")  # Save as Excel file
            showinfo(title="Success", message="Exported successfully")  # Success message
        except:
            showerror(title="Error", message="Location not selected...")  # Error message

    # Method to export fine details to an Excel file
    def export_fine_detail(self):
        dbt = db.fine_detail()  # Query to fetch fine details
        data = pd.read_sql_query(dbt[0], dbt[1])  # Convert the result into a Pandas DataFrame
        try:
            selected_folder = filedialog.askdirectory()  # Ask user to select a folder
            data.to_excel(f"{selected_folder}/fine_details.xlsx")  # Save as Excel file
            showinfo(title="Success", message="Exported successfully")  # Success message
        except:
            showerror(title="Error", message="Location not selected...")  # Error message
