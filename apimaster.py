from product_scraper import *
from SQLiteOperations import Operations

class Commands:
    def __init__(self):
        self.operation = Operations()
        self.response = All()
        self.categories = []
        
    def Start(self):
        self.categories = self.operation.SelectCategories
        for category in self.categories:
            self.response.set(category)
            

instance = Commands()
instance.Start()
