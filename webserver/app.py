from flask import Flask, request, jsonify
from pymongo import MongoClient
import time


MONGODB_IP = '127.0.0.1'
MONGODB_PORT = 27017 #TODO: env

mongo_client = MongoClient(host=MONGODB_IP, port=MONGODB_PORT).filter.selver_products
flask_client = Flask(__name__)



@flask_client.route('/', methods=['POST'])
def landing(): #POST {'urls':[''], 'forbidden': ['']}
    t = time.time()
    out = {}

    for enum, url in enumerate(request.json['urls']):
        if url.startswith('https'):
            url = url.split('/')[-1]

        out[enum] = []
        result = mongo_client.find_one({'url_path': url})
        for ingredient in request.json['forbidden']:
            if (ingredient in result['ingrediens'] 
                    or ingredient in result['allergens']):
                out[enum].append(ingredient)
    #print(out)
    resp = jsonify(out)
    print(f'Request finished in {time.time()-t:.3f}s')
    return resp

@flask_client.after_request
def apply_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response

flask_client.run()