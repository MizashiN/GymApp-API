from bs4 import BeautifulSoup
from dataclasses import dataclass
import requests
from SQLiteOperations import Operations
from generic_funcs import funcs
import json
import re


@dataclass
class ProductData:
    title: str
    price: str
    image_src: str
    url: str


class ProductConfig:
    def __init__(self, config_file="configSupp.json"):
        with open(config_file, "r") as f:
            self.config = json.load(f)

    def get_config(self):
        return self.config


class default:
    def __init__(self):
        self.operation = Operations()
        self.funcs = funcs()
        self.urls = []
        self.list_img_srcs = []
        self.product_list = []


class ProductScrapper(default):

    def fetch_product(
        self,
        urls,
        parent_tag,
        title_tag,
        img_tag,
        price_tag,
        url_test="",
        url_tag="",
        url_attribute="",
        url_base="",
        url_class="",
        price_parent_tag="",
        price_parent_class="",
        price_code="",
        price_integer="",
        price_decimal="",
        price_fraction="",
        img_attribute="",
        parent_class="",
        title_class="",
        price_class="",
        img_class="",
        alt_price_parent_tag="",
        alt_price_parent_class="",
        alt_img_tag="",
        alt_img_class="",
        alt_parent_class_2="",
        alt_img_tag_2="",
        alt_img_class_2="",
        alt_parent_tag_2="",
        alt_parent_tag="",
        alt_parent_class="",
    ):
        self.product_list = []

        def extract_product_data(soup, parent_tag, parent_class):
            product_items = soup.find_all(parent_tag, class_=parent_class)

            for idx, product_info in enumerate(product_items):
                title = product_info.find(title_tag, class_=title_class)

                price_list = []
                if (
                    price_tag
                    and price_code
                    and price_integer
                    and price_decimal
                    and price_fraction
                ):
                    price_separated = [
                        price_code,
                        price_integer,
                        price_decimal,
                        price_fraction,
                    ]

                    price_items = product_info.find(
                        price_parent_tag, class_=price_parent_class
                    ) or product_info.find(alt_price_parent_tag, alt_price_parent_class)
                    if price_items:
                        for p in price_separated:
                            price_scrapp = price_items.find(price_tag, class_=p)
                            if price_scrapp:
                                price_un = price_scrapp.get_text(strip=True)
                                price_list.append(price_un)
                            else:
                                print(
                                    f"Warning: Preço não encontrado para {p} no item {idx + 1}."
                                )
                    else:
                        print(f"Warning: Preço não encontrado no item {idx + 1}.")

                else:
                    price = product_info.find(price_tag, class_=price_class)

                image = product_info.find(img_tag, class_=img_class)

                if not image:
                    print("Warning: Primary image not found, trying alt tag and class")
                    image = product_info.find(
                        alt_img_tag, class_=alt_img_class
                    ) or product_info.find(alt_img_tag_2, class_=alt_img_class_2)

                link_product = product_info.find(url_tag, url_class)

                if not link_product:
                    parent_item = product_info.find_parent()
                    if parent_item:
                        link_product = parent_item.find(url_tag, class_=url_class)
                        if link_product:
                            print(f"Link do produto encontrado no pai: {link_product}")
                        else:
                            print("Warning: href não encontrado no elemento pai.")
                    else:
                        print("Warning: Elemento pai não encontrado.")

                if title and image and link_product and (price or price_list):
                    title_text = title.get_text(strip=True)
                    if price:
                        price_text = (
                            price.get_text(strip=True)
                            .replace("\u00a0", "")
                            .replace("R$", "R$ ")
                            .replace("R$  ", "R$ ")
                            .strip()
                        )

                        price_text = re.sub(
                            r"^(R\$ \d{1,3}(?:\.\d{3})*(?:,\d{2})?)(.*)",
                            r"\1",
                            price_text,
                        ).strip()
                    if price_list:
                        price_text = "".join(price_list).replace("R$", "R$ ")

                    url_product = link_product.get(url_attribute)
                    pos = -1
                    if url_base:
                        url_product = url_base + url_product
                        pos = url_product.find("https")

                    if pos != -1:
                        url_product = url_product[pos:]

                    image_src = image.get(img_attribute).split(",")[0].split(" ")[0]
                    if not image_src.startswith("https:"):
                        image_src = "https:" + image_src

                    if title_text and price_text and image_src and url_product:
                        print("Success Scrapping")
                        list_product = []
                        list_product = [title_text, price_text, image_src, url_product]

                        for l in list_product:
                            print(l)
                        print("-" * 10)

                    self.product_list.append(
                        ProductData(
                            title=title_text,
                            price=price_text,
                            image_src=image_src,
                            url=url_product,
                        )
                    )
                else:
                    print(
                        "Warning: Skipping product item due to missing data (title, price, or image)"
                    )

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        for url in urls:
            res = requests.get(url, headers=headers)
            print(f"Status Code: {res.status_code}")

            if res.status_code != 200:
                print(f"Failed to fetch URL: {url} with status code {res.status_code}")

            soup = BeautifulSoup(res.content, "html.parser")

            extract_product_data(soup, parent_tag, parent_class)

            if alt_parent_tag and alt_parent_class:
                extract_product_data(soup, alt_parent_tag, alt_parent_class)

            if alt_parent_tag_2 and alt_parent_class_2:
                extract_product_data(soup, alt_parent_tag_2, alt_parent_class_2)
                
        result = {"total": len(self.product_list), "products": self.product_list}
        
        self.VerifyCompanyExists(self.product_list)
        self.VerifyAlteration(self.product_url)
        
        return result
    def VerifyCompanyExists(self, product_list):
        product_list
        
    def VerifyAlteration(self, product_list):
        product_b = []
        for product_r in product_list:
            (
                image_src_r,
                price_r,
                title_r,
                url_r,
            ) = (
                product_r.image_src,
                product_r.price,
                product_r.title,
                product_r.url,
            )

            price_r = float(price_r.replace("R$", "").strip().replace(",", "."))

            product_b = self.operation.SelectProduct(image_src_r)

            if product_b:
                print(f"Produto {title_r} existe no banco")
                product = product_b[0]
                if product[0] != title_r:
                    self.operation.UpdateProduct("title_product", title_r, product[3])
                if product[1] != price_r:
                    self.operation.UpdateProduct("price_product", price_r, product[3])
                if product[2] != url_r:
                    self.operation.UpdateProduct("url_product", url_r, product[3])
            else:
                print(f"Inserindo o Produto {title_r}")
                image_blob_r = self.funcs.download_image(image_src_r)
                self.operation.InsertProduct(
                    title_r, price_r, url_r, image_src_r, image_blob_r,
                )

run = ProductScrapper()
configDB = Operations()
configJson = ProductConfig()

choice = input("Json(1) or Sqlite(2)")
if choice == "1":
    product_config = configDB.SelectConfigCompany()
    run.fetch_product(**product_config)
elif choice == "2":
    product_config = configJson.get_config()
    run.fetch_product(**product_config)
