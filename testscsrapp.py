import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
import os
import json
import re


@dataclass
class ProductData:
    title: str
    price: str
    image_src: str
    url: str


class default:
    def __init__(self):
        self.list_img_srcs = []
        self.product_list = []


class ProductConfig:
    def __init__(self, config_file="testScrapp/config.json"):
        with open(config_file, "r") as f:
            self.config = json.load(f)


class ProductScrapper(default):

    def fetch_product(
        self,
        url_test,
        parent_tag,
        title_tag,
        img_tag,
        price_tag,
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

            price = ""
            for idx, product_info in enumerate(product_items):
                title = product_info.find(title_tag, class_=title_class) 
                
                print(title)

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
                                    f"Warning: Preço não encontrado para não encontrado ."
                                )
                    else:
                        print(f"Warning: Preço não encontrado{idx + 1}.")

                else:
                    price = product_info.find(price_tag, class_=price_class) if price else ""

                image = product_info.find(img_tag, class_=img_class)
                
                if not image:
                    print("Warning: Primary image not found, trying alt tag and class")
                    image = product_info.find(
                        alt_img_tag, class_=alt_img_class
                    ) or product_info.find(alt_img_tag_2, class_=alt_img_class_2)
                
                print(image)

                link_product = product_info.find(url_tag, url_class)
                if link_product == None:
                    link_product = ""

                if not link_product:
                    parent_item = product_info.find_parent()
                    if parent_item:
                        link_product = parent_item.find(url_tag, class_=url_class)
                        if not link_product:
                            print("Warning: href não encontrado no elemento pai.")
                    else:
                        print("Warning: Elemento pai não encontrado.")
                print(link_product)

                if title and image and link_product and (price or price_list):
                    title_text = title.get_text(strip=True)
                    print(title_text)
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
                    
                    print(price_text)
                    
                    url_product = link_product.get(url_attribute)
                    pos = -1
                    if url_base:
                        url_product = url_base + url_product
                        pos = url_product.find("https")

                    if pos != -1:
                        url_product = url_product[pos:]
                        
                    print(url_product)

                    image_src = image.get(img_attribute).split(",")[0].split(" ")[0]
                    if not image_src.startswith("https:"):
                        image_src = "https:" + image_src
                    print(image_src)
                        

                    
                    if title_text and image_src and url_product and price_text:
                        print("Scrapping Success")

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
                        "Warning: Skipping product item due to missing data (title, price, or image or link product)"
                    )


        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }

        print(f"Fetching URL: {url_test}")
        res = requests.get(url_test, headers=headers)
        print(f"Status Code: {res.status_code}")

        if res.status_code != 200:
            print(f"Failed to fetch URL: {url_test} with status code {res.status_code}")

        soup = BeautifulSoup(res.content, "html.parser")

        extract_product_data(soup, parent_tag, parent_class)

        if alt_parent_tag and alt_parent_class:
            extract_product_data(soup, alt_parent_tag, alt_parent_class)

        if alt_parent_tag_2 and alt_parent_class_2:
            extract_product_data(soup, alt_parent_tag_2, alt_parent_class_2)

        result = {"total": len(self.product_list), "products": self.product_list}
        return result

run = ProductScrapper()
config = ProductConfig()

run.fetch_product(**config.config)
