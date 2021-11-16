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

board_routes = Blueprint(__name__)

client = pymongo.MongoClient('mongodb://{host}'.format(
    user=DB_USER, password=DB_PASSWORD, host=DB_HOST
))
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


@board_routes.route('/boards', methods=['GET'], cors=True)
def getBoards():
    collection = db['board']
    if board_routes.current_request.method == 'GET':
        e = board_routes.current_request.to_dict()
        params = e.get('query_params')
        skip = int(params.get('skip')) if params.get('skip') else 0;
        limit = int(params.get('limit')) if params.get('limit') else 12;
        user = params.get('user')
        if user: # user 페이지
            res = collection.find(
                {'user': user, 'type':'board', 'isDeleted': {'$ne': True}},{'_id':0, 'contents':0} # 있으면 찜한 목록이기 때문에 pull 함
            ).sort([('created_at',-1)]).skip(skip).limit(limit) # user 페이지
            r = utils.convertDatetimeHours(res)
            res = list(collection.aggregate([
                {'$match': {'user': user, 'type':'board','isDeleted': {'$ne': True}}},
                {'$group': { '_id': None, 'count': { '$sum': 1 } } },
            ]))
            count = res[0]['count'] if res else 0
            return Response(body={
                'results': r,
                'board_count':count
                },
                headers={'Content-Type': 'application/json'},
                status_code=200)
        else: # 전체 게시판 조회 페이지
            res = collection.aggregate([
                {'$match':{'type':'board'}},
                {'$sort': {'created_at': -1}},
                {'$skip': skip}, {'$limit': limit},
                {'$project':{
                    '_id': 0,
                    'user': 1,
                    'title': 1,
                    'id': 1,
                    'isDeleted':1,
                    'created_at':1,
                    'updated_at':1,
                    'favorites': {'$cond': {'if': {'$isArray': '$favorites'}, 'then':{'$size':'$favorites'},'else':0}} # Array 형식 get size
                }},
            ])
            r = utils.convertDatetimeHours(res)
            results = []
            for item in r:
                if item.get('isDeleted'):
                    item['title'] = utils.deleteByUser()
                    results.append(item)
                else:
                    results.append(item)
            return Response(body=r,
                headers={'Content-Type': 'application/json'},
                status_code=200)
@board_routes.route('/board/{_id}', methods=['GET'], cors=True)
def getBoard(_id):
    collection = db['board']
    if board_routes.current_request.method == 'GET':
        e = board_routes.current_request.to_dict()
        params = e.get('query_params')
        user = params.get('user')
        skip = int(params.get('skip')) if params.get('skip') else 0;
        limit = 15
        
        board = list(collection.aggregate([
            {'$match':{'id': int(_id), 'user':user,'type':'board'}},
            {'$project':{
                '_id': 0,
                'user': 1,
                'title': 1,
                'id': 1,
                'contents':1,
                'created_at':1,
                'updated_at':1,
                'isDeleted':1,
                'favorites': {'$cond': {'if': {'$isArray': '$favorites'}, 'then':{'$size':'$favorites'},'else':0}}
            }},
        ]))
        if board:
            board = board[0]
        res = collection.find(
            {'id': int(_id),'type':'reply'},{'_id':0, 'related_id':0} # 있으면 찜한 목록이기 때문에 pull 함
        ).sort([('created_at', -1)]).skip(skip).limit(limit)
        r = utils.convertDatetimeHours(res)
        if board.get('isDeleted'):
            board['title'] = utils.deleteByUser()
            board['contents'] = utils.deleteByUser()
        board['created_at'] = board['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        board['updated_at'] = board['updated_at'].strftime('%Y-%m-%d %H:%M:%S')
        isEnd = True if len(r)<limit else False
        return Response(body={
            'contents':board,
            'replies': r,
            'isEnd': isEnd
            },
            headers={'Content-Type': 'application/json'},
            status_code=200)
        
    
@board_routes.route('/board', methods=['POST'], cors=True)
def postBoard():
    collection = db['board']
    user_collection = db['users']
    data = json.loads(board_routes.current_request.raw_body.decode())
    user_id = data.get('user_id')
    uid = data.get('uid')
    title = data.get('title')
    contents = data.get('contents')
    if len(title.strip()) < 2 or len(title.strip())> 30:
        return Response(body='too large 30, too small 2',
        headers={'Content-Type': 'text/html'},
        status_code=403)
    if len(contents.strip()) <10:
        return Response(body='too small 10',
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
        'id': int(_id),
        'related_id': user_id + ':' + str(_id),
        'favorites': [],
        'type': 'board',
        'created_at': datetime.datetime.now(),
        'updated_at': datetime.datetime.now()

    })
    return Response(body=_id,
        headers={'Content-Type': 'application/json'},
        status_code=201)
    
