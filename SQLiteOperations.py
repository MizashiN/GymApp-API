import sqlite3


class Operations:
    def __init__(self):
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()
        self.list = []

    def VerifyImages(self, src_list):
        self.list = src_list.copy()
        for image_src in src_list:
            self.cursor.execute(
                "SELECT image_src FROM images WHERE image_src = :image_src",
                {"image_src": image_src},
            )
            result = self.cursor.fetchone()
            if result:
                self.list.remove(image_src)
            
        return self.list
    def InsertImg(self, image_src, image_blob):
        self.cursor.execute(
            "INSERT INTO IMAGES (image_src, image_blob) VALUES (:image_src, :image_blob)",
            {"image_src": image_src, "image_blob": image_blob}
        )
        self.conn.commit()  


    def close(self):
        self.conn.close()
