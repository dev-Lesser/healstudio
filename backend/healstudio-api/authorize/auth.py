import re, uuid

def auth_check(user_id, pwd):
    if len(user_id)<6 or len(user_id)>20:
        return False
    if len(pwd) < 8 or len(pwd) > 21 and not re.findall('[0-9]+', pwd) and not \
        re.findall('[a-z]', pwd) or not re.findall('[A-Z]', pwd):
        return False

    elif not re.findall('[`~!@#$%^&*(),<.>/?]+', pwd):
        return False

    return True
    
def create_uuid(user_id, password, ip):
    import random
    r = list(user_id+ ip+ password)
    random.shuffle(r)
    name = ''.join(r)
    return str(uuid.uuid5(uuid.NAMESPACE_URL, name))

def hidden_ip(ip):
    ips = ip.split('.') 
    ips[1] = '*'*3
    ips[2] = '*'*3
    result_ip = '.'.join(ips)
    return result_ip
    