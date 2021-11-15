from chalice import Chalice, Response
from chalice import BadRequestError
# from chalicelib import users
import json, os

import pymongo

from chalicelib.authorize import auth
from chalicelib.auth_app import auth_routes
from chalicelib.review_app import review_routes
from chalicelib.board_app import board_routes


from pathlib import Path
from dotenv import load_dotenv

basepath = Path()
basedir = str(basepath.cwd())
envars = basepath.cwd() / 'chalicelib/.env'
load_dotenv(envars)

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

# client = pymongo.MongoClient('mongodb+srv://{user}:{password}@{host}'.format(
#     user=DB_USER, password=DB_PASSWORD, host=DB_HOST
# ))
client = pymongo.MongoClient('mongodb://localhost:27017'.format(
    user=DB_USER, password=DB_PASSWORD, host=DB_HOST
))
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

app = Chalice(app_name='healstudio-api')
### AUTH API
app.register_blueprint(auth_routes) 
### REVIEW API
app.register_blueprint(review_routes) 
### BOARD API
app.register_blueprint(board_routes) 

@app.route('/search', methods=['GET'], cors=True)
def searchByQuery():
    collection = db['space']
    
    e = app.current_request.to_dict()
    params = e.get('query_params')
    query = str(params.get('query')).strip()
    if query!="" and len(query)< 2: # 1글자 미만 error
        return Response(
            body='텍스트 길이는 두자 이상 입력해주세요',
            headers={'Content-Type': 'text/html'},
            status_code=400
        )
        
    skip = int(params.get('skip'))
    limit = int(params.get('limit'))
    if limit >= 100:
        raise BadRequestError('error')
    if query != '':
        res = list(collection.find({"$text": {"$search": query}},{"_id":0,"checkParse":0}).skip(skip).limit(limit))
    else: res = list(collection.find({},{"_id":0, "checkParse":0}).skip(skip).limit(limit))
    return Response(body=res,
            headers={'Content-Type': 'application/json'},
            status_code=200)

# meta data
@app.route('/regions', methods=['GET'], cors=True)
def searchRegions():
    collection = db['region']
    regions = collection.distinct('region')
 
    return regions

# region
@app.route('/metadata', methods=['GET'], cors=True)
def getMeta():
    board_collection    = db['board']
    user_collection     = db['users']
    space_collection    = db['space']
    trainers_collection = db['board']
    review_collection   = db['reviews']
    find_board = {"type":"board"}
    find_reply = {"type": "reply"}
    find_all = {}
    board_count = board_collection.count_documents(find_board)
    reply_count = board_collection.count_documents(find_reply)
    user_count = user_collection.count_documents(find_all)
    space_count = space_collection.count_documents(find_all)
    trainer_count = trainers_collection.count_documents(find_all)
    review_count = review_collection.count_documents(find_all)
    results = {
        'board': board_count,
        'reply': reply_count,
        'user' : user_count,
        'space': space_count,
        'trainer': trainer_count,
        'review': review_count
    }
    return Response(body=results,
                headers={'Content-Type': 'application/json'},
                status_code=200)

@app.route('/region', methods=['GET'], cors=True)
def searchRegionDetail():
    collection = db['region']
    e = app.current_request.to_dict()
    params = e.get('query_params')
    sido = params.get('sido')
    sigungu = params.get('sigungu')
    if sigungu != None:
        regions = list(collection.find({
            'region': sido, 
            'depth1': sigungu
            },{'_id':0}))

        return regions
    regions = list(collection.find({'region': sido},{'_id':0}))

    return regions


@app.route('/gym/{gymId}', methods=['GET'], cors=True)
def searchByGymId(gymId):
    res = collection.find_one({"id": gymId},{"_id":0, "checkParse":0})
    return res


@app.route('/gym', methods=['POST'], content_types=['application/json'], cors=True)
def createGym():
    data = app.current_request.raw_body.decode()
    data['checkParse'] = False
    if collection.find_one({"id": data['id']}):
        raise BadRequestError('id %s exists' % data['id'])
    
    
    response = {
            "data" : data
    }
    return response

@app.route('/gyms-lists', methods=['GET'], cors=True)
def search():
    e = app.current_request.to_dict()
    params = e.get('query_params')
    skip = int(params.get('skip'))
    limit = int(params.get('limit'))
    if limit >= 100:
        raise BadRequestError('error')

    res = list(collection.find({},{"_id":0, "checkParse":0}).skip(skip).limit(limit))

    return res


