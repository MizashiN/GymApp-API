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
    def __init__(self, config_file="json/config.json"):
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
                    print(parent_item)
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

    def fetch_product_input(self):
        test_name = input("Digite o nome do teste: ")
        parent_tag = input("Digite a tag pai (parent_tag): ")
        parent_class = (
            input("Digite a classe do elemento pai (parent_class) [opcional]: ") or ""
        )

        title_class = (
            input("Digite a classe do título (title_class) [opcional]: ") or ""
        )
        title_tag = input("Digite a tag de título (title_tag): ")
        price_tag = input("Digite a tag de preço (price_tag): ")
        price_class = input("Digite a classe do preço (price_class) [opcional]: ") or ""
        img_tag = input("Digite a tag de imagem (img_tag): ")
        img_class = input("Digite a classe da imagem (img_class) [opcional]: ") or ""
        img_attribute = (
            input("Digite o atributo da imagem (img_attribute) [opcional]: ") or ""
        )
        url_test = input("Digite a URL de teste: ")

        url_tag = input("Digite a tag para o URL (url_tag) [opcional]: ") or ""
        url_class = input("Digite a classe do URL (url_class) [opcional]: ") or ""
        url_attribute = (
            input("Digite o atributo do URL (url_attribute) [opcional]: ") or ""
        )
        url_base = input("Digite a base do URL (url_base) [opcional]: ") or ""

        price_parent_tag = (
            input("Digite a tag pai do preço (price_parent_tag) [opcional]: ") or ""
        )
        price_parent_class = (
            input("Digite a classe pai do preço (price_parent_class) [opcional]: ")
            or ""
        )
        price_code = input("Digite o código do preço (price_code) [opcional]: ") or ""
        price_integer = (
            input("Digite a parte inteira do preço (price_integer) [opcional]: ") or ""
        )
        price_decimal = (
            input("Digite a parte decimal do preço (price_decimal) [opcional]: ") or ""
        )
        price_fraction = (
            input("Digite a fração do preço (price_fraction) [opcional]: ") or ""
        )

        alt_price_parent_tag = (
            input(
                "Digite a tag alternativa do preço (alt_price_parent_tag) [opcional]: "
            )
            or ""
        )
        alt_price_parent_class = (
            input(
                "Digite a classe alternativa do preço (alt_price_parent_class) [opcional]: "
            )
            or ""
        )
        alt_img_tag = (
            input("Digite a tag alternativa da imagem (alt_img_tag) [opcional]: ") or ""
        )
        alt_img_class = (
            input("Digite a classe alternativa da imagem (alt_img_class) [opcional]: ")
            or ""
        )

        alt_parent_class_2 = (
            input(
                "Digite a segunda classe alternativa do elemento pai (alt_parent_class_2) [opcional]: "
            )
            or ""
        )
        alt_img_tag_2 = (
            input(
                "Digite a segunda tag alternativa da imagem (alt_img_tag_2) [opcional]: "
            )
            or ""
        )
        alt_img_class_2 = (
            input(
                "Digite a segunda classe alternativa da imagem (alt_img_class_2) [opcional]: "
            )
            or ""
        )
        alt_parent_tag_2 = (
            input(
                "Digite a segunda tag alternativa do elemento pai (alt_parent_tag_2) [opcional]: "
            )
            or ""
        )
        alt_parent_tag = (
            input(
                "Digite a tag alternativa do elemento pai (alt_parent_tag) [opcional]: "
            )
            or ""
        )
        alt_parent_class = (
            input(
                "Digite a classe alternativa do elemento pai (alt_parent_class) [opcional]: "
            )
            or ""
        )

        product_data = {
            "test_name": test_name,
            "url_test": url_test,
            "parent_tag": parent_tag,
            "title_tag": title_tag,
            "img_tag": img_tag,
            "price_tag": price_tag,
            "url_tag": url_tag,
            "url_attribute": url_attribute,
            "url_base": url_base,
            "url_class": url_class,
            "price_parent_tag": price_parent_tag,
            "price_parent_class": price_parent_class,
            "price_code": price_code,
            "price_integer": price_integer,
            "price_decimal": price_decimal,
            "price_fraction": price_fraction,
            "img_attribute": img_attribute,
            "parent_class": parent_class,
            "title_class": title_class,
            "price_class": price_class,
            "img_class": img_class,
            "alt_price_parent_tag": alt_price_parent_tag,
            "alt_price_parent_class": alt_price_parent_class,
            "alt_img_tag": alt_img_tag,
            "alt_img_class": alt_img_class,
            "alt_parent_class_2": alt_parent_class_2,
            "alt_img_tag_2": alt_img_tag_2,
            "alt_img_class_2": alt_img_class_2,
            "alt_parent_tag_2": alt_parent_tag_2,
            "alt_parent_tag": alt_parent_tag,
            "alt_parent_class": alt_parent_class,
        }

        # Salva os dados em um arquivo JSON
        folder_name = "testScrapp"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Define o caminho do arquivo JSON
        file_name = os.path.join(folder_name, f"{test_name}_data.json")

        # Salva os dados em um arquivo JSON
        with open(file_name, "w") as json_file:
            json.dump(product_data, json_file, indent=4)

        print(f"Os dados do teste '{test_name}' foram salvos em '{file_name}'.")

        self.fetch_product(
            url_test,
            parent_tag,
            title_tag,
            img_tag,
            price_tag,
            url_tag,
            url_attribute,
            url_base,
            url_class,
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
        )


run = ProductScrapper()
run.fetch_product_input()
