import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    #If the file doesn’t exist, SQLite will create a new one.
    try:
        conn = sqlite3.connect(db_file)
        return conn
    #If it fails to connect, it catches and prints the error.
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    #Create a SQLite database named lms.db
    database = "./lms.db"
    
    # SQL statements to create tables
    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS books (
                                        book_id integer PRIMARY KEY, #unique identifier for each book.
                                        book_name text NOT NULL,
                                        book_author text,
                                        book_edition text,
                                        book_price text,
                                        date_of_purchase DATETIME,
                                        status text
                                    ); """
    #Tracks which books have been issued to which students.
    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS issued_book (
                                    book_id integer,
                                    issued_to integer,
                                    issued_on DATETIME NOT NULL,
                                    expired_on DATETIME NOT NULL,
                                    is_miscellaneous integer DEFAULT 0 NOT NULL,
                                    FOREIGN KEY (book_id)
                                    REFERENCES books (book_id)
                                        ON UPDATE CASCADE
                                        ON DELETE CASCADE
                                    FOREIGN KEY (issued_to)
                                    REFERENCES student (id)
                                        ON UPDATE CASCADE
                                        ON DELETE CASCADE
                                );"""
    #ON UPDATE CASCADE: If the primary key in the referenced table (books or student) changes, the corresponding foreign key in issued_book will also update.
    #ON DELETE CASCADE: If a book or student record is deleted, related entries in issued_book are automatically deleted to maintain referential integrity.
    
    sql_create_tasks1_table = """CREATE TABLE IF NOT EXISTS student (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    class text NOT NULL
                                );"""
                                
    #EX:                                
    #book_id: 101
    #student_id: 5001
    #issued_on: 2024-11-01
    #returned_date: 2024-11-20
    #total_fine: 10
    #no_of_day: 5

    sql_create_tasks2_table = """CREATE TABLE IF NOT EXISTS fine_details (
                                    book_id integer,
                                    student_id integer,
                                    issued_on DATETIME NOT NULL,
                                    returned_date DATETIME NOT NULL,
                                    total_fine integer,
                                    no_of_day integer,
                                    FOREIGN KEY (book_id)
                                    REFERENCES books (book_id)
                                        ON UPDATE CASCADE
                                        ON DELETE CASCADE
                                    FOREIGN KEY (student_id)
                                    REFERENCES student (id)
                                        ON UPDATE CASCADE
                                        ON DELETE CASCADE
                                );"""
    
    
    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_projects_table)

        # create tasks table
        create_table(conn, sql_create_tasks_table)
        create_table(conn, sql_create_tasks1_table)
        create_table(conn, sql_create_tasks2_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()