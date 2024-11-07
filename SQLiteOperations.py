import sqlite3


class Operations:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        
    def SelectCategories(self):
        categories = []
        self.cursor.execute(
            "SELECT * FROM categories",
        )
        
        categories = self.cursor.fetchall()
        
        return categories
        

    def verify_images(self, src_list):
        self.list = src_list.copy()
        images_to_remove = []

        for image_src in src_list:
            self.cursor.execute(
                "SELECT image_src FROM images WHERE image_src = ?", (image_src,)
            )
            result = self.cursor.fetchone()
            if result:
                images_to_remove.append(image_src)

        for image in images_to_remove:
            self.list.remove(image)
        return self.list
    
    def SelectProduct(self, image_src):
        product_b = []
        self.cursor.execute(
            """SELECT p.title_product, p.price_product, i.image_src, i.id_image
            FROM products p
            JOIN images i ON p.id_image = i.id_image
            WHERE i.image_src = ?;
            """, (image_src,)
        )
        product_b = self.cursor.fetchall()

        return product_b
    
    def UpdateProduct(self, column, value_r, id_image):
        query = f"UPDATE products SET {column} = ? WHERE id_image = ?"
        self.cursor.execute(query, (value_r, id_image))

        self.conn.commit()
    
    def InsertProduct(self, title, price, image_src, image_blob):
        self.cursor.execute(
            "INSERT INTO images (image_src, image_blob) VALUES (?, ?)", (image_src, image_blob)
        )
                
        self.cursor.execute(
            "INSERT INTO products (title_product, price_product, id_image) SELECT ?, ?, id_image FROM images WHERE image_src = ?", (title, price, image_src)
        )  

        self.conn.commit()
    

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
