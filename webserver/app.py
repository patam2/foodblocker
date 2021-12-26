from flask import Flask, request, jsonify
from pymongo import MongoClient


MONGODB_IP = '127.0.0.1'
MONGODB_PORT = 27017 #TODO: env

mongo_client = MongoClient(host=MONGODB_IP, port=MONGODB_PORT).filter.selver_products
flask_client = Flask(__name__)


@flask_client.route('/', methods=['POST'])
def landing(): #POST {'urls':[''], 'forbidden': ['']}
    out = {}

    for url in request.json['urls']:
        out[url] = []
        result = mongo_client.find_one({'url_path': url})

        for ingredient in request.json['forbidden']:
            if ingredient in result['ingrediens']:
                out[url].append(ingredient)

    return jsonify(out)

flask_client.run()