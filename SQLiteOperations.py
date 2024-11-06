import sqlite3


class Operations:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

    def verify_images(self, src_list):
        self.list = src_list.copy()
        images_to_remove = []

        for image_src in src_list:
            self.cursor.execute(
                "SELECT image_src FROM images WHERE image_src = %s", (image_src,)
            )
            result = self.cursor.fetchone()
            if result:
                images_to_remove.append(image_src)

        for image in images_to_remove:
            self.list.remove(image)
        return self.list

    def SelectCategories(self):
        categories = []
        self.cursor.execute(
            "SELECT * FROM categories",
        )
        
        categories = self.cursor.fetchall() 
        
        self.close()
        return categories

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
