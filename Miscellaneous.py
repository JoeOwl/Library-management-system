# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 03:36:09 2024

@author: MK-Store
"""

#MISCELLANEOUS 

import customtkinter
import tkinter
from tkinter import ttk
from database import LMS
from tkinter.messagebox import showinfo
import os
import sys

db = LMS(os.path.join(os.path.dirname(sys.executable), "lms.db"))  # Database initialization for LMS using a database file located in the executable's directory.

# Define a class for handling miscellaneous books in the library system
class Miscellaneous(customtkinter.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Library Management System")  # Set the window title
        self.minsize(1300, 450)  # Set minimum window size
        self.maxsize(1300, 450)  # Set maximum window size
        self.geometry('1300x450')  # Define the window size explicitly

        # Create a heading frame for the window
        heading_frame = customtkinter.CTkFrame(master=self, corner_radius=10)
        heading_frame.pack(padx=10, pady=10, ipadx=20, ipady=5, fill="x", anchor="n")

        # Add a heading label to the heading frame
        label = customtkinter.CTkLabel(
            master=heading_frame,
            text="Miscellaneous Books",
            font=customtkinter.CTkFont(family="Robot", size=25, weight="bold")
        )
        label.pack(ipady=10)

        # Create a main frame for displaying the table and other components
        main_frame = customtkinter.CTkFrame(master=self, corner_radius=10)
        main_frame.pack(padx=10, pady=10, ipadx=5, ipady=5, fill="both", expand=True)

        # Define columns for the table
        columns = ('book_id', 'book_name', 'book_author', 'book_edition', 'book_price', 'purchase_dt', 'status')

        # Create a Treeview widget for displaying book data
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings')

        # Define the column headings for the Treeview
        self.tree.heading('book_id', text='Book ID')
        self.tree.heading('book_name', text='Name')
        self.tree.heading('book_author', text='Author')
        self.tree.heading('book_edition', text='Edition')
        self.tree.heading('book_price', text='Price')
        self.tree.heading('purchase_dt', text='Purchased Date')
        self.tree.heading('status', text='Status')

        # Load book data from the database and populate the Treeview
        self.load_book_data()

        # Bind an event to handle item selection in the Treeview
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)

        # Add the Treeview widget to the main frame
        self.tree.grid(row=0, column=0, sticky='nsew')

        # Add a vertical scrollbar to the Treeview
        scrollbar = customtkinter.CTkScrollbar(main_frame, orientation='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

    def load_book_data(self):
        """
        Load miscellaneous book data from the database and insert it into the Treeview.
        """
        book_list = db.miscellaneous_books()  # Retrieve book data
        for i in book_list:
            self.tree.insert('', tkinter.END, values=i)  # Insert each book record into the Treeview

    def item_selected(self, event):
        """
        Handle item selection in the Treeview and display book details.
        """
        for selected_item in self.tree.selection():  # Iterate over selected items
            item = self.tree.item(selected_item)  # Get item details
            record = item['values']  # Extract book details as a tuple

        self.details_win(record)  # Open a new window to show book details

    def details_win(self, record):
        """
        Open a new window displaying detailed information about the selected book.
        """
        # Create a new top-level window for book details
        window = customtkinter.CTkToplevel(self)
        window.title("Library Management System")
        window.minsize(430, 630)
        window.maxsize(430, 630)
        window.geometry('430x630')

        # Create a main frame in the details window
        main_frame = customtkinter.CTkFrame(master=window, corner_radius=10, height=100)
        main_frame.pack(padx=10, pady=10, ipadx=5, ipady=5, fill="both", expand=True)

        # Add a heading label for the details window
        label = customtkinter.CTkLabel(
            master=main_frame,
            text="Details",
            font=customtkinter.CTkFont(family="Robot", size=30, weight="bold"),
            fg_color="#ca1a27",
            corner_radius=8,
            width=150
        )
        label.grid(column=0, row=0, pady=15, padx=5, ipadx=5, ipady=5, sticky='e')

        # Define labels and entry fields for each book detail, with fields disabled
        lbel1 = customtkinter.CTkLabel(
            master=main_frame, text="Book ID :", font=customtkinter.CTkFont(family="Verdana", size=25)
        )
        lbel1.grid(column=0, row=1, padx=5, pady=5, sticky='e')

        tvar1 = customtkinter.IntVar(window, record[0])  # Store book ID
        inp1 = customtkinter.CTkEntry(
            master=main_frame, font=customtkinter.CTkFont(family="Verdana", size=20),
            width=220, state='disabled', textvariable=tvar1
        )
        inp1.grid(column=1, row=1, padx=5, pady=5, sticky='w')

        # Repeat similar pattern for other book details (Name, Author, Edition, Price, etc.)
        lbel3 = customtkinter.CTkLabel(master=main_frame,text="Book Name :",font=customtkinter.CTkFont(family="Verdana", size=25, weight="normal"))
        lbel3.grid(column=0,row=2,padx=5, pady=5,sticky='e')
       
        tvar2 = customtkinter.StringVar(window,record[1])
        lbel4 = customtkinter.CTkEntry(master=main_frame, font=customtkinter.CTkFont(family="Verdana", size=20, weight="normal"),width=220,state='disabled', textvariable=tvar2)
        lbel4.grid(column=1,row=2,padx=5, pady=5,sticky='w')
       
        lbel5 = customtkinter.CTkLabel(master=main_frame,text="Book Author :",font=customtkinter.CTkFont(family="Verdana", size=25, weight="normal"))
        lbel5.grid(column=0,row=3,padx=5, pady=5,sticky='e')
       
        tvar3 = customtkinter.StringVar(window,record[2])
        lbel6 = customtkinter.CTkEntry(master=main_frame,font=customtkinter.CTkFont(family="Verdana", size=20, weight="normal"),width=220,state='disabled', textvariable=tvar3)
        lbel6.grid(column=1,row=3,padx=5, pady=5,sticky='w')
       
        lbel7 = customtkinter.CTkLabel(master=main_frame,text="Book Edition :",font=customtkinter.CTkFont(family="Verdana", size=25, weight="normal"))
        lbel7.grid(column=0,row=4,padx=5, pady=5,sticky='e')
       
        tvar4 = customtkinter.StringVar(window,record[3])
        lbel8 = customtkinter.CTkEntry(master=main_frame,font=customtkinter.CTkFont(family="Verdana", size=20, weight="normal"),width=220,state='disabled', textvariable=tvar4)
        lbel8.grid(column=1,row=4,padx=5, pady=5,sticky='w')
       
        lbel9 = customtkinter.CTkLabel(master=main_frame,text="Book Price :",font=customtkinter.CTkFont(family="Verdana", size=25, weight="normal"))
        lbel9.grid(column=0,row=5,padx=5, pady=5,sticky='e')
       
        tvar5 = customtkinter.StringVar(window,record[4])
        lbel10 = customtkinter.CTkEntry(master=main_frame, font=customtkinter.CTkFont(family="Verdana", size=20, weight="normal"),width=220,state='disabled', textvariable=tvar5)
        lbel10.grid(column=1,row=5,padx=5, pady=5,sticky='w')
       
        lbel11 = customtkinter.CTkLabel(master=main_frame,text="Purchase Date:",font=customtkinter.CTkFont(family="Verdana", size=25, weight="normal"))
        lbel11.grid(column=0,row=6,padx=5, pady=5,sticky='e')
       
        tvar6 = customtkinter.StringVar(window,record[5])
        lbel12 = customtkinter.CTkEntry(master=main_frame, font=customtkinter.CTkFont(family="Verdana", size=20, weight="normal"),width=220,state='disabled', textvariable=tvar6)
        lbel12.grid(column=1,row=6,padx=5, pady=5,sticky='w')
        # Add a footer label to indicate the type of book
        lb1 = customtkinter.CTkLabel(
            master=window, text="Miscellaneous Book", fg_color="#e30f67", corner_radius=8,
            font=customtkinter.CTkFont(family='Tahoma', size=20, weight='bold')
        )
        lb1.pack(ipady=5, ipadx=5, fill='x', anchor='n')
