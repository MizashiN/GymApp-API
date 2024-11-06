from bs4 import BeautifulSoup
from dataclasses import dataclass
from requests_cache import CachedSession
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

    def get_config(self, brand):
        return self.config.get(brand, {})


class default:
    def __init__(self):
        self.mapper = CategoryMapper()
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
        alternative_price_parent_tag="",
        alternative_price_parent_class="",
        alternative_img_tag="",
        alternative_img_class="",
        alternative_parent_class_2="",
        alternative_img_tag_2="",
        alternative_img_class_2="",
        alternative_parent_tag_2="",
        alternative_parent_tag="",
        alternative_parent_class="",
    ):
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
                    ) or product_info.find(
                        alternative_price_parent_tag, alternative_price_parent_class
                    )
                    if price_items:
                        for p in price_separated:
                            price_scrapp = price_items.find(price_tag, class_=p)
                            if price_scrapp:
                                price_un = price_scrapp.get_text(strip=True)
                                price_list.append(price_un)
                                print(f"Preço encontrado: {price_un}")
                            else:
                                print(
                                    f"Warning: Preço não encontrado para {p} no item {idx + 1}."
                                )
                    else:
                        print(
                            f"Warning: Preço não encontrado para {p} no item {idx + 1}."
                        )

                else:
                    price = product_info.find(price_tag, class_=price_class)

                image = product_info.find(img_tag, class_=img_class)

                if not image:
                    print(
                        "Warning: Primary image not found, trying alternative tag and class"
                    )
                    image = product_info.find(
                        alternative_img_tag, class_=alternative_img_class
                    ) or product_info.find(
                        alternative_img_tag_2, class_=alternative_img_class_2
                    )

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

        session = CachedSession(cache_name="cache/session", expire_after=180)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }

        # Loop para as URLs
        for url in urls:
            print(f"Fetching URL: {url}")
            res = session.get(url, headers=headers)
            print(f"Status Code: {res.status_code}")

            if res.status_code != 200:
                print(f"Failed to fetch URL: {url} with status code {res.status_code}")
                continue

            soup = BeautifulSoup(res.content, "html.parser")

            extract_product_data(soup, parent_tag, parent_class)

            if alternative_parent_tag and alternative_parent_class:
                extract_product_data(
                    soup, alternative_parent_tag, alternative_parent_class
                )

            if alternative_parent_tag_2 and alternative_parent_class_2:
                extract_product_data(
                    soup, alternative_parent_tag_2, alternative_parent_class_2
                )

        result = {"total": len(self.product_list), "products": self.product_list}

        self.list_img_srcs = []
        self.list_srcs = []

        self.list_img_srcs = [product.image_src for product in self.product_list]
        self.list_srcs = self.VerifyImgExists(self.list_img_srcs)
        if not self.list_srcs == []:
            self.InsertImgOnDatabase(self.list_srcs)
        return result

    def VerifyImgExists(self, list_img_srcs):
        self.list = self.operation.verify_images(list_img_srcs)

        return self.list

    def InsertImgOnDatabase(self, list_urls):
        if list_urls:
            self.funcs.download_images(list_urls)


class MaxTitanium(ProductScrapper):
    def __init__(self):
        super().__init__()
        self.name = "MaxTitanium"
        self.config = ProductConfig().get_config(self.name)

    def getUrls(self, category, subcategory=""):
        if category == "proteinas" and not subcategory:
            self.urls = [
                "https://www.maxtitanium.com.br/produtos/proteinas?filter.category-1=produtos&filter.category-2=proteinas&filter.category-3=concentrada",
                "https://www.maxtitanium.com.br/produtos/proteinas?filter.category-1=produtos&filter.category-2=proteinas&filter.category-3=3w",
                "https://www.maxtitanium.com.br/produtos/proteinas?filter.category-1=produtos&filter.category-2=proteinas&filter.category-3=blend-de-proteinas",
                "https://www.maxtitanium.com.br/produtos/proteinas?filter.category-1=produtos&filter.category-2=proteinas&filter.category-3=proteina-vegetal",
                "https://www.maxtitanium.com.br/produtos/proteinas?filter.category-1=produtos&filter.category-2=proteinas&filter.category-3=isolada",
            ]

        elif category == "aminoacidos" and not subcategory:
            self.urls = [
                "https://www.maxtitanium.com.br/produtos?filter.category-1=produtos&filter.category-2=aminoacidos&filter.category-3=creatina",
                "https://www.maxtitanium.com.br/produtos?filter.category-1=produtos&filter.category-2=aminoacidos&filter.category-3=bcaa",
                "https://www.maxtitanium.com.br/produtos?filter.category-1=produtos&filter.category-2=aminoacidos&filter.category-3=colageno",
                "https://www.maxtitanium.com.br/produtos?filter.category-1=produtos&filter.category-2=aminoacidos&filter.category-3=arginina",
                "https://www.maxtitanium.com.br/produtos?filter.category-1=produtos&filter.category-2=aminoacidos&filter.category-3=glutamina",
            ]
        elif category == "creatina" and not subcategory:
            self.urls = [
                f"https://www.maxtitanium.com.br/produtos/aminoacidos/{category}"
            ]

        else:
            if not subcategory:
                self.urls = [
                    f"https://www.maxtitanium.com.br/{category}",
                    f"https://www.maxtitanium.com.br/produtos/{category}",
                    f"https://www.maxtitanium.com.br/produtos?filter.category-1=produtos&filter.category-2={category}",
                    f"https://www.maxtitanium.com.br/s?q={category}",
                ]
            else:
                self.urls = [
                    f"https://www.maxtitanium.com.br/produtos/{category}?filter.category-1=produtos&filter.category-2={category}&filter.category-3={subcategory}"
                ]
        return self.urls

    def set(self, category, subcategory=""):
        mapped_category, mapped_subcategory = self.mapper.map(
            "MaxTitanium", category, subcategory
        )

        urls = self.getUrls(mapped_category, mapped_subcategory)

        return self.fetch_product(urls=urls, **self.config)


