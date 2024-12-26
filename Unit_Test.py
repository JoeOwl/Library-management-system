#AddBook
import unittest
from unittest.mock import MagicMock, patch
from AddBook import AddBook 
import customtkinter

class TestAddBook(unittest.TestCase):

    def setUp(self):
        # Create a mock database object
        self.mock_db = MagicMock()
        
        # Patch the LMS class to return the mock database
        patcher = patch('add_book.LMS', return_value=self.mock_db)
        self.addCleanup(patcher.stop)
        self.mock_LMS = patcher.start()

        # Create an instance of the AddBook GUI
        self.root = customtkinter.CTk()
        self.add_book_gui = AddBook(master=self.root)

    def tearDown(self):
        # Destroy the GUI root after each test
        self.root.destroy()

    def test_save_new_book_success(self):
        # Mock valid inputs
        self.add_book_gui.book_id_input.insert(0, "123")
        self.add_book_gui.book_nme_input.insert(0, "Python Programming")
        self.add_book_gui.book_author_input.insert(0, "John Doe")
        self.add_book_gui.book_edition_input.insert(0, "3rd")
        self.add_book_gui.book_price_input.insert(0, "49.99")
        self.add_book_gui.purch_dt_var.set("2024-01-01")

        # Mock database response
        self.mock_db.add_new_book.return_value = True

        # Simulate button click
        with patch('tkinter.messagebox.showinfo') as mock_info:
            self.add_book_gui.save_new_book()
            
            # Check that the database method was called with the correct data
            self.mock_db.add_new_book.assert_called_once_with((
                "123", "Python Programming", "John Doe", "3rd", "49.99", "2024-01-01", "available"
            ))

            # Check that a success message was shown
            mock_info.assert_called_once_with(title="Saved", message="New book saved successfully.")

    def test_save_new_book_empty_fields(self):
        # Leave inputs empty
        with patch('tkinter.messagebox.showerror') as mock_error:
            self.add_book_gui.save_new_book()

            # Ensure the database method was never called
            self.mock_db.add_new_book.assert_not_called()

            # Check that an error message was shown
            mock_error.assert_called_once_with(title="Empty Fields", message="Please fill all the details then submit!")

    def test_save_new_book_db_error(self):
        # Mock valid inputs
        self.add_book_gui.book_id_input.insert(0, "123")
        self.add_book_gui.book_nme_input.insert(0, "Python Programming")
        self.add_book_gui.book_author_input.insert(0, "John Doe")
        self.add_book_gui.book_edition_input.insert(0, "3rd")
        self.add_book_gui.book_price_input.insert(0, "49.99")
        self.add_book_gui.purch_dt_var.set("2024-01-01")

        # Mock database response to simulate an error
        self.mock_db.add_new_book.return_value = None

        # Simulate button click
        with patch('tkinter.messagebox.showerror') as mock_error:
            self.add_book_gui.save_new_book()

            # Ensure the database method was called
            self.mock_db.add_new_book.assert_called_once()

            # Check that an error message was shown
            mock_error.assert_called_once_with(title="Not Saved", message="Something went wrong. Please try again...")

if __name__ == '__main__':
    unittest.main(exit=False)


#API Integration with Flask
import unittest
from unittest.mock import patch, MagicMock
from API import RetrieveBook  
import customtkinter
import requests

