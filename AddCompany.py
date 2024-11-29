from bs4 import BeautifulSoup
from dataclasses import dataclass
from SQLiteOperations import Operations
from generic_funcs import funcs
import requests
import json
import re


@dataclass
class ProductData:
    title: str
    price: str
    image_src: str
    url: str
    company: str
    category: str
    subcategory: str = None

class default:
    def __init__(self):
        self.operation = Operations()
        self.funcs = funcs()
        self.product_list = []
        self.categories = []
        self.subcategories = []
        self.url_break = False


class ProductScrapper(default):

    def fetch_product(
        self,
        url,
        parent_tag,
        title_tag,
        img_tag,
        price_tag,
        id_company,
        company,
        unv_product_tag,
        unv_product_class,
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
            if not product_items:
                print("Não achou product items então acabou a url")
                self.url_break = True
                return
            for idx, product_info in enumerate(product_items):

                unv_product = product_info.find(
                    unv_product_tag, class_=unv_product_class
                )

                if unv_product:
                    print(unv_product)
                    self.url_break = True
                    return

                title = product_info.find(title_tag, class_=title_class)

                price_list = []
                price = None
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

                    if url_base:
                        url_product = url_base + url_product

                    if not url_product.startswith("https"):
                        url_product = "https://" + url_product

                    image_src = image.get(img_attribute).split(",")[0].split(" ")[0]
                    if not image_src.startswith("https:"):
                        image_src = "https:" + image_src

                    for a in self.categories:
                        cat = u.find(a)
                        if cat != -1:
                            category_name = a
                            self.subcategories = self.operation.SelectCompanySubCategories(id_company, a)
                            break

                    title_lower = title_text.lower()
                    for b in self.subcategories:
                        subcat = title_lower.find(b)
                        if subcat != -1:
                            subcategory_name = b
                            break
                        else:
                            subcategory_name = ""
                    if (
                        title_text
                        and price_text
                        and image_src
                        and url_product
                        and category_name
                    ):

                        list_product = []
                        list_product = [
                            title_text,
                            price_text,
                            image_src,
                            url_product,
                        ]

                        self.product_list.append(
                            ProductData(
                                title=title_text,
                                price=price_text,
                                image_src=image_src,
                                url=url_product,
                                company=company,
                                category=category_name,
                                subcategory=subcategory_name,
                            )
                        )
                    else:
                        print("está faltando alguma condição")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        }

        self.categories = self.operation.SelectCompanyCategories(id_company)

        for u in url:
            self.url_break = False
            for i in range(1, 100):
                urlPage = f"{u}{pageparam}{i}"
                res = requests.get(urlPage, headers=headers)
                print(urlPage)
                print(f"Status Code: {res.status_code}")

                if res.status_code != 200:
                    print(
                        f"Failed to fetch URL: {u} with status code {res.status_code}"
                    )

                soup = BeautifulSoup(res.content, "html.parser")

                extract_product_data(soup, parent_tag, parent_class)

                if alt_parent_tag and alt_parent_class:
                    extract_product_data(soup, alt_parent_tag, alt_parent_class)

                if alt_parent_tag_2 and alt_parent_class_2:
                    extract_product_data(soup, alt_parent_tag_2, alt_parent_class_2)

                if self.url_break:
                    break

        result = {"total": len(self.product_list), "products": self.product_list}
        self.VerifyAlteration(self.product_list)
        return result

    def VerifyAlteration(self, product_list):
        product_b = []
        for product_r in product_list:
            (
                image_src_r,
                price_r,
                title_r,
                url_r,
                company_name,
                category,
                subcategory,
            ) = (
                product_r.image_src,
                product_r.price,
                product_r.title,
                product_r.url,
                product_r.company,
                product_r.category,
                product_r.subcategory,
            )

            price_r = float(price_r.replace("R$", "").strip().replace(",", "."))

            product_b = self.operation.SelectProduct(image_src_r)

            if product_b:
                print(f"Produto \033[1;37m{title_r}\033[0m existe no banco")
                product = product_b[0]
                if product[0] != title_r:
                    self.operation.UpdateProduct("title_product", title_r, product[3])
                    print(f"Produto \033[1;37m{title_r}\033[0m \033[33mhouve mudança no nome\033[0m")
                if product[1] != price_r:
                    self.operation.UpdateProduct("price_product", price_r, product[3])
                    print(f"Produto \033[1;37m{title_r}\033[0m \033[33mhouve mudança no preço\033[0m")
                if product[2] != url_r:
                    self.operation.UpdateProduct("url_product", url_r, product[3])
                    print(f"Produto \033[1;37m{title_r}\033[0m \033[33mhouve mudança na url\033[0m")
            else:
                image_blob_r = self.funcs.download_image(image_src_r)
                self.operation.InsertProduct(
                    title_r,
                    price_r,
                    url_r,
                    image_src_r,
                    image_blob_r,
                    company_name,
                    category,
                    subcategory,
                )
                print(f"\033[1;37m{title_r}\033[0m \033[92mInserido com Sucesso\033[0m")


run = ProductScrapper()
configDB = Operations()

product_config = configDB.SelectConfigCompany()
run.fetch_product(**product_config)
