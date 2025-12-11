#Redis Connection

import redis


host = '127.0.0.1'
port = '6379'
db = '0'



def redisConn():

    try:
        conn = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        #print(conn)
        conn.ping()
        #print('Connected!')
        return conn
    except Exception as ex:
        print('Redis Error:', ex)
        return 0

def redisCmdHget(name, key):
    r = redisConn()
    result = r.hget(name, key)
    return result

def redisCmdHset(name, key, value):
    r = redisConn()
    result = r.hset(name, key, value)
    return result

def redisCmdRpush(name, value):
    r = redisConn()
    result = r.rpush(name, value)
    return result

def redisCmdLrange(name, start, end):
    r = redisConn()
    result = r.lrange(name, start, end)
    return result

def redisCmdHgetAll(name):
    r = redisConn()
    
    res = r.hgetall(name)
    return res
