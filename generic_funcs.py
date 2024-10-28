import requests
from PIL import Image, ImageDraw
import os
import json

class funcs:
    def getMotivationMessage(self):
        url = "https://inspirational-quote-generator.p.rapidapi.com/quoteGenerator"

        headers = {
            "x-rapidapi-key": "4f96e03eb6msh9eefc2d7a1d7e2cp12f686jsn6513a410c92a",
            "x-rapidapi-host": "inspirational-quote-generator.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)

        return response.json()
    
    def getIconImg(self, input_image_path):  
        input_dir = input_image_path
        output_dir ="C:\\Users\\Parafal\\Documents\\Output_Path"


        os.makedirs(output_dir, exist_ok=True)
        
        for i, filename in enumerate(os.listdir(input_dir)):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')):
                input_image = Image.open(os.path.join(input_dir, filename)).convert("RGB")
                input_image_resized = input_image.resize((160, 160))
                width, height = input_image_resized.size
                mask = Image.new('L', (width, height), 0)
                draw = ImageDraw.Draw(mask)
                radius = 77
                
                circle_bbox = (width // 2 - radius, height // 2 - radius, width // 2 + radius, height // 2 + radius)
                draw.ellipse(circle_bbox, fill=255)
                
                input_image_resized.putalpha(mask)
                

                output_name = f'{i}-ABOBORA.png'

                input_image_resized.save(os.path.join(output_dir, output_name), "PNG") 

    def getNews(self):
        url = "https://api.nytimes.com/svc/search/v2/articlesearch.json?q=powerlifting&api-key=ZILCSZHbyPDyAnFlhSTBc2ccXhIOf3KH"
        
        response = requests.get(url)
        data = response.json()
        
        first_doc = data["response"]["docs"][0]
        
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


        
        

