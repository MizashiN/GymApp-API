from bs4 import BeautifulSoup
from dataclasses import dataclass
import requests

@dataclass
class dataclass:
    title: str
    price: str
    image_src: str
class brands:
    brands = ["MaxTitanium", "Adaptogen"]
class defaultsets:
    def MaxTitaniumSet(urls):
        product_list = []  # Inicializa a lista de produtos
        
        for url in urls:
            res = requests.get(url)

            # Verifica se a requisição foi bem-sucedida
            if res.status_code != 200:
                continue  # Se falhar, pula para a próxima URL

            # Analisa o conteúdo HTML retornado
            soup = BeautifulSoup(res.content, "html.parser")

            # Encontra todos os artigos de produto na página
            product_items = soup.find_all('article', class_='product-card aud-flex aud-flex-col aud-h-full aud-relative aud-duration-300 aud-border-transparent aud-group hoverWishlist hoverZoom hoverShadow')

            for product_info in product_items:
                title = product_info.find("h3", class_="product-card__title aud-text-sm")
                price = product_info.find("div", class_="aud-font-semibold")
                image = product_info.find("img", class_="product-card__img mobile-only:aud-h-[var(--mobile-image-height)] lg:aud-h-[var(--desk-image-height)] product-card__img--first lg:aud-transition-all lg:aud-duration-300 aud-object-contain aud-w-full")

                if not image:
                    image = product_info.find("img", class_="product-card__img mobile-only:aud-h-[var(--mobile-image-height)] lg:aud-h-[var(--desk-image-height)] aud-object-contain aud-w-full")
                
                if title and price and image:
                    title_text = title.get_text(strip=True)
                    price_text = price.get_text(strip=True).replace('\u00a0', '').replace('R$', 'R$ ').strip()
                    image_src = image.get('src')
                    
                    product_list.append(dataclass(title=title_text, price=price_text, image_src=image_src))
        
        result = {
            f"total{brands.brands}": len(product_list),
            f"products{brands.brands}": product_list
        }
        
        return result
    
    def AdaptogenSet(urls):
        product_list = [] 
        
        for url in urls:
            res = requests.get(url)

            # Verifica se a requisição foi bem-sucedida
            if res.status_code != 200:
                continue  # Se falhar, pula para a próxima URL

                # Analisa o conteúdo HTML retornado
            soup = BeautifulSoup(res.content, "html.parser")

                # Encontra todos os artigos de produto na página
            product_items = soup.find_all('a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link')

                # Itera por cada item encontrado
            for product_info in product_items:
                title = product_info.find("h2", class_="woocommerce-loop-product__title")
                price = product_info.find("p")
                image = product_info.find("img")

                if title and price and image:
                    title_text = title.get_text(strip=True)
                    price_text = price.get_text(strip=True).replace('\u00a0', '').replace('R$', 'R$ ').strip()
                    image_src = image.get('src')
                        
                    product_list.append(dataclass(title=title_text, price=price_text, image_src=image_src))
                    
        result = {
            f"total{brands.brands}": len(product_list),
            f"products{brands.brands}": product_list
        }
        
        return result
    
    
class funcs:
    product_list = []
    
    def MaxTitanium(category, subcategory):
        if category == "proteinas" and subcategory == "":
            urls = [
                "https://www.maxtitanium.com.br/produtos/proteinas?filter.category-1=produtos&filter.category-2=proteinas&filter.category-3=concentrada",
                "https://www.maxtitanium.com.br/produtos/proteinas?filter.category-1=produtos&filter.category-2=proteinas&filter.category-3=3w",
                "https://www.maxtitanium.com.br/produtos/proteinas?filter.category-1=produtos&filter.category-2=proteinas&filter.category-3=blend-de-proteinas",
                "https://www.maxtitanium.com.br/produtos/proteinas?filter.category-1=produtos&filter.category-2=proteinas&filter.category-3=proteina-vegetal",
                "https://www.maxtitanium.com.br/produtos/proteinas?filter.category-1=produtos&filter.category-2=proteinas&filter.category-3=isolada"
            ]
            product_list = defaultsets.MaxTitaniumSet(urls)

        elif category and subcategory == "":
            urls = [
                f"https://www.maxtitanium.com.br/s?q={category}"
            ]
            product_list = defaultsets.MaxTitaniumSet(urls)

        return product_list
    
    def Adaptogen(category, subcategory):
        # URLs para a categoria de proteínas
        if category == "proteinas" and subcategory == "":
            urls = [
                "https://adaptogen.com.br/proteinas/?orderby=popularity&paged=1&_sft_product_cat=proteinas"
            ]
            product_list = defaultsets.AdaptogenSet(urls)
                        
        elif category == "proteinas" and subcategory:
            urls = [
                f"https://adaptogen.com.br/proteinas/?orderby=popularity&paged=1&_sft_product_cat={subcategory}"
            ]
            product_list = defaultsets.AdaptogenSet(urls)

        return product_list
    
    def proteins():
        product_list = []  # Reinicializa a lista para evitar duplicação
        total = 0
        
        for brand in brand.brands:
            brandFunc = getattr(funcs, brand, None)

            product = brandFunc("proteinas","")
            product_count = product[f"total{brand}"]


            product_list.append(product)
            total += product_count

        # Criar o dicionário com os produtos
        result = {
            "totalProducts": total,  # Soma dos totais de cada marca
            "products": product_list
        }

        return result  # Retorne o resultado
    
    def GetMotivationMessage():
        url = "https://inspirational-quote-generator.p.rapidapi.com/quoteGenerator"

        headers = {
            "x-rapidapi-key": "4f96e03eb6msh9eefc2d7a1d7e2cp12f686jsn6513a410c92a",
            "x-rapidapi-host": "inspirational-quote-generator.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)

        return response.json()
    
funcs.proteins()