@board_routes.route('/board', methods=['PATCH'], cors=True)
def patchBoard():
    collection = db['board']
    user_collection = db['users']
    data = json.loads(board_routes.current_request.raw_body.decode())
    user_id = data.get('user_id')
    uid = data.get('uid')
    title = data.get('title')
    contents = data.get('contents')
    _id = data.get('id')
    if len(title.strip()) < 2 or len(title.strip())> 30:
        return Response(body='too large 30, too small 2',
        headers={'Content-Type': 'text/html'},
        status_code=403)
    if len(contents.strip()) <10 :
        return Response(body='too large 500, too small 10',
        headers={'Content-Type': 'text/html'},
        status_code=403)

    if not user_collection.find_one({"user":user_id, "uuid": uid}):
        return Response(body='uuid is required',
        headers={'Content-Type': 'text/html'},
        status_code=403)
        
    collection.update_one(
                            {'user': user_id, 'id':_id, 'type': 'board' }, 
                            {'$set' : {
                                'title': title.strip(),
                                'contents': contents.strip(),
                                'updated_at': datetime.datetime.now()}
                            }
                            )

    return Response(body=_id,
        headers={'Content-Type': 'application/json'},
        status_code=204)
    
@board_routes.route('/board', methods=['DELETE'], cors=True)
def deleteBoard():
    collection = db['board']
    user_collection = db['users']
    e = board_routes.current_request.to_dict()
    params = e.get('query_params')
    user_id = params.get('user_id')
    uid = params.get('uid')
    title = params.get('title')
    _id = int(params.get('id'))


    if not user_collection.find_one({"user":user_id, "uuid": uid}):
        return Response(body='uuid is required',
        headers={'Content-Type': 'text/html'},
        status_code=403)
    collection.update_one({'user': user_id, 'id':_id, 'title':title, 'type': 'board' },
                            {'$set' : {'isDeleted': True,}}
                            )  ### 삭제하였을 경우 isDeleted 라는 변수에 True 를 넣어주자 그래서 리플라이들은 남을수있게

    return Response(body=_id,
        headers={'Content-Type': 'application/json'},
        status_code=200)
    
@board_routes.route('/reply', methods=['POST','DELETE'], cors=True)
def handleReply():
    collection = db['board']
    user_collection = db['users']
    if board_routes.current_request.method == 'POST':
        data = json.loads(board_routes.current_request.raw_body.decode())
        user_id = data.get('user_id')
        uid = data.get('uid')
        _id = data.get('id')
        contents = data.get('contents')
        if len(contents.strip()) <5 or len(contents.strip()) >50 :
            return Response(body='too large 50, too small 5',
                headers={'Content-Type': 'text/html'},
                status_code=403)
        
        if not user_collection.find_one({"user":user_id, "uuid": uid}):
            return Response(body='uuid is required',
                headers={'Content-Type': 'text/html'},
                status_code=403)
        item = {
            'user': user_id,
            'contents': contents,
            'id': int(_id),
            'related_id': user_id + ':' + str(_id),
            'type': 'reply',
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now()
        }
        collection.insert_one(item)
        return Response(body=_id,
            headers={'Content-Type': 'application/json'},
            status_code=201)
    elif board_routes.current_request.method == 'DELETE':
        e = board_routes.current_request.to_dict()
        params = e.get('query_params')
        user_id = params.get('user_id')
        uid = params.get('uid')
        _id = int(params.get('id'))
        
        if not user_collection.find_one({"user":user_id, "uuid": uid}):
            return Response(body='uuid is required',
                headers={'Content-Type': 'text/html'},
                status_code=403)
        collection.delete_one({'user': user_id, 'id': _id,  'type': 'reply' })

        return Response(body=_id,
            headers={'Content-Type': 'application/json'},
            status_code=200)

    
@board_routes.route('/board/{_id}/favorite', methods=['PATCH'], cors=True)
def handleBoardFavorite(_id):
    collection = db['board']
    user_collection = db['users']
    data = json.loads(board_routes.current_request.raw_body.decode())
    user_id = data.get('user_id')
    creater_id = data.get('creater_id')
    uid = data.get('uid')

    if not user_collection.find_one({"user":user_id, "uuid": uid}):
        return Response(body='uuid is required',
            headers={'Content-Type': 'text/html'},
            status_code=403)
    if creater_id:
        res = collection.find_one(
                {'user': creater_id, 'favorites': { '$in': [user_id] }} # 있으면 빼고 없으면 넣어라
            )
        query = {'user': creater_id, 'id':int(_id), 'related_id':creater_id+':%s'%_id, 'type': 'board'}

        if not res:
            collection.update_one(query, {'$push': {'favorites': user_id}})
        else:
            print(res)
            collection.update_one(query, {'$pull': {'favorites': user_id}})
        # collection.insert_one(item)
        # print(res)
        return Response(body=_id+":%s"%creater_id,
            headers={'Content-Type': 'application/json'},
            status_code=204)