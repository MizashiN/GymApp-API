from flask import Flask, jsonify, request
from funcs import Products

app = Flask(__name__)

funcs_instance = Products()

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
        
        response = funcs_instance.getMaxTitanium(category, subcategory)

        return jsonify(response)
    @app.route('/adaptogen', methods=['GET'])
    def get_supp_Adaptogen():
        
        category = request.args.get('category')
        subcategory = request.args.get('subcategory')
        
        response = funcs_instance.getAdaptogen(category, subcategory)

        return jsonify(response)
    @app.route('/proteins', methods=['GET'])
    def get_supp_proteins():
        
        response = funcs_instance.getProteins()

        return jsonify(response)
    
    
if __name__ == '__main__':
    app.run(debug=True)