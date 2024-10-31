from bs4 import BeautifulSoup
from dataclasses import dataclass
from requests_cache import CachedSession
import requests
import json

@dataclass
class ProductData:
    title: str
    price: str
    image_src: str
class ProductConfig:
    def __init__(self, config_file='configSupp.json'):
        with open(config_file, 'r') as f:
            self.config = json.load(f)

    def get_config(self, brand):
        return self.config.get(brand, {})        
    
class default:
    def __init__(self):
        self.search = ProductScrapper.fetch_product
        self.mapper = CategoryMapper()
        self.urls = []
        
class ProductScrapper(default):
    @staticmethod     
    def fetch_product(urls, parent_tag, title_tag, img_tag, price_tag, img_attribute="",
                      parent_class="", title_class="", price_class="", img_class="",
                      alternative_img_tag="", alternative_img_class="",alternative_parent_class_2="",
                      alternative_img_tag_2="", alternative_img_class_2="",alternative_parent_tag_2="",
                      alternative_parent_tag="", alternative_parent_class=""):

        def extract_product_data(soup, parent_tag, parent_class):
            product_items = soup.find_all(parent_tag, class_=parent_class)
            
            for idx, product_info in enumerate(product_items):
                title = product_info.find(title_tag, class_=title_class)
                price = product_info.find(price_tag, class_=price_class)
                image = product_info.find(img_tag, class_=img_class)
                
                # Tentar alternativa de imagem
                if not image:
                    print("Warning: Primary image not found, trying alternative tag and class")
                    image = product_info.find(alternative_img_tag, class_=alternative_img_class) or \
                            product_info.find(alternative_img_tag_2, class_=alternative_img_class_2)
                
                # Verificar se os dados foram encontrados
                if title and price and image:
                    title_text = title.get_text(strip=True)
                    price_text = price.get_text(strip=True).replace('\u00a0', '').replace('R$', 'R$ ').strip()
                    image_src = image.get(img_attribute)
                    
                    product_list.append(ProductData(title=title_text, price=price_text, image_src=image_src))
                else:
                    print("Warning: Skipping product item due to missing data (title, price, or image)")

        product_list = []
        session = CachedSession(
            cache_name='cache/session',
            expire_after=3600
        )
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
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
            
            # Primeiro fetch usando o parent_tag principal
            extract_product_data(soup, parent_tag, parent_class)

            # Se houver parent_tag e class alternativos, fazer novo fetch
            if alternative_parent_tag and alternative_parent_class:
                extract_product_data(soup, alternative_parent_tag, alternative_parent_class)
            
            if alternative_parent_tag_2 and alternative_parent_class_2:
                extract_product_data(soup, alternative_parent_tag_2, alternative_parent_class_2)

        result = {
            "total": len(product_list),
            "products": product_list
        }
        
        return result
    
class MaxTitanium(default):
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
                "https://www.maxtitanium.com.br/produtos/proteinas?filter.category-1=produtos&filter.category-2=proteinas&filter.category-3=isolada"
            ]
            
        elif category == "aminoacidos" and not subcategory:
            self.urls = [
                "https://www.maxtitanium.com.br/produtos?filter.category-1=produtos&filter.category-2=aminoacidos&filter.category-3=creatina",
                "https://www.maxtitanium.com.br/produtos?filter.category-1=produtos&filter.category-2=aminoacidos&filter.category-3=bcaa",
                "https://www.maxtitanium.com.br/produtos?filter.category-1=produtos&filter.category-2=aminoacidos&filter.category-3=colageno",
                "https://www.maxtitanium.com.br/produtos?filter.category-1=produtos&filter.category-2=aminoacidos&filter.category-3=arginina",
                "https://www.maxtitanium.com.br/produtos?filter.category-1=produtos&filter.category-2=aminoacidos&filter.category-3=glutamina"
            ]
        elif category == "creatina" and not subcategory:
            self.urls = [
                f"https://www.maxtitanium.com.br/produtos/aminoacidos/{category}"
            ]
        
        else:
            if not subcategory:    
                self.urls = [   
                    f"https://www.maxtitanium.com.br/produtos/{category}",   
                    f"https://www.maxtitanium.com.br/produtos?filter.category-1=produtos&filter.category-2={category}",
                    f"https://www.maxtitanium.com.br/s?q={category}"
                ]
            else:
                self.urls = [
                    f"https://www.maxtitanium.com.br/produtos/{category}?filter.category-1=produtos&filter.category-2={category}&filter.category-3={subcategory}"
                ]
        return self.urls
    
    def set(self, category, subcategory=""):
        mapped_category, mapped_subcategory = self.mapper.map("MaxTitanium", category, subcategory)
        
        urls = self.getUrls(mapped_category, mapped_subcategory)
        
        return self.search(
            urls=urls,
            **self.config           
            )  

