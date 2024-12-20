from flask import Flask, jsonify, request
from product_scraper import *
from generic_funcs import funcs


app = Flask(__name__)

funcs_instance = funcs()


class API:
    @app.route("/maxtitanium", methods=["GET"])
    def get_supp_MaxTitanium():

        category = request.args.get("category")
        subcategory = request.args.get("subcategory", "")

        response = MaxTitanium()
        result = response.set(category, subcategory)

        return jsonify(result)

    @app.route("/adaptogen", methods=["GET"])
    def get_supp_Adaptogen():

        category = request.args.get("category")
        subcategory = request.args.get("subcategory")

        response = Adaptogen()
        result = response.set(category, subcategory)

        return jsonify(result)

    @app.route("/darklab", methods=["GET"])
    def get_supp_Darklab():

        category = request.args.get("category")
        subcategory = request.args.get("subcategory")

        response = DarkLab()
        result = response.set(category, subcategory)

        return jsonify(result)
    @app.route("/mith", methods=["GET"])
    def get_supp_Mith():

        category = request.args.get("category")
        subcategory = request.args.get("subcategory")

        response = Mith()
        result = response.set(category, subcategory)

        return jsonify(result)

    @app.route("/growthsupp", methods=["GET"])
    def get_supp_GrowthSupp():

        category = request.args.get("category")
        subcategory = request.args.get("subcategory")

        response = GrowthSupp()
        result = response.set(category, subcategory)

        return jsonify(result)
    
    @app.route("/darkness", methods=["GET"])
    def get_supp_Darkness():

        category = request.args.get("category")
        subcategory = request.args.get("subcategory")

        response = Darkness()
        result = response.set(category, subcategory)

        return jsonify(result)
    

    @app.route("/all", methods=["GET"])
    def get_supp_proteins():

        category = request.args.get("category")
        subcategory = request.args.get("subcategory")

        response = All()
        result = response.set(category, subcategory)

        return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
