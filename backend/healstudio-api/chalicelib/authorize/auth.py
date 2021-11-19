import re, uuid

def auth_check(user_id, pwd):
    if len(user_id)<6 or len(user_id)>20:
        return False
    if len(pwd) < 8 or len(pwd) > 20 and not re.findall('[0-9]+', pwd) and not \
        re.findall('[a-z]', pwd) or not re.findall('[A-Z]', pwd):
        return False

    elif not re.findall('[`~!@#$%^&*(),<.>/?]+', pwd):
        return False

    return True
    
def create_uuid(user_id, password, ip):
    # import random
    # r = list(user_id+ ip+ password)
    # random.shuffle(r)
    # name = ''.join(r)
    return str(uuid.uuid4())

def hidden_ip(ip):
    ips = ip.split('.') 
    ips[0] = '*'*3
    ips[1] = '*'*3
    result_ip = '.'.join(ips)
    return result_ip
    