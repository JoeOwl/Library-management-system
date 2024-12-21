# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 03:42:25 2024

@author: MK-Store
"""

#RETURNBOOK 

import customtkinter
import tkinter
from database import LMS
from tkinter.messagebox import showerror, showinfo, askyesno
import datetime
import json
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

# Load settings from a JSON file
settings_file_path = os.path.join(executable_directory, 'settings.json')
with open(settings_file_path, "r") as settings_file:
    settings = json.load(settings_file)

# Define the class for the "Return Book" functionality
class ReturnBook(customtkinter.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Library Management System")  # Set the title of the window
        self.minsize(400, 250)  # Minimum size of the window
        self.maxsize(400, 250)  # Maximum size of the window
        self.geometry('400x250')  # Fixed dimensions of the window
        self.charge_per_day = settings["charge_per_day"]  # Fetch fine settings from JSON

        # Create a heading frame
        heading_frame = customtkinter.CTkFrame(master=self, corner_radius=10)
        heading_frame.pack(padx=10, pady=10, ipadx=20, ipady=5, fill="x", anchor="n")

        # Add a label to the heading frame
        label = customtkinter.CTkLabel(
            master=heading_frame,
            text="Return Book",
            font=customtkinter.CTkFont(family="Robot", size=25, weight="bold")
        )
        label.pack(ipady=10)

        # Create the main frame
        main_frame = customtkinter.CTkFrame(master=self, corner_radius=10)
        main_frame.pack(padx=10, pady=10, ipadx=5, ipady=5, fill="both", expand=True)

        # Add a label for "Book ID"
        book_id_lbel = customtkinter.CTkLabel(
            master=main_frame,
            text="Book ID",
            font=customtkinter.CTkFont(family="Verdana", size=16, weight="normal")
        )
        book_id_lbel.pack(pady=10)

        # Create an input field for the book ID
        self.book_id_var = customtkinter.StringVar(self)
        self.book_id_input = customtkinter.CTkEntry(master=main_frame, width=200, textvariable=self.book_id_var)
        self.book_id_input.pack(padx=5, pady=5)

        # Add a button to return the book
        return_book_btn = customtkinter.CTkButton(master=main_frame, text="Return Book", command=self.return_book)
        return_book_btn.pack(padx=10, pady=5)

    def return_book(self):
        """
        Main method to handle the book return process.
        Checks for book validity, calculates fines, and updates book status.
        """
        book_id = self.book_id_var.get()  # Retrieve entered book ID
        book_id = int(book_id)  # Convert book ID to integer

        if book_id in self.all_book_id():  # Check if book ID exists
            status = 'issued'
            if status in db.select_book_status(book_id):  # Verify book is issued
                book_detl = db.select_issued_book_det(book_id)  # Fetch issued book details

                # Calculate fine if return is late
                std_exp_dt = datetime.datetime.strptime(book_detl[2], "%Y-%m-%d %H:%M:%S")
                if std_exp_dt < datetime.datetime.now():
                    fine = self.total_fine(std_exp_dt)
                    conf = askyesno(
                        title="Fine Confirmation",
                        message=f"Student is fined {fine[0]} for {fine[1]} days extra. Is fine paid?"
                    )
                    if conf:
                        self.save_fine_details(book_detl[0], book_detl[1], book_detl[2], fine)  # Save fine details
                        self.return_book_func(book_id)  # Complete book return process
                    else:
                        misl_conf = askyesno(
                            title="Miscellaneous",
                            message="Do you want to move this book to Miscellaneous?"
                        )
                        if misl_conf:
                            try:
                                db.update_book_status(book_id, 'miscellaneous')  # Update book status
                                db.move_to_miscellaneous(book_id)  # Move to Miscellaneous section
                                showinfo(title='Success', message='Book moved to Miscellaneous section.')
                            except:
                                showerror(title='Server Error', message='An error occurred. Try again!')
                        else:
                            showerror(title="Error - Fine", message="Please collect the fine first!")
                else:
                    self.return_book_func(book_id)  # Return book if no fine is applicable
            else:
                showerror(title="Not Issued", message="This book is not issued to anyone.")
        else:
            showerror(title="Not Found", message="No book found with the given ID.")

    def all_book_id(self):
        """
        Fetch all book IDs from the database.
        Returns:
            List of all book IDs.
        """
        all_bookID = []
        for i in db.all_book_id():
            all_bookID.append(i[0])  # Extract and append each book ID
        return all_bookID

    def return_book_func(self, book_id):
        """
        Finalize the book return process.
        Updates book status and provides feedback to the user.
        """
        res1 = db.return_book(book_id)  # Mark book as returned
        res2 = db.update_book_status(book_id, "available")  # Update book availability status
        if res1 == "returned":
            showinfo(title="Book Returned", message=f"Book ID - {book_id} successfully returned!")
        else:
            showerror(title="Error", message="An error occurred. Please try again.")

    def total_fine(self, exp_dt):
        """
        Calculate the total fine for late return.
        Args:
            exp_dt: Expected return date.
        Returns:
            Tuple containing total fine and number of overdue days.
        """
        delta = datetime.datetime.now() - exp_dt
        total_fine = delta.days * self.charge_per_day
        return (total_fine, delta.days)

    def save_fine_details(self, book_id, student_id, issued_dt, fine):
        """
        Save fine details to the database.
        Args:
            book_id: ID of the returned book.
            student_id: ID of the student.
            issued_dt: Date when the book was issued.
            fine: Tuple containing total fine and overdue days.
        """
        dt = datetime.datetime.now()
        std_dt = dt.isoformat(' ', 'seconds')  # Format the current date-time
        data = (
            book_id,
            student_id,
            issued_dt,
            std_dt,
            fine[0],  # Total fine amount
            fine[1]  # Number of overdue days
        )
        res = db.save_fine_detail(data)  # Save fine details in the database
