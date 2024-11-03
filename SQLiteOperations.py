import sqlite3


class Operations:
    def __init__(self):
        self.conn = sqlite3.connect("Poha da Database.db")
        self.cursor = self.conn.cursor()
        self.list = []

    def VerifyImages(self, src_list):
        self.list = src_list.copy()
        for img_src in src_list:
            self.cursor.execute(
                "SELECT image_src FROM images WHERE image_src = :image_src",
                {"image_src": img_src},
            )
            result = self.cursor.fetchone()
            if result:
                self.list.remove(img_src)

        return self.list

    def close(self):
        self.conn.close()
