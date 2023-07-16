import pyodbc
import sqlite3


class Database:
    def __init__(self):
        # self.server = server
        self.connection = None
        self.cursor = None
        print('Connecting to SQLITE3....')

    def connect(self):
        try:
             #pyodbc.connect(f'DRIVER=ODBC Driver 17 for SQL Server;\
             #SERVER={self.server};DATABASE=Training;Trusted_Connection=yes;')
            self.connection = sqlite3.connect("bartimaeus-db.sql")
            self.cursor = self.connection.cursor()
            print("Connected to the database successfully.")
        except sqlite3.Error as error:
            print("Error connecting to the database:", error)

    def create_table(self, table_name, columns):
        try:
            self.cursor.execute(f'drop table if exists {table_name};')
            create_table_query = f"CREATE TABLE if not exists {table_name} ({columns});"
            self.cursor.execute(create_table_query)
            self.connection.commit()
            print(f"Table '{table_name}' created successfully.")
        except sqlite3.Error as error:
            print("Error creating table:", error)

    def insert_data(self, table_name, data):
        try:
            if table_name == 'bartimaeusContactList':
                insert_query = f"INSERT INTO {table_name}(name,email) VALUES ({data});"
                self.cursor.execute(insert_query)
                self.connection.commit()
                print("Data inserted successfully.")
                return 1
            elif table_name == 'bartimaeusEmailHistory':
                insert_query = f"INSERT INTO {table_name}(email,name,email_subject,email_message,send_status) VALUES ({data});"
                self.cursor.execute(insert_query)
                self.connection.commit()
                print("Data inserted successfully.")
                return 1
        except sqlite3.Error as error:
            print("Error inserting data:", error)
            return 0

    def read_data(self, table_name):
        try:
            select_query = f"SELECT * FROM {table_name}"
            self.cursor.execute(select_query)
            rows = self.cursor.fetchall()
            print(f"Data from table '{table_name}':")
            for row in rows:
                print(row)
        except sqlite3.Error as error:
            print("Error reading data:", error)

    def read_data_with_name(self, name, table_name):
        try:
            select_query = f"SELECT * FROM {table_name} WHERE Name = '{name}'"
            self.cursor.execute(select_query)
            rows = self.cursor.fetchall()
            print(f"Data from table '{table_name}':")
            for row in rows:
                print(row)
        except sqlite3.Error as error:
            print("Error reading data:", error)

    def read_email(self,name,table_name):
        try:
            select_query = f"SELECT email FROM {table_name} WHERE Name = '{name.title()}';"
            self.cursor.execute(select_query)
            rows = self.cursor.fetchall()
            if rows:
                for row in rows:
                    return row
            else :
                return None 
        except sqlite3.Error as error:
            print("Error reading data:", error)

    def read_email_history(self,name,table_name):
        try:
            select_query = f"SELECT * FROM {table_name} WHERE Name = '{name.title()}' order by send_time desc limit 1;"
            self.cursor.execute(select_query)
            rows = self.cursor.fetchall()
            if rows:
                for row in rows:
                    return row
            else :
                return f'You have not sent an email to {name} before. I\'m sure {name} will be happy to hear from you'
        except sqlite3.Error as error:
            print("Error reading data:", error)

    def delete_data(self, table_name, condition):
        try:
            delete_query = f"DELETE FROM {table_name} WHERE {condition}"
            self.cursor.execute(delete_query)
            self.connection.commit()
            print("Data deleted successfully.")
        except sqlite3.Error as error:
            print("Error deleting data:", error)

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Disconnected from the database")





'''
# # Example usage
# db = Database("ISW-220521-608\SQLEXPRESS")

# db.connect()

# db.create_table("bartimaeus-table.sql", "id INTEGER PRIMARY KEY, name varchar(25), email varchar(45)")
# db.create_table("bartimaeus-email-history.sql", "id INTEGER PRIMARY KEY, email varchar(45), name varchar(25), message varchar(200), send_time datetime default current_timestamp")


# db.insert_data("bartimaeus-table.sql", "1, 'Tayo', 'tayo@gmail.com'")
# db.insert_data("bartimaeus-table.sql", "2, 'Nana', 'omma@gmail.com'")
# db.insert_data("bartimaeus-table.sql", "3, 'Uyoz', 'uyoz@gmail.com'")
# db.insert_data("bartimaeus-table.sql", "4, 'Taga', 'outofoffice@gmail.com'")
# db.insert_data("bartimaeus-table.sql", "5, 'John', 'ade@gmail.com'")
# db.insert_data("bartimaeus-table.sql", "6, 'Ifa', 'fk@gmail.com'")

# db.read_data("bartimaeus-table.sql")

# db.delete_data("bartimaeus-table.sql", "id = 5")

# db.read_data("bartimaeus-table.sql")

# db.read_data_with_name("Tayo", "bartimaeus-table.sql")

# db.disconnect()
'''