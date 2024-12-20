import sqlite3
import openpyxl


class LMS:
    #Establishes a connection to the SQLite database and creates a cursor object for executing SQL queries.
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
    
    def add_new_book(self, data):
        """
        Add a new book into the books table
        :param self:
        :param data: list with book details
        :return: book id
        """
        sql = '''INSERT INTO books(book_id,book_name,book_author,book_edition,book_price,date_of_purchase,status)
            VALUES(?,?,?,?,?,?,?)'''
        self.cur.execute(sql, data)
        self.conn.commit()
        return self.cur.lastrowid
    
    #Reads student data from an Excel file (xl_file) and inserts it into the student table.
    #Each row in the Excel file corresponds to a new student record.
    ''' ##Excel format
    
        id    |  name            | class
        -------------------------------------
        101   | Alice Johnson    | 10A
        102   | Bob Smith        | 11B
        103   | Charlie Brown    | 9C
    '''
    def add_new_student(self, xl_file):
        wb = openpyxl.load_workbook(xl_file)
        sheet = wb['Sheet1']
        for row in sheet.rows:
            dt = [cell.value for cell in row]
            sql = '''INSERT INTO student (id,name,class)
            VALUES(?,?,?) '''
            self.cur.execute(sql, dt)
        self.conn.commit()
        return self.cur.lastrowid
    
    
    def delete_book(self, book_id):
        """
        Delete a book by book id
        :param self:
        :param book_id: id of book
        :return error or deleted
        """
        try:
            sql = 'DELETE FROM books WHERE book_id=?'
            self.cur.execute(sql, (book_id,))
            self.conn.commit()
            return "deleted"
        except:
            return "error"
    
    def view_book_list(self):
        """
        Query all book rows in the books table, Fetches and returns all books with a status of either 'available' or 'issued'.
        :param self:
        :return: all book list
        """
        self.cur.execute("SELECT * FROM books WHERE status = ? or status = ?",('available','issued'))
        return self.cur.fetchall()
    
    def miscellaneous_books(self):
        #Fetches and returns all books with the status 'miscellaneous'.
        self.cur.execute("SELECT * FROM books WHERE status = 'miscellaneous'")
        return self.cur.fetchall()
    
    def view_issued_book(self,id):
        self.cur.execute("SELECT * FROM issued_book WHERE book_id = ? and is_miscellaneous = ?", (id,0))
        return self.cur.fetchone()
    
    def view_student(self,id):
        self.cur.execute("SELECT * FROM student WHERE id = ?", (id,))
        return self.cur.fetchone()
    
    def all_book_id(self):
        """
        Query all book id in the books table
        :param self:
        :return: all available book id list
        """
        self.cur.execute("SELECT book_id FROM books WHERE status = ? or status = ?", ('available','issued'))
        return self.cur.fetchall()
    
    def all_student_id(self):
        """
        Query all student id in the student table
        :param self:
        :return: all available student id list
        """
        self.cur.execute("SELECT id FROM student")
        return self.cur.fetchall()
    
    def issue_book(self,data):
        """
        Issue a new book into the issued_book table
        :param self:
        :param data: list with issue book details
        :return: book id
        """
        sql = '''INSERT INTO issued_book (book_id,issued_to,issued_on,expired_on)
            VALUES(?,?,?,?) '''
        self.cur.execute(sql, data)
        self.conn.commit()
        return self.cur.lastrowid
    
    def delete_issued_book(self):
        try:
            sql = 'DELETE FROM issued_book'
            self.cur.execute(sql)
            self.conn.commit()
            return "deleted"
        except:
            return "error"
    
    def all_issued_book_id(self):
        """
        Query all issued book id in the issued book table
        :param self:
        :return: all issued book id list
        """
        self.cur.execute("SELECT book_id FROM issued_book WHERE is_miscellaneous = ?",(0,))
        return self.cur.fetchall()
    
    def return_book(self,book_id):
        """
        Return the book which issued by id
        :param self:
        :param book_id: id of book
        :return error or returned
        """
        try:
            sql = 'DELETE FROM issued_book WHERE book_id=?'
            self.cur.execute(sql, (book_id,))
            self.conn.commit()
            return "returned"
        except:
            return "error"
    
    def update_book_status(self,book_id,status):
        """
        Updates the status of a book (e.g., from 'available' to 'issued').
        :param conn:
        :param book_id: id of book
        :param status: status of book
        :return:
        """
        sql = '''UPDATE books SET status = ? WHERE book_id = ?'''
        self.cur.execute(sql,(status,book_id,))
        self.conn.commit()
    
    def select_book_status(self,book_id):
        """
        Query book status by book_id
        :param self:
        :param book_id:
        :return: book status
        """
        self.cur.execute("SELECT status FROM books WHERE book_id=?", (book_id,))
        return self.cur.fetchone()
    
    def select_issued_book_det(self,book_id):
        self.cur.execute("SELECT * FROM issued_book WHERE book_id=?", (book_id,))
        return self.cur.fetchone()
    
    def select_book_detail(self,book_id):
        self.cur.execute("SELECT * FROM books WHERE book_id=?", (book_id,))
        return self.cur.fetchone()
    
    def all_available_book(self):
        sql="SELECT book_id, book_name, book_author, book_edition, book_price FROM books WHERE status = 'available'"
        return (sql,self.conn)
    
    def all_issued_book(self):
        sql="SELECT book_id, book_name, book_author, book_edition, book_price FROM books WHERE status = 'issued'"
        return (sql,self.conn)
    
    def all_books(self):
        """
        Retrieves all books that are either available or issued.
        Constructs a SQL query to select book details such as ID, name, author, edition, and price
        from the 'books' table where the book status is either 'available' or 'issued'.
        Returns the SQL query string and the database connection object.
        """
        sql = "SELECT book_id, book_name, book_author, book_edition, book_price FROM books WHERE status = 'available' or status = 'issued'"
        return (sql, self.conn)


    def fine_detail(self):
        """
        Retrieves all fine details from the 'fine_details' table.
        Constructs a SQL query to select all columns from the 'fine_details' table.
        Returns the SQL query string and the database connection object.
        """
        sql = "SELECT * FROM fine_details"
        return (sql, self.conn)


    def move_to_miscellaneous(self, id):
        """
        Marks a book as miscellaneous in the 'issued_book' table.
        Updates the 'is_miscellaneous' column to 1 for the specified book ID.
        Commits the change to the database.
        
        :param id: The ID of the book to be marked as miscellaneous.
        """
        sql = '''UPDATE issued_book SET is_miscellaneous = ? WHERE book_id = ?'''
        self.cur.execute(sql, (1, id,))
        self.conn.commit()


    def update_book_details(self, data):
        """
        Updates the details of an existing book in the 'books' table.
        Replaces the values for the book's ID, name, author, edition, price, and date of purchase
        with the new data provided.
        Commits the change to the database.
    
        :param data: A tuple containing the updated book details, including:
                     (book_id, book_name, book_author, book_edition, book_price, date_of_purchase, book_id).
        """
        sql = '''UPDATE books SET book_id = ?, book_name = ?, book_author = ?, book_edition = ?, book_price = ?, date_of_purchase = ? WHERE book_id = ?'''
        self.cur.execute(sql, data)
        self.conn.commit()

    
    def save_fine_detail(self, data):
        """
        Saves a fine record into the 'fine_details' table.
        Inserts details about a book fine, including book ID, student ID, issue date, return date,
        total fine amount, and the number of overdue days.
        Commits the change to the database and returns the ID of the newly inserted record.
    
        :param data: A tuple containing fine details, including:
                     (book_id, student_id, issued_on, returned_date, total_fine, no_of_day).
        :return: The ID of the newly inserted fine record.
        """
        sql = '''INSERT INTO fine_details(book_id, student_id, issued_on, returned_date, total_fine, no_of_day)
                  VALUES(?,?,?,?,?,?)'''
        self.cur.execute(sql, data)
        self.conn.commit()
        return self.cur.lastrowid