class Adaptogen(ProductScrapper):
    def __init__(self):
        super().__init__()
        self.name = "Adaptogen"
        self.config = ProductConfig().get_config(self.name)

    def getUrls(self, category, subcategory=""):
        if subcategory == "whey-protein" and category:
            self.urls = [
                "https://adaptogen.com.br/proteinas/whey-protein-3w/",
                "https://adaptogen.com.br/proteinas/whey-protein-concentrada-proteinas/",
                "https://adaptogen.com.br/proteinas/whey-protein-isolado-e-hidrolisada",
            ]

        else:
            if not subcategory:
                self.urls = [f"https://adaptogen.com.br/{category}/"]
            else:
                self.urls = [f"https://adaptogen.com.br/{category}/{subcategory}/"]
        return self.urls

    def set(self, category, subcategory=""):
        mapped_category, mapped_subcategory = self.mapper.map(
            "Adaptogen", category, subcategory
        )

        urls = self.getUrls(mapped_category, mapped_subcategory)

        return self.fetch_product(urls=urls, **self.config)


class DarkLab(ProductScrapper):
    def __init__(self):
        super().__init__()
        self.name = "DarkLab"
        self.config = ProductConfig().get_config(self.name)

    def getUrls(self, category, subcategory=""):
        if category == "aminoacidos" and not subcategory:
            self.urls = [
                f"https://darklabsuplementos.com.br/aminoacidos/bcaa",
                f"https://darklabsuplementos.com.br/aminoacidos/alanina",
                f"https://darklabsuplementos.com.br/aminoacidos/creatina",
                f"https://darklabsuplementos.com.br/aminoacidos/glutamina",
                f"https://darklabsuplementos.com.br/aminoacidos/l-carnitina",
                f"https://darklabsuplementos.com.br/aminoacidos/colageno",
            ]
        else:
            if not subcategory:
                self.urls = [f"https://darklabsuplementos.com.br/{category}/?mpage=2"]
            else:
                self.urls = [
                    f"https://darklabsuplementos.com.br/{category}/{subcategory}/"
                ]

        return self.urls

    def set(self, category, subcategory=""):
        mapped_category, mapped_subcategory = self.mapper.map(
            "DarkLab", category, subcategory
        )

        urls = self.getUrls(mapped_category, mapped_subcategory)
        return self.fetch_product(urls=urls, **self.config)


class GrowthSupp(ProductScrapper):
    def __init__(self):
        super().__init__()
        self.name = "GrowthSupp"
        self.config = ProductConfig().get_config(self.name)

    def getUrls(self, category, subcategory=""):
        i = 1
        while True:
            self.urls = [f"https://www.gsuplementos.com.br/{category}/?pg={i}"]
            i += 1

            return self.urls

    def set(self, category, subcategory=""):
        mapped_category, mapped_subcategory = self.mapper.map(
            "GrowthSupp", category, subcategory
        )

        urls = self.getUrls(mapped_category, mapped_subcategory)
        return self.fetch_product(urls=urls, **self.config)


class Darkness(ProductScrapper):
    def __init__(self):
        super().__init__()
        self.name = "Darkness"
        self.config = ProductConfig().get_config(self.name)

    def getUrls(self, category, subcategory=""):
        if not subcategory:
            self.urls = [
                f"https://www.darkness.com.br/{category}",
                f"https://www.darkness.com.br/{category}?page=2",
                f"https://www.darkness.com.br/{category}?page=3",
            ]
        else:
            self.urls = [f"https://www.darkness.com.br/{category}/{subcategory}"]
        return self.urls

    def set(self, category, subcategory=""):
        mapped_category, mapped_subcategory = self.mapper.map(
            "Darkness", category, subcategory
        )

        urls = self.getUrls(mapped_category, mapped_subcategory)

        return self.fetch_product(urls=urls, **self.config)


