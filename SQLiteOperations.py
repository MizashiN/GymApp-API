import sqlite3


class Operations:
    def _init_(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
    

    def SelectUrlProduct(self, id_product):
        self.cursor.execute(
            "SELECT urlproduct FROM urlsproducts WHERE id_product = ?",(id_product)
        )
        
        result = self.cursor.fetchone()
        
        return result    

    def SelectConfigBrand(self):
        config = {}
        self.cursor.execute(
            """
            SELECT

            parent_tag, title_tag, img_tag, price_tag, url_tag,
            url_attribute, url_base, url_class, price_parent_tag,
            price_parent_class, price_code, price_integer, price_decimal,
            price_fraction, img_attribute, parent_class, title_class,
            price_class, img_class, alt_price_parent_tag,
            alt_price_parent_class, alt_img_tag, alt_img_class,
            alt_parent_class_2, alt_img_tag_2, alt_img_class_2,
            alt_parent_tag_2, alt_parent_tag, alt_parent_class

            FROM configBrands
            """,
        )
        
        config = self.cursor.fetchall()
        
        return config

    
    def SelectUrlsBrands(self, category, subcategory=""):
        urls = []

        if not subcategory:
            self.cursor.execute(
                "SELECT url FROM urlsbrands WHERE id_category = ?",(category)
            )
        else:
            self.cursor.execute(
                "SELECT url FROM urlsbrands WHERE id_category = ? AND id_subcategory = ?",(category, subcategory)
            )
        
        urls = self.cursor.fetchall()
        
        return urls

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
            """SELECT p.title_product, p.price_product, p.url_product, i.image_src, i.id_image
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
    
    def InsertProduct(self, title, price, image_src, url_product ,image_blob):
        self.cursor.execute(
            "INSERT INTO images (image_src, image_blob) VALUES (?, ?)", (image_src, image_blob)
        )
                
        self.cursor.execute(
            "INSERT INTO products (title_product, price_product, url_product, id_image) SELECT ?, ?, ?, id_image FROM images WHERE image_src = ?", (title, price, image_src, url_product)
        )  

        self.conn.commit()
    

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
