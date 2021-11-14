from chalice import Blueprint
from chalice import Response
import bcrypt
import requests
import json, datetime, os
from .authorize import auth
from dotenv import load_dotenv

import pymongo

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

auth_routes = Blueprint(__name__)

client = pymongo.MongoClient('mongodb://{host}'.format(
    user=DB_USER, password=DB_PASSWORD, host=DB_HOST
))
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# login
@auth_routes.route('/auth/login', methods=['POST'], cors=True)
def login():
    data = json.loads(auth_routes.current_request.raw_body.decode())
    user_id = data.get('user_id')
    password = data.get('password')
    collection = db['users']
    bytes_password = bytes(password, 'utf-8')

    data = collection.find_one({'user': user_id})
    if not bcrypt.checkpw(bytes_password, data.get('password')):
        return Response(body='error',
                    headers={'Content-Type': 'application/json'},
                    status_code=400)

    collection.update_one({ 'user': user_id }, {'$set' : {
                "last_login": datetime.datetime.now()}
            })
    if data:
        return Response(body={
            'token': data.get('uuid'),
            'user_id': data.get('user'),
            },
                    headers={'Content-Type': 'application/json'},
                    status_code=200)
        
    return Response(body='error',
                    headers={'Content-Type': 'application/json'},
                    status_code=400)


@auth_routes.route('/auth/signup', methods=['POST'], cors=True)
def signup():
    data = json.loads(auth_routes.current_request.raw_body.decode())
    user_id = data.get('user_id')
    password = data.get('password')
    
    bytes_password = bytes(password, 'utf-8') #// 비밀번호
    hashed_password = bcrypt.hashpw(password=bytes_password, salt=bcrypt.gensalt())
    if not auth.auth_check(user_id, password):
        return Response(body='error',
                    headers={'Content-Type': 'application/json'},
                    status_code=400)
    collection = db['users']
    data = collection.find_one({'user': user_id}) # id 체크
    if data:
        return Response(body='error',
                    headers={'Content-Type': 'application/json'},
                    status_code=400)
    ip = requests.get("https://api.ipify.org").text
    uid = auth.create_uuid(user_id, password, ip)
    admin = False
    results = {
        'user': user_id,
        'uuid': uid,
        'password': hashed_password,
        'ip': ip,
        'admin': admin,
        'favList': [],
        'reviews':[],
        "created_at": datetime.datetime.now(),
        "last_login": datetime.datetime.now()
    }
    collection.insert_one(results)
    return Response(body={
        'token':uid,
        'user_id': user_id,
        },
        headers={'Content-Type': 'application/json'},
        status_code=200)
        
    
    