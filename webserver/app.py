from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pymongo import MongoClient
import time


MONGODB_IP = '127.0.0.1'
MONGODB_PORT = 27017 #TODO: env

mongo_client = MongoClient(host=MONGODB_IP, port=MONGODB_PORT).filter.selver_products
flask_client = Flask(__name__)

limiter = Limiter(flask_client, key_func=get_remote_address) #avoid double page loads

@flask_client.route('/', methods=['POST'])
@limiter.limit("1/s")
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