class Mith(ProductScrapper):
    def __init__(self):
        super().__init__()
        self.name = "Mith"
        self.config = ProductConfig().get_config(self.name)

    def getUrls(self, category, subcategory=""):
        if category == "waxy-maize" and not subcategory:
            self.urls = [
                f"https://www.mithoficial.com.br/waxy%20maize?_q=Waxy%20Maize&map=ft"
            ]
        else:
            if not subcategory:
                self.urls = [f"https://www.mithoficial.com.br/{category}"]
            else:
                self.urls = [
                    f"https://www.mithoficial.com.br/{subcategory}/{category}?initialMap=productClusterIds&initialQuery=221&map=category-3,productclusternames"
                ]
        return self.urls

    def set(self, category, subcategory=""):
        mapped_category, mapped_subcategory = self.mapper.map(
            "Mith", category, subcategory
        )

        urls = self.getUrls(mapped_category, mapped_subcategory)

        return self.fetch_product(urls=urls, **self.config)


class All:
    def __init__(self):
        self.brand_instances = [
            Adaptogen(),
            MaxTitanium(),
            DarkLab(),
            Darkness(),
            Mith(),
        ]

    def set(self, category, subcategory=""):
        product_list = []  # Reinicializa a lista para evitar duplicação
        total = 0

        for brand_instance in self.brand_instances:
            brand_products = brand_instance.set(category, subcategory)
            if brand_products and "products" in brand_products:
                product_list.extend(brand_products["products"])

        result = {"totalProducts": len(product_list), "products": product_list}

        return result


class CategoryMapper:
    def __init__(self):
        super().__init__()
        self.params = {}

    def map(self, brand_name, category, subcategory=""):
        self.params = self.paramStorage(brand_name)
        mapped_category = self.params.get(category, category)
        mapped_subcategory = (
            self.params.get(subcategory, subcategory) if subcategory else ""
        )

        return mapped_category, mapped_subcategory

    def paramStorage(self, brand_name):
        params_map = {
            "MaxTitanium": {
                "proteins": "proteinas",
                "products": "produtos",
                "aminoacids": "aminoacidos",
                "pre-workouts": "pre-treino",
                "whey-proteins": "whey-protein",
                "creatines": "creatina",
                "hypercalorics": "hipercaloricos",
                "protein-bars": "barras-proteicas",
                "clothes": "roupas",
                "shakers": "coqueteleiras",
                "t-shirts": "camisetas",
                "vitamins": "vitaminas-e-minerais",
                "thermogenics": "termogenicos",
                "carbohydrates": "carboidratos",  # SubCategoria, Precisa da Categoria Produtos
            },
            "Adaptogen": {
                "proteins": "proteinas",
                "products": "produtos",
                "aminoacids": "aminoacidos",
                "pre-workouts": "pre-treino-formulas",
                "whey-proteins": "whey-protein",
                "creatines": "creatina",
                "hypercalorics": "hipercaloricos",
                "protein-bars": "barras-de-proteinas",
                "clothes": "roupas",
                "shakers": "coqueteleira",
                "t-shirts": "camisetas",
                "vitamins": "vitaminas-e-nutrientes",
                "thermogenics": "termogenico",
                "carbohydrates": "carboidratos",
            },
            "DarkLab": {
                "proteins": "proteinas",
                "products": "produtos",
                "aminoacids": "aminoacidos",
                "pre-workouts": "pre-treino1",
                "whey-proteins": "whey-protein",
                "creatines": "creatina",
                "hypercalorics": "waxy-maize",
                "protein-bars": "barras-de-proteinas",
                "clothes": "vestuario2",
                "shakers": "coqueteleira",
                "t-shirts": "camisetas",
                "vitamins": "vitaminas",
                "thermogenics": "termogenico",
                "carbohydrates": "carboidratos",
                "acessories": "acessorios",
            },
            "Darkness": {
                "proteins": "proteina",
                "products": "produtos",
                "aminoacids": "aminoacidos",
                "pre-workouts": "pre-treino",
                "whey-proteins": "whey-protein",
                "creatines": "creatina",
                "hypercalorics": "hipercalorico",
                "protein-bars": "barra-de-proteina",
                "clothes": "moda",
                "shakers": "coqueteleira",
                "t-shirts": "camisetas",
                "vitamins": "vitaminas",
                "thermogenics": "termogenico",
                "carbohydrates": "carboidratos",
                "acessories": "acessorios",
            },
            "Mith": {
                "proteins": "proteinas-whey-protein",
                "products": "suplementos",
                "aminoacids": "aminoacidos",
                "pre-workouts": "pre-treino",
                "whey-proteins": "proteinas-whey-protein",
                "creatines": "creatina",
                "hypercalorics": "hipercalorico",
                "protein-bars": "barra-de-proteina",
                "clothes": "moda",
                "shakers": "coqueteleiras-mith",
                "t-shirts": "camisetas",
                "vitamins": "vitaminas",
                "thermogenics": "termogenico",
                "carbohydrates": "waxy-maize",
                "acessories": "acessorios",
                "kits": "kits-promocionais",
            },
        }

        self.params = params_map.get(brand_name, {})
        return self.params
