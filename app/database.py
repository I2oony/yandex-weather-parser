import sqlite3

class Database:
    def __init__(self, path_to_db):
        self.db_name = "parser"
        self.table_name = "logs"
        self.connection = sqlite3.connect(f"{path_to_db}/{self.db_name}.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name}(search_query, datetime, result, traceback)")
        return
    
    def save_log(self, search_query, datetime, result, traceback):
        self.cursor.execute(f"INSERT INTO {self.table_name} VALUES ('{search_query}', '{datetime}', '{result}', '{traceback}')")
        self.connection.commit()
