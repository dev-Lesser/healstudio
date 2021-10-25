from chalice import Chalice, Response
from chalice import BadRequestError
# from chalicelib import users
import json, os
from dotenv import load_dotenv

import requests
import pymongo
import datetime
import bcrypt
from authorize import auth
from utils import utils
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

# login
@app.route('/auth/login', methods=['POST'], cors=True)
def login():
    data = json.loads(app.current_request.raw_body.decode())
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


@app.route('/auth/signup', methods=['POST'], cors=True)
def signup():
    data = json.loads(app.current_request.raw_body.decode())
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

@app.route('/reviews/{gymId}', methods=['GET'], cors=True)
def getReviews(gymId):
    collection = db['reviews']
    e = app.current_request.to_dict()
    params = e.get('query_params')
    skip = int(params.get('skip')) if params.get('skip') else 0
    limit = int(params.get('limit')) if params.get('limit') else 5
    user = params.get('user')
    
    sort_by = params.get('sortBy')
    if not sort_by:
        sort_by = 'updated_at'
    if user and gymId=='all': # 유저가 쓴 것만 가져올 수 있음
        res = list(collection.aggregate([
            {'$match': {'user': user}},
            {'$sort': { sort_by: -1 }},  # [TODO] 디스크 에러 날 경우 어떻게???
            {'$skip': skip}, {'$limit':limit},
            {'$lookup': {'from':'space', 'localField':'related_gym_id', 'foreignField':'id', 'as':'gymInfo'}}, # join
            {'$unwind': '$gymInfo'}, # 반드시 하나
            {'$project': { '_id':0, 'gymInfo._id':0, 'gymInfo.desc':0, 'gymInfo.checkParse':0, 'gymInfo.urlList':0,
                        'gymInfo.x':0,'gymInfo.y':0}},
            
            
        ]))
        results = utils.convertDatetime(res)
        return Response(body=results,
                headers={'Content-Type': 'application/json'},
                status_code=200)
    ## user 가 없다면 > 모든 user 가 gym 에대한 리뷰를 updated_at 로 소팅하여 가져옴
    if gymId.isdigit():
        res = list(collection.find({"related_gym_id": gymId},{"_id":0}).sort([(sort_by,-1)]).skip(skip).limit(limit))
        results = utils.convertDatetime(res)
        return Response(body=results,
                headers={'Content-Type': 'application/json'},
                status_code=200)
    else: return Response(body='error gymId: \t [%s]' % gymId,
                headers={'Content-Type': 'text/html'},
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
    user_collection = db['users']
    data = json.loads(app.current_request.raw_body.decode())
    contents = data.get('contents')
    if len(contents) > 50:
        return Response(body={
                    "error": "리뷰를 확인해주세요"
                    },
            headers={'Content-Type': 'application/json'},
            status_code=403)
        
    user_id = data.get('user_id')
    rate_point = data.get('point')
    isExist = collection.find_one({"related_gym_id": gymId}, sort=[('id', -1)])
    if isExist:
        review_id_max = isExist.get('id') + 1
    else:
        review_id_max = 1
    if contents and user_id and gymId and rate_point:
        res = {
            "id": review_id_max,
            "user": user_id,
            "related_gym_id": gymId,
            "contents": contents,
            "point": rate_point,
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now()
        }
        collection.insert(res)
        user_collection.update_one({"user": user_id},{'$push': {'reviews': {'review_id':review_id_max, 'gym_id': gymId}}})

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
    if len(contents) > 50:
        return Response(body={
                    "error": "리뷰를 확인해주세요"
                    },
            headers={'Content-Type': 'application/json'},
            status_code=403)
    user_id = data.get('user_id')
    rate_point = data.get('point')
    if contents and user_id and gymId and rate_point and _id:
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
    user_collection = db['users']
    e = app.current_request.to_dict()
    params = e.get('query_params')
    _id = int(params.get('id'))
    user_id = params.get('user_id')
    if user_id and gymId and _id:
        delete_query = {
            "id": _id,
            "related_gym_id": gymId,
            "user": user_id,
        }
        
        collection.delete_one(delete_query)
        user_collection.update_one(
            {'user': user_id},
            {'$pull': {'reviews': {'review_id':_id, 'gym_id': gymId}}}
        )
        return Response(body=gymId,
                headers={'Content-Type': 'text/plain'},
                status_code=200)
        
    return Response(body={
                    "error": "평점 및 리뷰를 확인해주세요"
                    },
            headers={'Content-Type': 'application/json'},
            status_code=403)

@app.route('/user/{user_id}', methods=['GET'], cors=True)
def getUserDetails(user_id):
    collection = db['users']
    e = app.current_request.to_dict()
    params = e.get('query_params')
    uid = params.get('uid')
    skip = int(params.get('skip')) if params.get('skip') else 0
    limit = int(params.get('limit')) if params.get('limit') else 10
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
            'results':results_bucket
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

@app.route('/boards', methods=['GET'], cors=True)
def getBoards():
    collection = db['board']
    if app.current_request.method == 'GET':
        e = app.current_request.to_dict()
        params = e.get('query_params')
        # print(params)
        skip = int(params.get('skip')) if params.get('skip') else 0;
        limit = int(params.get('limit')) if params.get('limit') else 12;
        res = collection.find(
            {'type':'board'},{'_id':0} # 있으면 찜한 목록이기 때문에 pull 함
        ).sort([('updated_at',-1)]).skip(skip).limit(limit)
        r = utils.convertDatetime(res)
        return Response(body=r,
            headers={'Content-Type': 'application/json'},
            status_code=200)
@app.route('/board/{_id}', methods=['GET'], cors=True)
def getBoard(_id):
    collection = db['board']
    if app.current_request.method == 'GET':
        e = app.current_request.to_dict()
        params = e.get('query_params')
        user = params.get('user')
        skip = int(params.get('skip')) if params.get('skip') else 0;
        limit = 15
        board = collection.find_one(
            {'id': int(_id),'user':user,'type':'board'},{'_id':0, 'related_id':0, 'type':0} # 있으면 찜한 목록이기 때문에 pull 함
        )
        res = collection.find(
            {'related_id': user+':'+_id,'type':'reply'},{'_id':0, 'related_id':0} # 있으면 찜한 목록이기 때문에 pull 함
        ).sort([('created_at', 1)]).skip(skip).limit(limit)
        r = utils.convertDatetime(res)
        board['created_at'] = board['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        board['updated_at'] = board['updated_at'].strftime('%Y-%m-%d %H:%M:%S')
        
        return Response(body={
            'contents':board,
            'replies': r
            },
            headers={'Content-Type': 'application/json'},
            status_code=200)
        
    
@app.route('/board', methods=['POST'], cors=True)
def postBoard():
    collection = db['board']
    user_collection = db['users']
    data = json.loads(app.current_request.raw_body.decode())
    user_id = data.get('user_id')
    uid = data.get('uid')
    title = data.get('title')
    contents = data.get('contents')
    if len(title.strip()) < 2 or len(contents.strip())> 30:
        return Response(body='too large 30, too small 2',
        headers={'Content-Type': 'text/html'},
        status_code=403)
    if len(contents.strip()) <10 or len(contents.strip())> 500:
        return Response(body='too large 500, too small 10',
        headers={'Content-Type': 'text/html'},
        status_code=403)

    if not user_collection.find_one({"user":user_id, "uuid": uid}):
        return Response(body='uuid is required',
        headers={'Content-Type': 'text/html'},
        status_code=403)
    
        
    isExist = collection.find_one({"type": "board"}, sort=[('id', -1)])
    if isExist:
        _id = isExist.get('id') + 1
    else:
        _id = 1
    collection.insert_one({
        'user': user_id,
        'title': title.strip(),
        'contents': contents.strip(),
        'id': _id,
        'related_id': user_id + ':' + str(_id),
        'favorites': 0,
        'type': 'board',
        'created_at': datetime.datetime.now(),
        'updated_at': datetime.datetime.now()

    })
    return Response(body=_id,
        headers={'Content-Type': 'application/json'},
        status_code=201)
    
