from product_scraper import *
from MySQLOperations import Operations

class Commands:
    def __init__(self):
        self.operation = Operations()
        self.response = Mith()
        
    def Start(self):
        categories = self.operation.SelectCategories()
        for category in categories:
            
            self.response.set(category[1].lower())
            

instance = Commands()
instance.Start()