class TestRetrieveBook(unittest.TestCase):

    def setUp(self):
        # Create an instance of the RetrieveBook GUI
        self.root = customtkinter.CTk()
        self.retrieve_book_gui = RetrieveBook(master=self.root)

    def tearDown(self):
        # Destroy the GUI root after each test
        self.root.destroy()

    @patch('requests.get')
    def test_retrieve_book_details_success(self, mock_get):
        # Mock the API response for a valid ISBN
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "volumeInfo": {
                        "title": "Test Book",
                        "authors": ["Author One", "Author Two"],
                        "publishedDate": "2020-01-01",
                        "description": "A test book description."
                    }
                }
            ]
        }
        mock_get.return_value = mock_response

        # Simulate user input
        self.retrieve_book_gui.isbn_input.insert(0, "1234567890")

        # Simulate button click
        with patch('tkinter.messagebox.showinfo') as mock_info:
            self.retrieve_book_gui.retrieve_book_details()

            # Verify API call
            mock_get.assert_called_once_with("https://www.googleapis.com/books/v1/volumes?q=isbn:1234567890")

            # Verify GUI output
            expected_output = (
                "Title: Test Book\n"
                "Authors: Author One, Author Two\n"
                "Published Date: 2020-01-01\n"
                "Description: A test book description."
            )
            self.assertEqual(self.retrieve_book_gui.output_label.cget("text"), expected_output)

            # Verify success message
            mock_info.assert_called_once_with(title="Book Found", message="Book details retrieved successfully.")

    @patch('requests.get')
    def test_retrieve_book_details_not_found(self, mock_get):
        # Mock the API response for an invalid ISBN
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        mock_get.return_value = mock_response

        # Simulate user input
        self.retrieve_book_gui.isbn_input.insert(0, "0000000000")

        # Simulate button click
        with patch('tkinter.messagebox.showerror') as mock_error:
            self.retrieve_book_gui.retrieve_book_details()

            # Verify API call
            mock_get.assert_called_once_with("https://www.googleapis.com/books/v1/volumes?q=isbn:0000000000")

            # Verify GUI output
            self.assertEqual(self.retrieve_book_gui.output_label.cget("text"), "")

            # Verify error message
            mock_error.assert_called_once_with(title="Not Found", message="No book found with the provided ISBN ID.")

    @patch('requests.get')
    def test_retrieve_book_details_api_error(self, mock_get):
        # Mock an API error response
        mock_get.side_effect = requests.RequestException("API error")

        # Simulate user input
        self.retrieve_book_gui.isbn_input.insert(0, "1234567890")

        # Simulate button click
        with patch('tkinter.messagebox.showerror') as mock_error:
            self.retrieve_book_gui.retrieve_book_details()

            # Verify API call
            mock_get.assert_called_once_with("https://www.googleapis.com/books/v1/volumes?q=isbn:1234567890")

            # Verify GUI output
            self.assertEqual(self.retrieve_book_gui.output_label.cget("text"), "")

            # Verify error message
            mock_error.assert_called_once_with(title="Error", message="An error occurred while fetching data: API error")

    def test_retrieve_book_details_empty_field(self):
        # Simulate empty input
        with patch('tkinter.messagebox.showerror') as mock_error:
            self.retrieve_book_gui.retrieve_book_details()

            # Verify no API call was made
            self.assertEqual(mock_error.call_count, 1)

            # Verify error message
            mock_error.assert_called_once_with(title="Empty Field", message="Please enter an ISBN ID to search.")

if __name__ == '__main__':
    unittest.main(exit=False)


#BookReport
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from BookReport import BookReport  # Replace with the actual module name

class TestBookReport(unittest.TestCase):

    def setUp(self):
        # Initialize the BookReport instance for testing
        self.book_report = BookReport()

    @patch('your_module.db.all_available_book')
    @patch('your_module.filedialog.askdirectory', return_value='/fake/dir')
    @patch('your_module.pd.DataFrame.to_excel')
    def test_export_available_book(self, mock_to_excel, mock_askdirectory, mock_all_available_book):
        # Mock the database query response
        mock_all_available_book.return_value = ("SELECT * FROM available_books", MagicMock())
        pd.read_sql_query = MagicMock(return_value=pd.DataFrame())

        # Run the method
        self.book_report.export_available_book()

        # Assert file dialog and to_excel are called
        mock_askdirectory.assert_called_once()
        mock_to_excel.assert_called_once_with('/fake/dir/available_books.xlsx')

    @patch('your_module.db.all_issued_book')
    @patch('your_module.filedialog.askdirectory', return_value='/fake/dir')
    @patch('your_module.pd.DataFrame.to_excel')
    def test_export_issued_book(self, mock_to_excel, mock_askdirectory, mock_all_issued_book):
        mock_all_issued_book.return_value = ("SELECT * FROM issued_books", MagicMock())
        pd.read_sql_query = MagicMock(return_value=pd.DataFrame())

        self.book_report.export_issued_book()

        mock_askdirectory.assert_called_once()
        mock_to_excel.assert_called_once_with('/fake/dir/issued_books.xlsx')

    @patch('your_module.db.all_books')
    @patch('your_module.filedialog.askdirectory', return_value='/fake/dir')
    @patch('your_module.pd.DataFrame.to_excel')
    def test_export_all_book(self, mock_to_excel, mock_askdirectory, mock_all_books):
        mock_all_books.return_value = ("SELECT * FROM all_books", MagicMock())
        pd.read_sql_query = MagicMock(return_value=pd.DataFrame())

        self.book_report.export_all_book()

        mock_askdirectory.assert_called_once()
        mock_to_excel.assert_called_once_with('/fake/dir/all_books.xlsx')

    @patch('your_module.db.fine_detail')
    @patch('your_module.filedialog.askdirectory', return_value='/fake/dir')
    @patch('your_module.pd.DataFrame.to_excel')
    def test_export_fine_detail(self, mock_to_excel, mock_askdirectory, mock_fine_detail):
        mock_fine_detail.return_value = ("SELECT * FROM fine_details", MagicMock())
        pd.read_sql_query = MagicMock(return_value=pd.DataFrame())

        self.book_report.export_fine_detail()

        mock_askdirectory.assert_called_once()
        mock_to_excel.assert_called_once_with('/fake/dir/fine_details.xlsx')

