import customtkinter
from tkinter.messagebox import showerror, showinfo
import requests
import os
import sys

def get_executable_directory():
    # Get the directory of the executable (or script during development)
    if getattr(sys, 'frozen', False):  # Check if the program is frozen (packaged as .exe)
        return os.path.dirname(sys.executable)  # Path to the .exe
    else:
        return os.path.dirname(os.path.abspath(__file__))  # Path to the script during development

# "RetrieveBook" GUI window class
class RetrieveBook(customtkinter.CTkToplevel):
    def __init__(self, master=None):
        # Initialize the parent CTkToplevel
        super().__init__(master)

        # Set window properties
        self.title("Retrieve Book Details")
        self.minsize(400, 300)
        self.geometry('400x300')

        # Create a frame for the heading section
        heading_frame = customtkinter.CTkFrame(master=self, corner_radius=10)
        heading_frame.pack(padx=10, pady=10, ipadx=20, ipady=5, fill="x", anchor="n")

        # Heading label: "Retrieve Book Details"
        label = customtkinter.CTkLabel(
            master=heading_frame, 
            text="Retrieve Book Details",
            font=customtkinter.CTkFont(family="Robot", size=20, weight="bold")
        )
        label.pack(ipady=10)

        # Create a main frame for input and output fields
        main_frame = customtkinter.CTkFrame(master=self, corner_radius=10)
        main_frame.pack(padx=10, pady=10, ipadx=5, ipady=5, fill="both", expand=True)

        # Configure grid layout for the input fields
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=2)

        # "ISBN ID" label
        isbn_label = customtkinter.CTkLabel(master=main_frame, text="ISBN ID")
        isbn_label.grid(column=1, row=0, padx=5, pady=5)

        # "ISBN ID" input field
        self.isbn_input = customtkinter.CTkEntry(master=main_frame, width=200)
        self.isbn_input.grid(column=2, row=0, padx=5, pady=5)

        # "Retrieve Book" button
        retrieve_book_btn = customtkinter.CTkButton(
            master=main_frame, 
            text="Retrieve", 
            font=customtkinter.CTkFont(family="Verdana", size=14, weight="bold"), 
            command=self.retrieve_book_details
        )
        retrieve_book_btn.grid(column=2, row=1, padx=10, pady=10, ipadx=10, ipady=5)

        # Output label for book details
        self.output_label = customtkinter.CTkLabel(
            master=main_frame, 
            text="", 
            wraplength=350,
            justify="left"
        )
        self.output_label.grid(column=1, row=2, columnspan=2, padx=10, pady=10)

    # Method to retrieve book details using an API
    def retrieve_book_details(self):
        isbn_id = self.isbn_input.get()  # Get the ISBN ID from the input field

        if isbn_id != "":
            # API endpoint for retrieving book details
            api_url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn_id}"
            
            try:
                # Send a GET request to the API
                response = requests.get(api_url)
                response.raise_for_status()  # Raise an error for HTTP issues
                data = response.json()

                # Check if any book information is available
                if "items" in data and len(data["items"]) > 0:
                    book_info = data["items"][0]["volumeInfo"]

                    # Extract relevant details
                    title = book_info.get("title", "N/A")
                    authors = ", ".join(book_info.get("authors", ["N/A"]))
                    published_date = book_info.get("publishedDate", "N/A")
                    description = book_info.get("description", "N/A")

                    # Format and display the book details
                    details = (
                        f"Title: {title}\n"
                        f"Authors: {authors}\n"
                        f"Published Date: {published_date}\n"
                        f"Description: {description}"
                    )
                    self.output_label.configure(text=details)
                    showinfo(title="Book Found", message="Book details retrieved successfully.")
                else:
                    # Display an error message if no book is found
                    self.output_label.configure(text="")
                    showerror(title="Not Found", message="No book found with the provided ISBN ID.")

            except requests.RequestException as e:
                # Handle any errors during the API request
                self.output_label.configure(text="")
                showerror(title="Error", message=f"An error occurred while fetching data: {e}")
        else:
            # Display an error message if the ISBN ID is empty
            showerror(title="Empty Field", message="Please enter an ISBN ID to search.")
