"""
Description: 
Author: Xiaohan Liu
Assistant: Mandeep Kaur, Doanh Chung
Date: 2024 - 11 - 12
Usage: A context manager class for managing database connections. This class opens a connection to the specified SQLite database, provides a cursor 
for executing SQL commands, and ensures that all changes are committed and the connection is properly closed after the operations are completed.
"""
import sqlite3

class DBCM:
    
    def __init__(self, db_name):
        """
        Initializes the DBCM context manager with the database name.
        
        Parameters:
            db_name (str): The name of the SQLite database file.
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """
        Enters the runtime context for database operations.
        
        Opens a connection to the SQLite database and creates a cursor object.
        
        Returns:
            sqlite3.Cursor: A cursor object for executing SQL commands.
        """
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor  

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
        Exits the runtime context, ensuring database connection is properly closed.
        
        If no exceptions occurred, commits the transaction. Closes both the cursor 
        and connection regardless of whether an exception was raised.
        
        Parameters:
            exc_type (type): The exception type, if an exception was raised.
            exc_value (Exception): The exception instance, if an exception was raised.
            exc_traceback (traceback): The traceback object, if an exception was raised.
        """
        if exc_type is None:
            self.conn.commit()
        
        self.cursor.close()
        self.conn.close()
