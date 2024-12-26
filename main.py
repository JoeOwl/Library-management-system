import tkinter
import customtkinter
from AddBook import *
from EditBook import *
from DeleteBook import *
from SearchBook import *
from ViewBooks import *
from IssueBook import *
from ReturnBook import *
from BookReport import *
from Miscellaneous import *
import json
from tkinter import filedialog
from tkinter.messagebox import askokcancel, showinfo, showerror
import os
import sys
import requests

def get_executable_directory():
    # Get the directory of the executable (or script during development)
    if getattr(sys, 'frozen', False):  # Check if the program is frozen (packaged as .exe)
        return os.path.dirname(sys.executable)  # Path to the .exe
    else:
        return os.path.dirname(os.path.abspath(__file__))  # Path to the script during development

# Get the directory where the .exe is located
executable_directory = get_executable_directory()

# Construct the full path to the settings.json file
settings_file_path = os.path.join(executable_directory, 'settings.json')
with open(settings_file_path, "r") as settings_file:
    settings = json.load(settings_file)

customtkinter.set_appearance_mode(settings["theme"])
customtkinter.set_default_color_theme(settings["color_theme"])

class Setting(customtkinter.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Library Management System")
        self.minsize(300,450)
        self.maxsize(300,450)
        self.geometry('300x450')
        
        self.main_frame = customtkinter.CTkFrame(master=self,corner_radius=10)
        self.main_frame.pack(padx=10,pady=10, ipadx=5, ipady=5,fill="both",expand=True)
        
        label = customtkinter.CTkLabel(master=self.main_frame, text="Settings",font=customtkinter.CTkFont(family="Robot", size=20, weight="bold"))
        label.grid(column=1,row=0,ipady=10)
        
        theme_lbel = customtkinter.CTkLabel(master=self.main_frame,text="Theme")
        theme_lbel.grid(column=1,row=1,padx=5, pady=5,sticky='w')
        
        self.theme_combo = customtkinter.CTkOptionMenu(self.main_frame, values=["Light", "Dark", "System"],command=self.change_theme)
        self.theme_combo.grid(column=2,row=1,padx=5, pady=5,sticky='e')
        self.theme_combo.set(settings["theme"])
        
        color_theme_lbel = customtkinter.CTkLabel(master=self.main_frame,text="Color Theme")
        color_theme_lbel.grid(column=1,row=2,padx=5, pady=5,sticky='w')
        
        self.color_theme_combo = customtkinter.CTkOptionMenu(self.main_frame, values=["blue", "dark-blue", "green"],command=self.change_theme_color)
        self.color_theme_combo.grid(column=2,row=2,padx=5, pady=5,sticky='e')
        self.color_theme_combo.set(settings["color_theme"])
        
        issue_duration_lbel = customtkinter.CTkLabel(master=self.main_frame,text="Issue Book Duration")
        issue_duration_lbel.grid(column=1,row=3,padx=5, pady=5,sticky='w')
        
        self.issue_duration_inp = customtkinter.CTkEntry(master=self.main_frame)
        self.issue_duration_inp.grid(column=2,row=3,padx=5,pady=5,sticky='e')
        self.issue_duration_inp.insert(0,settings["issue_duration"])
        
        charge_per_day_lbel = customtkinter.CTkLabel(master=self.main_frame,text="Charge Per Day")
        charge_per_day_lbel.grid(column=1,row=4,padx=5, pady=5,sticky='w')
        
        self.charge_per_day_inp = customtkinter.CTkEntry(master=self.main_frame)
        self.charge_per_day_inp.grid(column=2,row=4,padx=5,pady=5,sticky='e')
        self.charge_per_day_inp.insert(0,settings["charge_per_day"])
        
        footer_txt = customtkinter.CTkLabel(master=self.main_frame,text="Footer Text")
        footer_txt.grid(column=1,row=5,padx=5, pady=5,sticky='w')
        
        self.footer_txt_inp = customtkinter.CTkEntry(master=self.main_frame)
        self.footer_txt_inp.grid(column=2,row=5,padx=5,pady=5,sticky='e')
        self.footer_txt_inp.insert(0,settings["footer_txt"])
        
        self.save_setting = customtkinter.CTkButton(master=self.main_frame, text="Save",command=self.save_settings)
        self.save_setting.grid(column=2,row=6,padx=5,pady=5)

        watermark = customtkinter.CTkLabel(master=self,text="Developed By Youssef Abdel Mohsen, Mohamed Hamdy, Mohamed Walid")
        watermark.pack(padx=10,pady=5, ipadx=5, ipady=5,fill="x",expand=True)
        
    def change_theme(self, new_theme_mode:str):
        settings["theme"] = new_theme_mode
        f = open("settings.json","w")
        json.dump(settings,f,indent=4)
        customtkinter.set_appearance_mode(new_theme_mode)
    
    def change_theme_color(self, new_theme_color:str):
        settings["color_theme"] = new_theme_color
        f = open("settings.json","w")
        json.dump(settings,f,indent=4)
        customtkinter.set_default_color_theme(new_theme_color)
    
    def change_issue_duration(self, issue_dur):
        settings["issue_duration"] = issue_dur
        f = open("settings.json","w")
        json.dump(settings,f,indent=4)
    
    def change_charge_per_day(self, per_day_charge):
        settings["charge_per_day"] = per_day_charge
        f = open("settings.json","w")
        json.dump(settings,f,indent=4)
    
    def change_footer_txt(self, txt):
        settings["footer_txt"] = txt
        f = open("settings.json","w")
        json.dump(settings,f,indent=4)
    
    def save_settings(self):
        issue_dur = self.issue_duration_inp.get()
        charge_per_day = self.charge_per_day_inp.get()
        footer_txt = self.footer_txt_inp.get()
        
        if issue_dur != None and charge_per_day != None and footer_txt != None:
            self.change_issue_duration(int(issue_dur))
            self.change_charge_per_day(int(charge_per_day))
            self.change_footer_txt(str(footer_txt))
            showinfo(title="Saved",message="Settings saved successfully! Note default color theme changes works after restart.")
        else:
            showerror(title="Empty",message="Settings shouldn't be empty!")

class LMSApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.minsize(600,500)
        self.maxsize(600,500)
        self.geometry('600x430')
        
        # Initialize LMS database instance (db)
        executable_directory = get_executable_directory()
        self.db = LMS(os.path.join(executable_directory, "lms.db"))  # Initialize db here
        
        heading_frame = customtkinter.CTkFrame(master=self, corner_radius=10)
        heading_frame.pack(padx=10,pady=10, ipadx=20, ipady=5, fill="x", anchor="n")
        
        label = customtkinter.CTkLabel(master=heading_frame, text="Library Management System", font=customtkinter.CTkFont(family="Robot", size=25, weight="bold"))
        label.pack(ipady=10)
        
        main_frame = customtkinter.CTkFrame(master=self,corner_radius=10,fg_color='transparent')
        main_frame.pack(padx=10,pady=10, ipadx=5, ipady=5,fill="both",expand=True)
        
        
        left_frame = customtkinter.CTkFrame(master=main_frame,corner_radius=10)
        left_frame.pack(padx=10,pady=10, ipadx=5, ipady=5,fill="both",expand=True,side="left")
        
        right_frame = customtkinter.CTkFrame(master=main_frame,corner_radius=10)
        right_frame.pack(padx=10,pady=10, ipadx=5, ipady=5,fill="both",expand=True,side="right")
        
        button_1 = customtkinter.CTkButton(master=left_frame,text="Add new Book",corner_radius=3, command=self.add_book_win)
        button_1.pack(padx=20, pady=10)
        
        button_2 = customtkinter.CTkButton(master=left_frame,text="Delete Book",corner_radius=3, command=self.delete_book_win)
        button_2.pack(padx=20, pady=10)
        
        button_3 = customtkinter.CTkButton(master=left_frame,text="Book List",corner_radius=3, command=self.view_book_win)
        button_3.pack(padx=20, pady=10)
        
        button_4 = customtkinter.CTkButton(master=right_frame,text="Issue Book",corner_radius=3, command=self.issue_book_win)
        button_4.pack(padx=20, pady=10)
        
        button_5 = customtkinter.CTkButton(master=right_frame,text="Return Book",corner_radius=3, command=self.return_book_win)
        button_5.pack(padx=20, pady=10)
        
        button_6 = customtkinter.CTkButton(master=right_frame,text="Report",corner_radius=3, command=self.book_report_win)
        button_6.pack(padx=20, pady=10)
        
        button_7 = customtkinter.CTkButton(master=right_frame,text="Miscellaneous",corner_radius=3, command=self.miscellaneous_case_win)
        button_7.pack(padx=20, pady=10)
        
        button_8 = customtkinter.CTkButton(master=left_frame,text="Edit Book",corner_radius=3, command=self.edit_book_win)
        button_8.pack(padx=20, pady=10)
        
        button_9 = customtkinter.CTkButton(master=left_frame,text="Setting",corner_radius=3,fg_color='#cc0a0a',command=self.settings_win)
        button_9.pack(padx=20, pady=10)
        
        button_10 = customtkinter.CTkButton(master=right_frame,text="Import Student",corner_radius=3,command=self.import_student)
        button_10.pack(padx=20, pady=10)

        button_11 = customtkinter.CTkButton(master=left_frame, text="Search Book", corner_radius=3, command=self.search_book_win)
        button_11.pack(padx=20, pady=10)

        button_12 = customtkinter.CTkButton(master=right_frame, text="Retrieve Book by ISBN", corner_radius=3, command=self.retrieve_book_by_isbn)
        button_12.pack(padx=20, pady=10)
        
        footer_frame = customtkinter.CTkFrame(master=self,corner_radius=8,fg_color="#f55d5d")
        footer_frame.pack(padx=20,pady=10,fill="x",anchor="s")
        dev_by_label = customtkinter.CTkLabel(master=footer_frame,text=settings["footer_txt"],bg_color="#f55d5d")
        dev_by_label.pack()

        watermark = customtkinter.CTkLabel(master=self,text="Developed By Youssef Abdel Mohsen, Mohamed Hamdy, Mohamed Walid")
        watermark.place(relx = 0.3, rely = 0.9, anchor = 'sw')

    def add_book_win(self):
        app = AddBook(self)
        app.focus()
    
    def edit_book_win(self):
        app = EditBook(self)
        app.focus()
    
    def delete_book_win(self):
        app = DeleteBook(self)
        app.focus()
    
    def view_book_win(self):
        app = ViewBooks(self)
        app.focus()
    
    def issue_book_win(self):
        app = IssueBook(self)
        app.focus()
    
    def return_book_win(self):
        app = ReturnBook(self)
        app.focus()
    
    def book_report_win(self):
        app = BookReport(self)
        app.focus()
    
    def miscellaneous_case_win(self):
        app = Miscellaneous(self)
        app.focus()
    
    def settings_win(self):
        app = Setting(self)
        app.focus()

    def search_book_win(self):
        app = SearchBook(self, db=self.db) 
        app.focus()
    
    def import_student(self):
        try:
            filetypes = (
                ('excel files', '*.xlsx'),
            )
            file = filedialog.askopenfilename(title="Import Students",filetypes=filetypes)
            res = db.add_new_student(file)
            if res != None:
                showinfo(title="Success",message="Students imported successfully")
            else:
                showerror(title="Error",message="Something went wrong. Try Again!")
        except:
            showerror(title="Error",message="File is not in correct form or file not selected")

    def retrieve_book_by_isbn(self):
        # Prompt user for ISBN
        isbn_window = customtkinter.CTkToplevel(self)
        isbn_window.title("Retrieve Book by ISBN")
        isbn_window.geometry("400x200")

        isbn_label = customtkinter.CTkLabel(isbn_window, text="Enter ISBN:")
        isbn_label.pack(pady=10)
        
        isbn_entry = customtkinter.CTkEntry(isbn_window, width=300)
        isbn_entry.pack(pady=5)
        
        def fetch_book_info():
            isbn = isbn_entry.get().strip()
            if not isbn:
                showerror("Error", "ISBN cannot be empty!")
                return

            try:
                api_url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
                response = requests.get(api_url)
                if response.status_code == 200:
                    book_data = response.json()
                    if "items" in book_data:
                        book_info = book_data["items"][0]["volumeInfo"]
                        book_title = book_info.get("title", "Unknown Title")
                        book_authors = ", ".join(book_info.get("authors", ["Unknown Author"]))
                        book_publisher = book_info.get("publisher", "Unknown Publisher")
                        book_description = book_info.get("description", "No description available.")
                        
                        showinfo("Book Retrieved", f"Title: {book_title}\n"
                                                   f"Author(s): {book_authors}\n"
                                                   f"Publisher: {book_publisher}\n"
                                                   f"Description: {book_description}")
                    else:
                        showerror("Error", "No book found with this ISBN.")
                else:
                    showerror("Error", f"Failed to fetch data. HTTP Status Code: {response.status_code}")
            except Exception as e:
                showerror("Error", f"An error occurred while retrieving the book: {e}")
        
        fetch_button = customtkinter.CTkButton(isbn_window, text="Fetch Book Info", command=fetch_book_info)
        fetch_button.pack(pady=10)

if __name__ == '__main__':
    app = LMSApp()
    app.mainloop()
