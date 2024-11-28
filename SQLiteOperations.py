import sqlite3
from itertools import chain


class Operations:
    def __init__(self):
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()

    def SelectConfigCompany(self):

        configcompany = {}

        self.cursor.execute(
            """
            SELECT
                c.id_company, a.company, c.parent_tag, c.title_tag, c.img_tag, c.price_tag, c.url_tag,
                c.url_attribute, c.url_base, c.url_class, c.price_parent_tag,
                c.price_parent_class, c.price_code, c.price_integer, c.price_decimal,
                c.price_fraction, c.img_attribute, c.parent_class, c.title_class,
                c.price_class, c.img_class, c.alt_price_parent_tag,
                c.alt_price_parent_class, c.alt_img_tag, c.alt_img_class,
                c.alt_parent_class_2, c.alt_img_tag_2, c.alt_img_class_2,
                c.alt_parent_tag_2, c.alt_parent_tag, c.alt_parent_class,
                c.unv_product_tag, c.unv_product_class
            FROM
                configcompanies c
            JOIN
                companies a ON a.id_company = c.id_company
            """
        )

        config = self.cursor.fetchall()

        for i, a in enumerate(self.cursor.description):
            configcompany[a[0]] = [line[i] for line in config]

            value = configcompany[a[0]]

            value_str = str(value[0])

            configcompany[a[0]] = value_str.replace("['", "'").replace("']", "'")
            configcompany[a[0]] = value_str.replace("None", "")

        id_company = configcompany["id_company"]

        url = self.SearchUrlBases(id_company)
        dict_catsub = self.SelectCategories(id_company)
        urls_list = self.BuildUrls(dict_catsub, url)

        configcompany["url"] = urls_list

        return configcompany

    def CheckCompanyExists(self, company):
        self.cursor.execute(
            """
            SELECT id_company FROM companies
            WHERE company = ?
            """,
            (company,),
        )
        value = self.cursor.fetchone()
        if value != None:
            return value[0]
        else:
            return False

    def InsertConfigCompany(
        self,
        id_company,
        parent_tag,
        title_tag,
        img_tag,
        price_tag,
        url_tag,
        url_attribute,
        url_base,
        url_class,
        url_test,
        price_parent_tag,
        price_parent_class,
        price_code,
        price_integer,
        price_decimal,
        price_fraction,
        img_attribute,
        parent_class,
        title_class,
        price_class,
        img_class,
        alt_price_parent_tag,
        alt_price_parent_class,
        alt_img_tag,
        alt_img_class,
        alt_parent_class_2,
        alt_img_tag_2,
        alt_img_class_2,
        alt_parent_tag_2,
        alt_parent_tag,
        alt_parent_class,
    ):
        # Em seguida, insere os dados na tabela `configcompanies`
        self.cursor.execute(
            """
            INSERT INTO configcompanies
            (id_company, parent_tag, title_tag, img_tag, price_tag, url_tag, url_attribute,
            url_base, url_class, url_test, price_parent_tag, price_parent_class, price_code, 
            price_integer, price_decimal, price_fraction, img_attribute, parent_class, title_class, 
            price_class, img_class, alt_price_parent_tag, alt_price_parent_class, alt_img_tag, 
            alt_img_class, alt_parent_class_2, alt_img_tag_2, alt_img_class_2, alt_parent_tag_2, 
            alt_parent_tag, alt_parent_class)
            VALUES (? ,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                id_company,
                parent_tag,
                title_tag,
                img_tag,
                price_tag,
                url_tag,
                url_attribute,
                url_base,
                url_class,
                url_test,
                price_parent_tag,
                price_parent_class,
                price_code,
                price_integer,
                price_decimal,
                price_fraction,
                img_attribute,
                parent_class,
                title_class,
                price_class,
                img_class,
                alt_price_parent_tag,
                alt_price_parent_class,
                alt_img_tag,
                alt_img_class,
                alt_parent_class_2,
                alt_img_tag_2,
                alt_img_class_2,
                alt_parent_tag_2,
                alt_parent_tag,
                alt_parent_class,
            ),
        )
        self.conn.commit()

    def CheckUrlExists(self, url):
        self.cursor.execute(
            "SELECT url FROM urlssearch WHERE url = ?",
            (url,),
        )
        check = self.cursor.fetchall()
        if check == []:
            return False
        else:
            return True

    def VerifyConfigExists(self, parent_tag):
        check = False
        self.cursor.execute(
            """
            SELECT id_company FROM configcompanies WHERE parent_tag = ?
            """,
            (parent_tag,),
        )

        value = self.cursor.fetchone()

        if value:
            check = True

        return check

    def BuildUrls(self, dict_urls, url_base):
        url_list = []
        for a in dict_urls.keys():
            values = dict_urls[a]
            if values != []:
                for b in values:
                    url = url_base + a + "/" + b
            else:
                url = url_base + a
            url_list.append(url)
        print(url_list)
        return url_list

    def SelectCategories(self, id_company):
        dict_urls = {}
        self.cursor.execute(
            """
            SELECT id_category, companyparam FROM categoryparams WHERE id_company = ?
            """,
            (id_company,),
        )

        result = self.cursor.fetchall()
        for c in result:
            subcat = self.SelectSubCategories(id_company, c[0])
            dict_urls[c[1]] = subcat
        return dict_urls

    def SelectCompanyCategories(self, id_company):
        self.cursor.execute(
            """
            SELECT companyparam FROM categoryparams WHERE id_company = ?
            """,
            (id_company,),
        )

        result = self.cursor.fetchall()
        categories = [s[0] for s in result]
        return categories

    def SelectSubCategories(self, id_company, id_category=""):
        self.cursor.execute(
            """
            SELECT companyparam FROM subcategoryparams WHERE id_company = ? AND id_category = ?
            """,
            (
                id_company,
                id_category,
            ),
        )

        result = self.cursor.fetchall()
        subcategories = [s[0] for s in result]
        return subcategories

    def SelectCompanySubCategories(self, id_company):
        self.cursor.execute(
            """
            SELECT companyparam FROM subcategorytitleparams WHERE id_company = ?
            """,
            (id_company,),
        )

        result = self.cursor.fetchall()
        subcategories = [s[0] for s in result]
        return subcategories

    def SearchUrlBases(self, id_company):
        self.cursor.execute(
            "SELECT urlbase FROM urlbases WHERE id_company = ?",
            (id_company,),
        )
        urls = self.cursor.fetchall()
        url = [u[0] for u in urls]

        return url[0]

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
            """,
            (image_src,),
        )
        product_b = self.cursor.fetchall()

        return product_b

    def UpdateProduct(self, column, value_r, id_image):
        query = f"UPDATE products SET {column} = ? WHERE id_image = ?"
        self.cursor.execute(query, (value_r, id_image))

        self.conn.commit()

    def InsertProduct(
        self,
        title,
        price,
        url_product,
        image_src,
        image_blob,
        company,
        category,
        subcategory="",
    ):
        self.cursor.execute(
            "INSERT INTO images (image_src, image_blob, id_company) VALUES (?, ?,(SELECT id_company FROM companies WHERE company = ?))",
            (image_src, image_blob, company),
        )

        self.cursor.execute(
            """INSERT INTO products (title_product,price_product,url_product,id_image, id_company, id_category, id_subcategory) 
            VALUES (?, ?, ?, (SELECT id_image FROM images WHERE image_src = ?),(SELECT id_company FROM companies WHERE company = ?), 
            (SELECT id_category FROM categoryparams WHERE companyparam = ?),
            (SELECT id_subcategory FROM subcategorytitleparams WHERE companyparam = ?)
            )
            
            
            """,
            (
                title,
                price,
                url_product,
                image_src,
                company,
                category,
                subcategory,
            ),
        )

        self.conn.commit()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


ruin = Operations()
ruin.SelectCategories(37)
