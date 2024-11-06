import mysql.connector
from mysql.connector import Error

class Operations:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.host = "gym-app.mysql.uhserver.com"
        self.username = "parafalpwladmin"
        self.password = "@D3adlift"
        self.database = "gym_app"
        self.connect()

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database,
            )
            if self.conn.is_connected():
                # Cria um cursor buffered
                self.cursor = self.conn.cursor(buffered=True)
            else:
                print("Failed to connect to the database.")
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")

    def SelectCategories(self):
        if self.conn is None or not self.conn.is_connected():
            self.connect()
        categories = []
        self.cursor.execute(
            "SELECT * FROM categories",
        )
        
        categories = self.cursor.fetchall() 
        
        return categories

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()