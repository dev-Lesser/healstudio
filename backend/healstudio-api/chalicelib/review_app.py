from chalice import Blueprint
from chalice import Response
import os
from dotenv import load_dotenv
from .utils import utils
import pymongo
import datetime, json
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

review_routes = Blueprint(__name__)

client = pymongo.MongoClient('mongodb://{host}'.format(
    user=DB_USER, password=DB_PASSWORD, host=DB_HOST
))
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

### REVIEW CRUD
@review_routes.route('/reviews/{gymId}', methods=['GET'], cors=True)
def getReviews(gymId):
    collection = db['reviews']
    e = review_routes.current_request.to_dict()
    params = e.get('query_params')
    skip = int(params.get('skip')) if params.get('skip') else 0
    limit = int(params.get('limit')) if params.get('limit') else 5
    user = params.get('user')
    
    sort_by = params.get('sortBy')
    if not sort_by:
        sort_by = 'created_at'
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
        res = list(collection.aggregate([
            {'$match': {'user': user}},
            {'$group': { '_id': None, 'count': { '$sum': 1 } } },
        ]))
        count = res[0]['count'] if res else 0
        return Response(body={
            'results':results,
            'review_count': count,
        },
                headers={'Content-Type': 'application/json'},
                status_code=200)
    ## user 가 없다면 > 모든 user 가 gym 에대한 리뷰를 updated_at 로 소팅하여 가져옴
    if gymId.isdigit():
        
        count = collection.count_documents({"related_gym_id": gymId})
        res = list(collection.find({"related_gym_id": gymId},{"_id":0}).sort([(sort_by,-1)]).skip(skip).limit(limit))
        results = utils.convertDatetime(res)
        return Response(body={
                    'results': results,
                    'review_count': count
                },
                headers={'Content-Type': 'application/json'},
                status_code=200)
    else: return Response(body='error gymId: \t [%s]' % gymId,
                headers={'Content-Type': 'text/html'},
                status_code=200)


@review_routes.route('/review/{gymId}', methods=['POST'], cors=True)
def createReview(gymId):
    collection = db['reviews']
    user_collection = db['users']
    data = json.loads(review_routes.current_request.raw_body.decode())
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
    
@review_routes.route('/review/{gymId}', methods=['PATCH'], cors=True)
def updateReview(gymId):
    collection = db['reviews']
    data = json.loads(review_routes.current_request.raw_body.decode())
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

@review_routes.route('/review/{gymId}', methods=['DELETE'], cors=True)
def deleteReview(gymId):
    collection = db['reviews']
    user_collection = db['users']
    e = review_routes.current_request.to_dict()
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