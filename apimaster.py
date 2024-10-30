from flask import Flask, jsonify, request
from product_scraper import *
from generic_funcs import funcs


app = Flask(__name__)

funcs_instance = funcs()

class API():
    

    
    @app.route('/motivationmessage', methods=['GET'])
    def get_message():
        response = funcs_instance.getMotivationMessage()
        
        author = response.get("author", "Unknown")
        quote = response.get("quote", "No quote available")

        return jsonify({"author": author, "quote": quote})
    
    @app.route('/maxtitanium', methods=['GET'])
    def get_supp_MaxTitanium():
        
        
        category = request.args.get('category')
        subcategory = request.args.get('subcategory', "")
        
        response = MaxTitanium()
        result = response.set(category, subcategory)

        return jsonify(result)
    
    @app.route('/adaptogen', methods=['GET'])
    def get_supp_Adaptogen():
        
        category = request.args.get('category')
        subcategory = request.args.get('subcategory')
        
        response = Adaptogen()
        result = response.set(category, subcategory)

        return jsonify(result)
    @app.route('/all', methods=['GET'])
    def get_supp_proteins():
        
        category = request.args.get('category')
        subcategory = request.args.get('subcategory')
        
        response = All()
        result = response.set(category, subcategory)

        return jsonify(result)
    
    @app.route('/news', methods=['GET'])
    def get_news():
        
        response = funcs_instance.getNews()
        
        return jsonify(response)
    
    @app.route('/getImgIcon', methods=['POST'])
    def get_imgicon():
        
        file = request.args.get('file')
        response = funcs_instance.getIconImg(file)
        
        return jsonify(response)
    
if __name__ == '__main__':
    app.run(debug=True)