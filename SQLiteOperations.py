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
                database=self.database
            )
            if self.conn.is_connected():
                self.cursor = self.conn.cursor()
            else:
                print("Failed to connect to the database.")
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")

    def verify_images(self, src_list):
        if self.conn is None or not self.conn.is_connected():
            self.connect()

        # Cria um cursor buffered
        with self.conn.cursor(buffered=True) as cursor:
            self.list = src_list.copy()
            images_to_remove = []

            for image_src in src_list:
                cursor.execute(
                    "SELECT image_src FROM images WHERE image_src = %s", (image_src,)
                )
                result = cursor.fetchone()
                if result:
                    images_to_remove.append(image_src)

            # Remove imagens que existem no banco de dados
            for image in images_to_remove:
                self.list.remove(image)

        return self.list

    def insert_img(self, image_src, image_blob):
        if self.conn is None or not self.conn.is_connected():
            self.connect()
        try:
            self.cursor.execute(
                "INSERT INTO images (image_src, image_blob) VALUES (%s, %s)",
                (image_src, image_blob)
            )
            self.conn.commit()
        except mysql.connector.OperationalError as e:
            print(f"Operational error: {e}")
        except Error as e:
            print(f"Error: {e}")

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()