class Adaptogen(default):
    def __init__(self):
        super().__init__()
        self.name = "Adaptogen"
        self.config = ProductConfig().get_config(self.name)
        
    def getUrls(self, category, subcategory=""):
        if category == "whey-protein" and not subcategory:
            self.urls = [
                "https://adaptogen.com.br/proteinas/whey-protein-3w/",
                "https://adaptogen.com.br/proteinas/whey-protein-concentrada-proteinas/",
                "https://adaptogen.com.br/proteinas/whey-protein-isolado-e-hidrolisada/"
            ]

        else:
            if not subcategory:    
                self.urls = [
                    f"https://adaptogen.com.br/{category}/"
                ]
            else:
                self.urls = [
                    f"https://adaptogen.com.br/{category}/{subcategory}/"
                ]
        return self.urls
    
    def set(self, category, subcategory=""):
        mapped_category, mapped_subcategory = self.mapper.map("Adaptogen", category, subcategory)
        
        urls = self.getUrls(mapped_category, mapped_subcategory)
        
        return self.search(
            urls=urls,
            **self.config
            )         

class DarkLab(default):
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
                 f"https://darklabsuplementos.com.br/aminoacidos/colageno"
                ]           
        else:
            if not subcategory:    
                self.urls = [
                    f"https://darklabsuplementos.com.br/{category}/?mpage=2"
                    ]
            else:
                self.urls = [
                    f"https://darklabsuplementos.com.br/{category}/{subcategory}/"
                ]

        return self.urls
    
    def set(self, category, subcategory=""):
        mapped_category, mapped_subcategory = self.mapper.map("DarkLab", category, subcategory)

        urls = self.getUrls(mapped_category, mapped_subcategory)
        print(urls)
        return self.search(
            urls=urls,
            **self.config
            )         

class All:
    def __init__(self):
        self.brand_instances = [
            Adaptogen(),
            MaxTitanium(),
            DarkLab()
        ]
    
    def set(self, category, subcategory=""):
        product_list = []  # Reinicializa a lista para evitar duplicação
        total = 0

        for brand_instance in self.brand_instances:
            brand_products = brand_instance.set(category, subcategory)
            if brand_products and "products" in brand_products:
                product_list.extend(brand_products["products"])
                
        result = {
            "totalProducts": len(product_list),  
            "products": product_list
        }
        
        return result
    
class CategoryMapper():
    def __init__(self):
        super().__init__()
        self.params = {}
    def map(self, brand_name, category, subcategory=""):
        self.params = self.paramStorage(brand_name)   
        mapped_category = self.params.get(category, category)
        mapped_subcategory = self.params.get(subcategory, subcategory) if subcategory else ""
        
        return mapped_category, mapped_subcategory
        
    def paramStorage(self, brand_name):
        params_map = {
            "MaxTitanium": {
                "protein": "proteinas",
                "aminoacid": "aminoacidos",
                "pre-workout": "pre-treino",
                "whey-protein": "whey-protein",
                "creatine": "creatina"
            },
            "Adaptogen": {
                "protein": "proteinas",
                "pre-workout": "pre-treino-formulas",
                "aminoacid": "aminoacidos",
                "whey-protein": "whey-protein",
                "creatine": "creatina"
            },
            "DarkLab": {
                "protein": "proteinas",
                "aminoacid": "aminoacidos",
                "pre-workouts": "pre-treino1",
                "whey-protein": "whey-protein",
                "creatine": "creatina"
            }
        }

        self.params = params_map.get(brand_name, {})
        return self.params
