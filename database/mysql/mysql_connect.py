import mysql.connector
from config.database_config import get_database_config
from pathlib import Path
from database.mysql.sql_manager import create_mysql_database, execute_sql_file
from mysql.connector import Error

class MysqlConnect:
    # get mysql config
    def __init__(self, config):
        self.config = config
        self.connection = None
        self.cursor = None

    # connect mysql
    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor()
            print("----------Connected to MySQL----------")
        except Error as e:
            raise Exception("----------Failed to connect MySQL----------", e) from e

    # disconnect mysql
    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("----------Disconnected from MySQL----------")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