@app.route('/trainers/{gymId}', methods=['GET'], cors=True)
def getTrainers(gymId):
    collection = db['trainers']
    e = app.current_request.to_dict()
    params = e.get('query_params')
    skip = int(params.get('skip'))
    limit = int(params.get('limit'))
    
    res = list(collection.aggregate([
        {'$unwind': "$related_gym_ids"},
        {'$match': {"related_gym_ids": gymId}},
        {'$skip' : skip},
        {'$limit': limit},
        {'$project': {'_id':0, 'created_at':0, 'updated_at':0}}
    ]))
    
    return Response(body=res,
            headers={'Content-Type': 'application/json'},
            status_code=200)

@app.route('/user/{user_id}', methods=['GET'], cors=True)
def getUserDetails(user_id):
    collection = db['users']
    e = app.current_request.to_dict()
    params = e.get('query_params')
    uid = params.get('uid')
    skip = int(params.get('skip')) if params.get('skip') else 0
    limit = int(params.get('limit')) if params.get('limit') else 5
    if user_id and uid:
        results = collection.aggregate([
                {'$match': {'user': user_id, 'uuid': uid}},
                {'$unwind': '$favList'},
                {'$skip': skip}, {'$limit':limit},
                {'$lookup': {'from':'space', 'localField':'favList', 'foreignField':'id', 'as':'gymInfo'}}, # join
                {'$unwind': '$gymInfo'}, # 반드시 하나
                {'$project': { '_id':0, 'password':0, 'admin':0,'uuid':0, 'reviews':0,
                            'gymInfo._id':0,'gymInfo.desc':0, 'gymInfo.urlList':0, 'gymInfo.checkParse':0,
                            'gymInfo.x':0, 'gymInfo.y':0,'gymInfo.imgList':0,
                            }},
            ])
        res = list(collection.aggregate([
                {'$match': {'user': user_id, 'uuid': uid}},
                {'$unwind': '$favList'},
                {'$group': { '_id': None, 'count': { '$sum': 1 } } },
        ]))
        
        count = res[0]['count'] if res else 0
        
        results_bucket = list()
        user_info = collection.find_one({'user':user_id, 'uuid': uid},{'_id':0,'uuid':0,'password':0, 'admin':0})
        user_info['ip'] = auth.hidden_ip(user_info['ip'])
        user_info['created_at'] = user_info['created_at'].strftime('%Y-%m-%d')
        user_info['last_login'] = user_info['last_login'].strftime('%Y-%m-%d')
        for i in results:
            item = i
            item['created_at'] = i['created_at'].strftime('%Y-%m-%d')
            item['last_login'] = i['last_login'].strftime('%Y-%m-%d')
            item['ip'] = auth.hidden_ip(i['ip'])
            results_bucket.append(item)
        return Response(body={
            'user': user_info,
            'results':results_bucket,
            'fav_count': count
            },
                headers={'Content-Type': 'application/json'},
                status_code=200)
        
    return Response(body={
                    "error": "error"
                    },
            headers={'Content-Type': 'application/json'},
            status_code=403)

@app.route('/favorite/{gymId}', methods=['GET','POST'], cors=True)
def handleFavorite(gymId):
    collection = db['users']
    if app.current_request.method == 'GET':
        e = app.current_request.to_dict()
        params = e.get('query_params')
        user_id = params.get('user_id')
        uid = params.get('uid')
        res = collection.find_one(
            {'user': user_id, 'uuid': uid, 'favList': { '$in': [gymId] }} # 있으면 찜한 목록이기 때문에 pull 함
        )
        if res:
            return Response(body=True,
                headers={'Content-Type': 'application/json'},
                status_code=200)
        else:
            return Response(body=False,
                headers={'Content-Type': 'application/json'},
                status_code=200)
    elif app.current_request.method == 'POST':
        data = json.loads(app.current_request.raw_body.decode())
        user_id = data.get('user_id')
        uid = data.get('uid')
        if user_id and uid:
            query = {
                'user': user_id,
                'uuid': uid,
            }
            res = collection.find_one(
                {'user': user_id, 'uuid': uid, 'favList': { '$in': [gymId] }} # 있으면 빼고 없으면 넣어라
            )
            if not res:
                collection.update_one(query, {'$push': {'favList': gymId}})
            else:
                collection.update_one(query, {'$pull': {'favList': gymId}})
            return Response(body=gymId,
                    headers={'Content-Type': 'application/json'},
                    status_code=200)
            
        return Response(body={
                        "error": "error"
                        },
                headers={'Content-Type': 'application/json'},
                status_code=403)


