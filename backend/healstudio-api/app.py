from chalice import Chalice, Response
from chalice import BadRequestError
# from chalicelib import users
import json, os
from dotenv import load_dotenv
import pymongo
import datetime
load_dotenv(verbose=True)
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

client = pymongo.MongoClient('mongodb://{host}'.format(
    user=DB_USER, password=DB_PASSWORD, host=DB_HOST
))
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

app = Chalice(app_name='healstudio-api')

@app.route('/', methods=['GET'], cors=True)
def index():
    return {'hello': 'world'}

# login
@app.route('/login', methods=['POST'], cors=True)
def login():
    data = json.loads(app.current_request.raw_body.decode())
    user_id = data.get('user_id')
    password = data.get('password')
    collection = db['users']
    if collection.find_one({'user': user_id, 'password':password}):
        return Response(body='token',
                    headers={'Content-Type': 'application/json'},
                    status_code=200)
        
    return Response(body='error',
                    headers={'Content-Type': 'application/json'},
                    status_code=400)
    
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

# region
@app.route('/regions', methods=['GET'], cors=True)
def searchRegions():
    collection = db['region']
    regions = collection.distinct('region')
 
    return regions

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
# user
@app.route('/user/{userId}', methods=['GET'], cors=True)
def searchUser(userId):
    collection = db['users']
    user = collection.find_one({'user':userId},{'_id':0, 'ip':0, 'password':0})
    return user

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

@app.route('/reviews/{gymId}', methods=['GET'], cors=True)
def getReviews(gymId):
    collection = db['reviews']
    e = app.current_request.to_dict()
    params = e.get('query_params')
    skip = int(params.get('skip'))
    limit = int(params.get('limit'))
    
    res = list(collection.find({"related_gym_id": gymId},{"_id":0}).sort([('created_at',-1)]).skip(skip).limit(limit))
    results = []
    for i in res:
        item = i
        item['created_at'] = item['created_at'].strftime("%Y-%m-%d %H:%M:%S")
        item['updated_at'] = item['updated_at'].strftime("%Y-%m-%d %H:%M:%S")
        results.append(item)
    return Response(body=results,
            headers={'Content-Type': 'application/json'},
            status_code=200)

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


### REVIEW CRUD
@app.route('/review/{gymId}', methods=['POST'], cors=True)
def createReview(gymId):
    collection = db['reviews']
    data = json.loads(app.current_request.raw_body.decode())
    contents = data.get('contents')
    user_id = data.get('user_id')
    rate_point = data.get('point')
    if contents and user_id and gymId and rate_point:
        res = {
            "id":collection.find_one({"related_gym_id": gymId}, sort=[('id', -1)])['id'] + 1,
            "user": user_id,
            "related_gym_id": gymId,
            "contents": contents,
            "point": rate_point,
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now()
        }
        collection.insert(res)
    

        return Response(body=gymId,
                headers={'Content-Type': 'text/plain'},
                status_code=200)
        
    return Response(body={
                    "error": "평점 및 리뷰를 확인해주세요"
                    },
            headers={'Content-Type': 'application/json'},
            status_code=403)
    
@app.route('/review/{gymId}', methods=['PATCH'], cors=True)
def updateReview(gymId):
    collection = db['reviews']
    data = json.loads(app.current_request.raw_body.decode())
    _id = data.get('id')
    contents = data.get('contents')
    user_id = data.get('user_id')
    rate_point = data.get('point')
    if contents and user_id and gymId and rate_point:
        insert_query = {
            "id": _id,
            "related_gym_id": gymId,
            "user": user_id,
        }
        res = {
            '$set' : {
                "contents": contents,
                "point": rate_point,
                "updated_at": datetime.datetime.now()
            }
        }
        collection.update(insert_query, res)
    

        return Response(body=gymId,
                headers={'Content-Type': 'text/plain'},
                status_code=204)
        
    return Response(body={
                    "error": "평점 및 리뷰를 확인해주세요"
                    },
            headers={'Content-Type': 'application/json'},
            status_code=403)

@app.route('/review/{gymId}', methods=['DELETE'], cors=True)
def deleteReview(gymId):
    collection = db['reviews']
    data = json.loads(app.current_request.raw_body.decode())
    _id = data.get('id')
    contents = data.get('contents')
    user_id = data.get('user_id')
    rate_point = data.get('point')
    if contents and user_id and gymId and rate_point:
        delete_query = {
            "id": _id,
            "related_gym_id": gymId,
            "user": user_id,
        }
        
        collection.delete(delete_query)
    

        return Response(body=gymId,
                headers={'Content-Type': 'text/plain'},
                status_code=204)
        
    return Response(body={
                    "error": "평점 및 리뷰를 확인해주세요"
                    },
            headers={'Content-Type': 'application/json'},
            status_code=403)

