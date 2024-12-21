import sqlite3
import customtkinter
import tkinter
from tkinter.messagebox import showerror, showwarning, showinfo
from tkcalendar import DateEntry
import datetime
import os
import sys
from database import LMS  # Assuming LMS class is in the 'database' module

def get_executable_directory():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

# Get the directory where the .exe is located
executable_directory = get_executable_directory()
db = LMS(os.path.join(executable_directory, "lms.db"))

class SearchBook(customtkinter.CTkToplevel):
    def __init__(self, master=None, db=None):
        super().__init__(master)

        # Ensure db is not None
        if db is None:
            raise ValueError("Database instance (LMS) is required")

        self.db = db  # Store the LMS instance

        # Window properties
        self.title("Library Management System")
        self.geometry('600x400')
        
        # Heading Frame
        heading_frame = customtkinter.CTkFrame(master=self, corner_radius=10)
        heading_frame.pack(padx=10, pady=10, ipadx=20, ipady=5, fill="x", anchor="n")
        
        label = customtkinter.CTkLabel(
            master=heading_frame, 
            text="Search Books",
            font=customtkinter.CTkFont(family="Robot", size=25, weight="bold")
        )
        label.pack(ipady=10)

        # Main Frame for inputs
        main_frame = customtkinter.CTkFrame(master=self, corner_radius=10)
        main_frame.pack(padx=10, pady=10, ipadx=5, ipady=5, fill="both", expand=True)
        
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)

        # Search Filter Label
        search_filter_label = customtkinter.CTkLabel(master=main_frame, text="Search By:")
        search_filter_label.grid(column=1, row=0, padx=5, pady=5)

        # Dropdown for Search Filter
        self.filter_var = tkinter.StringVar(value="All")
        search_filter = customtkinter.CTkOptionMenu(
            master=main_frame, 
            values=["All", "ID", "Name", "Author"],
            variable=self.filter_var
        )
        search_filter.grid(column=2, row=0, padx=5, pady=5)

        # Search Query Label
        search_query_label = customtkinter.CTkLabel(master=main_frame, text="Search Query:")
        search_query_label.grid(column=1, row=1, padx=5, pady=5)

        # Search Query Input Field
        self.search_query_input = customtkinter.CTkEntry(master=main_frame, width=200)
        self.search_query_input.grid(column=2, row=1, padx=5, pady=5)

        # Search Button
        search_button = customtkinter.CTkButton(
            master=main_frame, 
            text="Search",
            font=customtkinter.CTkFont(family="Verdana", size=16, weight="bold"),
            command=self.search_books
        )
        search_button.grid(column=2, row=2, padx=10, pady=10)

        # Results Frame
        results_frame = customtkinter.CTkFrame(master=self, corner_radius=10)
        results_frame.pack(padx=10, pady=10, ipadx=5, ipady=5, fill="both", expand=True)

        # Results Label
        results_label = customtkinter.CTkLabel(master=results_frame, text="Search Results:")
        results_label.pack(pady=5)

        # Results Listbox
        self.results_listbox = tkinter.Listbox(results_frame, height=10, width=80)
        self.results_listbox.pack(padx=5, pady=5, fill="both", expand=True)
        
    def search_books(self):
        search_query = self.search_query_input.get()
        filter_by = self.filter_var.get().lower()

        if not search_query.strip():
            showwarning(title="Empty Query", message="Please enter a search query!")
            return

        if filter_by == "id":
            search_key = "book_id"
            search_value = search_query
        elif filter_by == "name":
            search_key = "book_name"
            search_value = search_query
        elif filter_by == "author":
            search_key = "book_author"
            search_value = search_query
        else:  # Default to searching all fields
            search_key = "book_name"
            search_value = search_query

        # Use LMS instance's search_book method to search for books
        results = self.db.search_book(search_key, search_value)

        # Display results
        self.results_listbox.delete(0, tkinter.END)
        if results:
            for result in results:
                self.results_listbox.insert(
                    tkinter.END, 
                    f"ID: {result[0]}, Name: {result[1]}, Author: {result[2]}, Edition: {result[3]}, Price: {result[4]}, Date: {result[5]}, Status: {result[6]}"
                )
        else:
            self.results_listbox.insert(tkinter.END, "No results found.")


