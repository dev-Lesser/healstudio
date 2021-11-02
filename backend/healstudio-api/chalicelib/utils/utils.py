import datetime

def convertDatetime(res):
    r = list()
    for i in res:
        item = i
        item['created_at'] = i['created_at'].strftime('%Y-%m-%d')
        item['updated_at'] = i['updated_at'].strftime('%Y-%m-%d')
        r.append(item)
    return r


def convertDatetimeHours(res):
    r = list()
    for i in res:
        item = i
        item['created_at'] = i['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        item['updated_at'] = i['updated_at'].strftime('%Y-%m-%d %H:%M:%S')
        r.append(item)
    return r