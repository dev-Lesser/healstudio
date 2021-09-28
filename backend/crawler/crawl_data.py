import requests
from requests import exceptions
import pymongo
import pandas as pd
import urllib.request
import os, json, sys


def createGglquery(query, display=50, start=1):
    query = [{
        'operationName': "getPlacesList",
        'query': """query getPlacesList($input: PlacesInput) {
                    businesses: places(input: $input) {
                        total
                        items {
                            id
                            name
                            category
                            roadAddress
                            fullAddress
                            bookingUrl      
                            phone
                            virtualPhone
                            businessHours
                            daysOff
                            imageUrl
                            x
                            y
                        }
                    }
                }""",
        'variables': {
            'input':{
                'adult': False,
                'deviceType': "pcmap",
                'display': display,
                'query': query,
                'queryRank': "",
                'spq': False,
                'start': start
            },
            'isBounds': 'false',
            'isNmap': 'false'
        }

    }]
    return query

def parseGymDetail(data):
    gymID = data['id']
    url = 'https://map.naver.com/v5/api/sites/summary/{id}?lang=ko'.format(id=gymID)
    checkParse = False
    desc = None
    keywords = None
    urlList = None
    imgList = None
    imageIDs = []
    try:
        res_detail = requests.get(url).json()
    except exceptions.HTTPError as e:
        return pd.Series([desc, keywords, urlList, imageIDs, checkParse])
    except exceptions.ConnectionError as e:
        return pd.Series([desc, keywords, urlList, imageIDs, checkParse])
    except exceptions.RetryError as e:
        return pd.Series([desc, keywords, urlList, imageIDs, checkParse])
    desc = res_detail['description']
    keywords = res_detail['keywords']
    urlList = res_detail['urlList']
    imgList = [i['url'] for i in res_detail['images']]
    print(keywords)
    if keywords == 0:
        keywords = None
    
    if imgList:
        try:
            
            os.makedirs("images/{gymID}".format(gymID=gymID))
        except FileExistsError:
            # directory already exists
            pass
        for idx, image_url in enumerate([i['url'] for i in res_detail['images']][:5]):
            try:
                imageIDs.append(gymID +'_{}'.format(idx))
                urllib.request.urlretrieve(image_url, 'images/' + gymID + '/' +gymID +'_{}'.format(idx) +'.jpg') # code 이름으로 파일 저장
            except Exception:
                continue
    else:
        imageIDs = []
    checkParse = True
    return pd.Series([desc, keywords, urlList, imageIDs, checkParse])

def main():
    
    client = pymongo.MongoClient(DB_HOST)
    db = client[DB_NAME]
    region = db['region']
    regions = list(region.find({'depth1': sys.argv[1]}))
    spaces = db[COLLECTION_NAME]
    url = 'https://pcmap-api.place.naver.com/place/graphql'

    for ires in list(regions):
        print(ires)
        page = 1
        headers = {
            'origin': 'https://pcmap.place.naver.com',
            'referer': 'https://pcmap.place.naver.com/',
            'Content-type':  'application/json',
        }
        
        while True:
            print('page is', page)
            data = createGglquery(
                query='{region} {region_detail} {region_detail_spec} 헬스장'.format(
                            region = ires['region'], 
                            region_detail=ires['depth1'],
                            region_detail_spec=ires['depth2'] if ires['depth2'] is not None else ''
                    ), 
                start=page
            )
            res = requests.post(url, data=json.dumps(data), headers=headers).json()
            if not res[0]['data']['businesses']['items']:
                break


            df = pd.DataFrame(res[0]['data']['businesses']['items'])
            df = df[df['name']!='전단지배포대행홍보전문업체학원헬스장배포']

            
            df = df.astype({'x':float, 'y': float})
            df['region'] = ires['region']
            df['region_detail'] = ires['depth1']
            df['region_detail_spec'] =ires['depth2']
            df[['desc', 'keywords', 'urlList', 'imgList', 'checkParse']] = df.apply(parseGymDetail, axis=1)
            data = df.to_dict('records')
            spaces.insert_many(data)
            page += 50

if __name__ == '__main__':
    main()