import requests
from PIL import Image, ImageDraw
import io

class funcs:
    def getMotivationMessage(self):
        url = "https://inspirational-quote-generator.p.rapidapi.com/quoteGenerator"

        headers = {
            "x-rapidapi-key": "4f96e03eb6msh9eefc2d7a1d7e2cp12f686jsn6513a410c92a",
            "x-rapidapi-host": "inspirational-quote-generator.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)

        return response.json()
    
    def get_icon_img(self, input_image_path):  
        input_image = Image.open(input_image_path).convert("RGB")
        input_image_resized = input_image.resize((200, 200))
        width, height = input_image_resized.size
        mask = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(mask)
        radius = 98

        circle_bbox = (width // 2 - radius, height // 2 - radius, width // 2 + radius, height // 2 + radius)
        draw.ellipse(circle_bbox, fill=255)
        
        input_image_resized.putalpha(mask)

        # Converter a imagem para blob
        image_blob = io.BytesIO()
        input_image_resized.save(image_blob, format="PNG")
        image_blob.seek(0)  # Voltar para o início do arquivo

        return image_blob.getvalue()

    def getNews(self):
        url = "https://api.nytimes.com/svc/search/v2/articlesearch.json?q=health&api-key=ZILCSZHbyPDyAnFlhSTBc2ccXhIOf3KH"
        
        response = requests.get(url)
        data = response.json()
        
        first_doc = data["response"]["docs"][4]
        
        title = first_doc["headline"]["main"]
        paragraph = first_doc["lead_paragraph"]
        article_url = first_doc["web_url"]        
        
        result = {
            "title": title,
            "paragraph": paragraph,
            "url": article_url
        }
    
    # Convertendo o dicionário para JSON
        return result
