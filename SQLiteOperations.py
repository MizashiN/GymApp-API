import sqlite3
from itertools import chain


class Operations:
    def __init__(self):
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()

    def SelectConfigCompany(self, id_company):

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
                c.unv_product_tag, c.unv_product_class, c.page_param,
                c.perc_pix
            FROM
                configcompanies c
            JOIN
                companies a ON a.id_company = c.id_company
            WHERE 
                c.id_company = ?    
            """,
            (id_company,),
        )

        config = self.cursor.fetchall()
        for i, a in enumerate(self.cursor.description):
            configcompany[a[0]] = [line[i] for line in config]

            value = configcompany[a[0]]

            value_str = str(value[0])

            configcompany[a[0]] = value_str.replace("['", "'").replace("']", "'")
            configcompany[a[0]] = value_str.replace("None", "")

        id_cp = configcompany["id_company"]

        url = configcompany["url_base"]
        page_param = configcompany["page_param"]
        dict_catsub = self.SelectCategories(id_cp)
        urls_list = self.BuildUrls(dict_catsub, url, page_param)
        print(urls_list)
        del configcompany["page_param"]

        configcompany["url"] = urls_list

        return configcompany

    def BuildUrls(self, dict_urls, url_base, page_param):
        url_list = []
        for a in dict_urls.keys():
            values = dict_urls[a]
            if values != []:
                for b in values:
                    url = url_base + "/" + a + "/" + b + page_param
            else:
                url = url_base + "/" + a + page_param
            url_list.append(url)
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

    def SelectCompanies(self):
        self.cursor.execute(
            """
            SELECT id_company FROM companies
            """
        )

        result = self.cursor.fetchall()
        companies = [s[0] for s in result]
        return companies

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

    def SelectSubCategories(self, id_company, companyparam):
        self.cursor.execute(
            """
            SELECT companyparam FROM subcategoryparams WHERE id_company = ? AND id_category =
            (SELECT id_category FROM categoryparams WHERE companyparam = ?)
            """,
            (
                id_company,
                companyparam,
            ),
        )

        result = self.cursor.fetchall()
        subcategories = [s[0] for s in result]
        return subcategories

    def SelectTitleSubCategories(self, id_company, companyparam):
        self.cursor.execute(
            """
            SELECT companyparam FROM subcategorytitleparams WHERE id_company = ? AND id_category =
            (SELECT id_category FROM categoryparams WHERE companyparam = ?)
            """,
            (
                id_company,
                companyparam,
            ),
        )

        result = self.cursor.fetchall()
        subcategories = [s[0] for s in result]
        return subcategories

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
            """INSERT INTO products (
                title_product,
                price_product,
                url_product,
                id_image,
                id_company,
                id_category,
                id_subcategory
            )
            VALUES (
                ?, ?, ?, 
                (SELECT id_image FROM images WHERE image_src = ?),
                (SELECT id_company FROM companies WHERE company = ?), 
                (SELECT id_category FROM categoryparams WHERE companyparam = ?),
                COALESCE(
                    (SELECT id_subcategory FROM subcategorytitleparams WHERE companyparam = ?),
                    (SELECT id_subcategory FROM subcategoryparams WHERE companyparam = ?)
                )
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
