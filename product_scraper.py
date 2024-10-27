from bs4 import BeautifulSoup
from dataclasses import dataclass
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
        
class ProductScrapper():
    @staticmethod     
    def fetch_product(urls, parent_tag, title_tag, img_tag, price_tag, img_attribute="",  parent_class="",  title_class="",  
                      price_class="", img_class="", alternative_img_tag="",alternative_img_class=""):
        product_list = []
        for url in urls:
            res = requests.get(url)

            if res.status_code != 200:
                continue
            
            print(url)
            soup = BeautifulSoup(res.content, "html.parser")
            product_items = soup.find_all(parent_tag, class_=parent_class)
            for product_info in product_items:
                title = product_info.find(title_tag, class_=title_class)
                price = product_info.find(price_tag, class_=price_class)
                image = product_info.find(img_tag, class_=img_class)

                if not image:
                    image = product_info.find(alternative_img_tag, class_=alternative_img_class)
                
                if title and price and image:
                    title_text = title.get_text(strip=True)
                    price_text = price.get_text(strip=True).replace('\u00a0', '').replace('R$', 'R$ ').strip()
                    image_src = image.get(img_attribute)
                    
                    product_list.append(ProductData(title=title_text, price=price_text, image_src=image_src))
        
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

class All:
    def __init__(self):
        self.brand_instances = [
            Adaptogen(),
            MaxTitanium()
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
        if brand_name == "MaxTitanium":
            self.params = {
            "proteins": "proteinas",
            "amino-acids": "aminoacidos",
            "pre-workouts": "pre-treino",
            "whey-protein": "whey-protein",
            "creatine": "creatina"
             }
        elif brand_name == "Adaptogen":
            self.params = {
                    "proteins": "proteinas",
                    "pre-workouts": "pre-treino-formulas",
                    "amino-acids": "aminoacidos",   
                    "whey-protein": "whey-protein",
                    "creatine": "creatina"
                }
            
        return self.params
