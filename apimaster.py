from flask import Flask, jsonify, request
from funcs import funcs

app = Flask(__name__)

funcs_instance = funcs()

class API(funcs):
    @app.route('/motivationmessage', methods=['GET'])
    def get_message():
        response = funcs_instance.GetMotivationMessage()
        
        author = response.get("author", "Unknown")
        quote = response.get("quote", "No quote available")

        return jsonify({"author": author, "quote": quote})
    
    @app.route('/maxtitanium', methods=['GET'])
    def get_supp_MaxTitanium():
        
        category = request.args.get('category')
        subcategory = request.args.get('subcategory')
        
        response = funcs.MaxTitanium(category, subcategory)

        return jsonify(response)
    @app.route('/adaptogen', methods=['GET'])
    def get_supp_Adaptogen():
        
        category = request.args.get('category')
        subcategory = request.args.get('subcategory')
        
        response = funcs.Adaptogen(category, subcategory)

        return jsonify(response)
    @app.route('/proteins', methods=['GET'])
    def get_supp_proteins():
        
        response = funcs.proteins()

        return jsonify(response)
    
    
if __name__ == '__main__':
    app.run(debug=True)