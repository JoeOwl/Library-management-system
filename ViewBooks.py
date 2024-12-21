# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 03:45:40 2024

@author: MK-Store
"""
#VIEWBOOK 

import customtkinter
import tkinter
from tkinter import ttk
from database import LMS
from tkinter.messagebox import showinfo
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

class ViewBooks(customtkinter.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)  # Initialize parent class (CTkToplevel)
        self.title("Library Management System")  # Set the window title
        self.minsize(1300, 450)  # Set minimum size for the window
        self.maxsize(1300, 450)  # Set maximum size for the window
        self.geometry('1300x450')  # Set the initial size of the window
        
        # Heading Frame - Contains the title of the window
        heading_frame = customtkinter.CTkFrame(master=self, corner_radius=10)
        heading_frame.pack(padx=10, pady=10, ipadx=20, ipady=5, fill="x", anchor="n")
        
        # Label showing the title of the screen
        label = customtkinter.CTkLabel(master=heading_frame, text="View Book", font=customtkinter.CTkFont(family="Robot", size=25, weight="bold"))
        label.pack(ipady=10)
        
        # Main Frame - Contains the table to view books
        main_frame = customtkinter.CTkFrame(master=self, corner_radius=10)
        main_frame.pack(padx=10, pady=10, ipadx=5, ipady=5, fill="both", expand=True)
        
        # Define columns for the treeview (book data table)
        columns = ('book_id', 'book_name', 'book_author', 'book_edition', 'book_price', 'purchase_dt', 'status')

        # Create a Treeview widget to display the book list in a table format
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings')
        
        # Define headings for each column
        self.tree.heading('book_id', text='Book ID')
        self.tree.heading('book_name', text='Name')
        self.tree.heading('book_author', text='Author')
        self.tree.heading('book_edition', text='Edition')
        self.tree.heading('book_price', text='Price')
        self.tree.heading('purchase_dt', text='Purchased Date')
        self.tree.heading('status', text='Status')
        
        # Load book data from the database and insert into the treeview
        self.load_book_data()
        
        # Bind the item selection event to fetch and show book details
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)
        
        # Display the treeview in the main frame
        self.tree.grid(row=0, column=0, sticky='nsew')
        
        # Create a vertical scrollbar for the treeview
        scrollbar = customtkinter.CTkScrollbar(main_frame, orientation='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

    def load_book_data(self):
        # Fetch the list of all books from the database
        book_list = db.view_book_list()
        
        # Insert each book's details as a row in the treeview
        for i in book_list:
            self.tree.insert('', tkinter.END, values=i)
    
    def item_selected(self, event):
        # Get the selected book's data when the user clicks on a row in the treeview
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            record = item['values']
        
        # Open a new window to display detailed information about the selected book
        self.details_win(record)
    
    def details_win(self, record):
        # Create a new top-level window to display book details
        window = customtkinter.CTkToplevel(self)
        window.title("Library Management System")  # Set the window title
        window.minsize(430, 630)  # Set the minimum size for the window
        window.maxsize(430, 630)  # Set the maximum size for the window
        window.geometry('430x630')  # Set the initial size of the window
        
        # Main frame inside the details window
        main_frame = customtkinter.CTkFrame(master=window, corner_radius=10, height=100)
        main_frame.pack(padx=10, pady=10, ipadx=5, ipady=5, fill="both", expand=True)
        
        # Label showing the title of the details section
        label = customtkinter.CTkLabel(master=main_frame, text="Details", font=customtkinter.CTkFont(family="Robot", size=30, weight="bold"), fg_color="#ca1a27", corner_radius=8, width=150)
        label.grid(column=0, row=0, pady=15, padx=5, ipadx=5, ipady=5, sticky='e')
        
        # Display the book's details in labels and disabled input fields
        # Book ID
        lbel1 = customtkinter.CTkLabel(master=main_frame, text="Book ID :", font=customtkinter.CTkFont(family="Verdana", size=25, weight="normal"))
        lbel1.grid(column=0, row=1, padx=5, pady=5, sticky='e')
        tvar1 = customtkinter.IntVar(window, record[0])
        inp1 = customtkinter.CTkEntry(master=main_frame, font=customtkinter.CTkFont(family="Verdana", size=20, weight="normal"), width=220, state='disabled', textvariable=tvar1)
        inp1.grid(column=1, row=1, padx=5, pady=5, sticky='w')
        
        # Book Name
        lbel3 = customtkinter.CTkLabel(master=main_frame, text="Book Name :", font=customtkinter.CTkFont(family="Verdana", size=25, weight="normal"))
        lbel3.grid(column=0, row=2, padx=5, pady=5, sticky='e')
        tvar2 = customtkinter.StringVar(window, record[1])
        lbel4 = customtkinter.CTkEntry(master=main_frame, font=customtkinter.CTkFont(family="Verdana", size=20, weight="normal"), width=220, state='disabled', textvariable=tvar2)
        lbel4.grid(column=1, row=2, padx=5, pady=5, sticky='w')
        
        # Book Author
        lbel5 = customtkinter.CTkLabel(master=main_frame, text="Book Author :", font=customtkinter.CTkFont(family="Verdana", size=25, weight="normal"))
        lbel5.grid(column=0, row=3, padx=5, pady=5, sticky='e')
        tvar3 = customtkinter.StringVar(window, record[2])
        lbel6 = customtkinter.CTkEntry(master=main_frame, font=customtkinter.CTkFont(family="Verdana", size=20, weight="normal"), width=220, state='disabled', textvariable=tvar3)
        lbel6.grid(column=1, row=3, padx=5, pady=5, sticky='w')
        
        # Book Edition
        lbel7 = customtkinter.CTkLabel(master=main_frame, text="Book Edition :", font=customtkinter.CTkFont(family="Verdana", size=25, weight="normal"))
        lbel7.grid(column=0, row=4, padx=5, pady=5, sticky='e')
        tvar4 = customtkinter.StringVar(window, record[3])
        lbel8 = customtkinter.CTkEntry(master=main_frame, font=customtkinter.CTkFont(family="Verdana", size=20, weight="normal"), width=220, state='disabled', textvariable=tvar4)
        lbel8.grid(column=1, row=4, padx=5, pady=5, sticky='w')
        
        # Book Price
        lbel9 = customtkinter.CTkLabel(master=main_frame, text="Book Price :", font=customtkinter.CTkFont(family="Verdana", size=25, weight="normal"))
        lbel9.grid(column=0, row=5, padx=5, pady=5, sticky='e')
        tvar5 = customtkinter.StringVar(window, record[4])
        lbel10 = customtkinter.CTkEntry(master=main_frame, font=customtkinter.CTkFont(family="Verdana", size=20, weight="normal"), width=220, state='disabled', textvariable=tvar5)
        lbel10.grid(column=1, row=5, padx=5, pady=5, sticky='w')
        
        # Book Purchase Date
        lbel11 = customtkinter.CTkLabel(master=main_frame, text="Purchase Date:", font=customtkinter.CTkFont(family="Verdana", size=25, weight="normal"))
        lbel11.grid(column=0, row=6, padx=5, pady=5, sticky='e')
        # Book Purchase Date Display - Show the purchase date of the book in a disabled entry field
        tvar6 = customtkinter.StringVar(window, record[5])  # Set the value from the record
        lbel12 = customtkinter.CTkEntry(master=main_frame, font=customtkinter.CTkFont(family="Verdana", size=20, weight="normal"), width=220, state='disabled', textvariable=tvar6)
        lbel12.grid(column=1, row=6, padx=5, pady=5, sticky='w')

    # Check the book's status (available or issued) and display relevant messages
        if record[6] == 'available':
        # If the book is available, show a label with green background
            lb1 = customtkinter.CTkLabel(master=window, text="Available in Library", fg_color="#0dcd6a", corner_radius=8, font=customtkinter.CTkFont(family='Tahoma', size=25, weight='bold'))
            lb1.pack(ipady=5, ipadx=5, fill='x', anchor='n')
        elif record[6] == 'issued':
            # If the book is issued, show a red background label and additional student details
            lb1 = customtkinter.CTkLabel(master=window, text="Book is issued, details below", fg_color="#e30f67", corner_radius=8, font=customtkinter.CTkFont(family='Tahoma', size=20, weight='bold'))
            lb1.pack(ipady=5, ipadx=5, fill='x', anchor='n')
    
            # Create a frame to hold the student details
            sec_frame = customtkinter.CTkFrame(master=window, corner_radius=10)
            sec_frame.pack(padx=10, pady=10, ipadx=5, ipady=5, fill="both", expand=True)
    
            # Get issued book details and corresponding student information
            isu_book_dtail = db.view_issued_book(record[0])
            stu_detail = db.view_student(isu_book_dtail[1])
    
            # Display student details (ID, name, and class)
            l1 = customtkinter.CTkLabel(master=sec_frame, text="Student ID :", font=customtkinter.CTkFont(family="Verdana", size=25, weight="normal"))
            l1.grid(column=0, row=1, padx=5, pady=5, sticky='e')
            tv1 = customtkinter.StringVar(window, stu_detail[0])
            in1 = customtkinter.CTkEntry(master=sec_frame, font=customtkinter.CTkFont(family="Verdana", size=20, weight="normal"), width=210, state='disabled', textvariable=tv1)
            in1.grid(column=1, row=1, padx=5, pady=5, sticky='w')
    
            # Display student name
            l2 = customtkinter.CTkLabel(master=sec_frame, text="Student Name :", font=customtkinter.CTkFont(family="Verdana", size=25, weight="normal"))
            l2.grid(column=0, row=2, padx=5, pady=5, sticky='e')
            tv2 = customtkinter.StringVar(window, stu_detail[1])
            in2 = customtkinter.CTkEntry(master=sec_frame, font=customtkinter.CTkFont(family="Verdana", size=20, weight="normal"), width=210, state='disabled', textvariable=tv2)
            in2.grid(column=1, row=2, padx=5, pady=5, sticky='w')
            
            # Display student class
            l3 = customtkinter.CTkLabel(master=sec_frame, text="Student Class :", font=customtkinter.CTkFont(family="Verdana", size=25, weight="normal"))
            l3.grid(column=0, row=3, padx=5, pady=5, sticky='e')
            tv3 = customtkinter.StringVar(window, stu_detail[2])
            in3 = customtkinter.CTkEntry(master=sec_frame, font=customtkinter.CTkFont(family="Verdana", size=20, weight="normal"), width=210, state='disabled', textvariable=tv3)
            in3.grid(column=1, row=3, padx=5, pady=5, sticky='w')
            
            # Convert the issue date and return date from datetime string to a formatted date
            isu_dt = datetime.datetime.strptime(isu_book_dtail[2], "%Y-%m-%d %H:%M:%S")
            exp_dt = datetime.datetime.strptime(isu_book_dtail[3], "%Y-%m-%d %H:%M:%S")
    
            # Display issue date
            l4 = customtkinter.CTkLabel(master=sec_frame, text="Issued Date :", font=customtkinter.CTkFont(family="Verdana", size=25, weight="normal"))
            l4.grid(column=0, row=4, padx=5, pady=5, sticky='e')
            tv4 = customtkinter.StringVar(window, isu_dt.strftime("%b %d %Y, %I:%M:%S"))
            in4 = customtkinter.CTkEntry(master=sec_frame, font=customtkinter.CTkFont(family="Verdana", size=20, weight="normal"), width=210, state='disabled', textvariable=tv4)
            in4.grid(column=1, row=4, padx=5, pady=5, sticky='w')
    
            # Display expected return date
            l5 = customtkinter.CTkLabel(master=sec_frame, text="Return Date :", font=customtkinter.CTkFont(family="Verdana", size=25, weight="normal"))
            l5.grid(column=0, row=5, padx=5, pady=5, sticky='e')
            tv5 = customtkinter.StringVar(window, exp_dt.strftime("%b %d %Y, %I:%M:%S"))
            in5 = customtkinter.CTkEntry(master=sec_frame, font=customtkinter.CTkFont(family="Verdana", size=20, weight="normal"), width=210, state='disabled', textvariable=tv5)
            in5.grid(column=1, row=5, padx=5, pady=5, sticky='w')
        