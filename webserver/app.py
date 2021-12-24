from flask import Flask, request
from pymongo import MongoClient


MONGODB_IP = '127.0.0.1'
MONGODB_PORT = 27017 #TODO: env

mongo_client = MongoClient(host=MONGODB_IP, port=MONGODB_PORT)
flask_client = Flask(__name__)


@flask_client.route('/', methods=['POST'])
def landing():
    pass

flask_client.run()