if __name__ == '__main__':
    unittest.main(exit=False)


#database
import unittest
import sqlite3
import os
from database import LMS

class TestLMS(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create an in-memory SQLite database for testing
        cls.test_db = LMS(':memory:')
        cls.conn = cls.test_db.conn
        cls.cur = cls.test_db.cur

        # Create tables for testing
        cls.cur.executescript('''
        CREATE TABLE books (
            book_id TEXT PRIMARY KEY,
            book_name TEXT,
            book_author TEXT,
            book_edition TEXT,
            book_price REAL,
            date_of_purchase TEXT,
            status TEXT
        );
        CREATE TABLE student (
            id TEXT PRIMARY KEY,
            name TEXT,
            class TEXT
        );
        CREATE TABLE issued_book (
            book_id TEXT,
            issued_to TEXT,
            issued_on TEXT,
            expired_on TEXT,
            is_miscellaneous INTEGER DEFAULT 0
        );
        CREATE TABLE fine_details (
            book_id TEXT,
            student_id TEXT,
            issued_on TEXT,
            returned_date TEXT,
            total_fine REAL,
            no_of_day INTEGER
        );
        ''')

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def setUp(self):
        # Clean tables before each test
        self.cur.execute("DELETE FROM books;")
        self.cur.execute("DELETE FROM student;")
        self.cur.execute("DELETE FROM issued_book;")
        self.cur.execute("DELETE FROM fine_details;")
        self.conn.commit()

    def test_add_new_book(self):
        book_data = ('B001', 'Python Basics', 'John Doe', '1st', 29.99, '2023-01-01', 'available')
        book_id = self.test_db.add_new_book(book_data)
        self.cur.execute("SELECT * FROM books WHERE book_id = ?", (book_id,))
        result = self.cur.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 'B001')

    def test_delete_book(self):
        book_data = ('B002', 'Advanced Python', 'Jane Doe', '2nd', 39.99, '2023-01-02', 'available')
        self.test_db.add_new_book(book_data)
        result = self.test_db.delete_book('B002')
        self.assertEqual(result, 'deleted')
        self.cur.execute("SELECT * FROM books WHERE book_id = 'B002'")
        self.assertIsNone(self.cur.fetchone())

    def test_view_book_list(self):
        books = [
            ('B003', 'Data Science 101', 'Alice', '1st', 49.99, '2023-01-03', 'available'),
            ('B004', 'Machine Learning', 'Bob', '3rd', 59.99, '2023-01-04', 'issued')
        ]
        for book in books:
            self.test_db.add_new_book(book)
        result = self.test_db.view_book_list()
        self.assertEqual(len(result), 2)

    def test_issue_book(self):
        book_data = ('B005', 'Deep Learning', 'Eve', '1st', 79.99, '2023-01-05', 'available')
        self.test_db.add_new_book(book_data)
        issue_data = ('B005', 'S001', '2023-01-10', '2023-01-20')
        issue_id = self.test_db.issue_book(issue_data)
        self.cur.execute("SELECT * FROM issued_book WHERE book_id = 'B005'")
        result = self.cur.fetchone()
        self.assertIsNotNone(result)

    def test_return_book(self):
        book_data = ('B006', 'AI Basics', 'Trent', '2nd', 69.99, '2023-01-06', 'issued')
        self.test_db.add_new_book(book_data)
        issue_data = ('B006', 'S002', '2023-01-11', '2023-01-21')
        self.test_db.issue_book(issue_data)
        result = self.test_db.return_book('B006')
        self.assertEqual(result, 'returned')
        self.cur.execute("SELECT * FROM issued_book WHERE book_id = 'B006'")
        self.assertIsNone(self.cur.fetchone())

    def test_update_book_status(self):
        book_data = ('B007', 'Cyber Security', 'Mallory', '3rd', 89.99, '2023-01-07', 'available')
        self.test_db.add_new_book(book_data)
        self.test_db.update_book_status('B007', 'issued')
        self.cur.execute("SELECT status FROM books WHERE book_id = 'B007'")
        result = self.cur.fetchone()
        self.assertEqual(result[0], 'issued')

if __name__ == '__main__':
    unittest.main(exit=False)


