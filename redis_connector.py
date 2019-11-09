#Redis Connection
import redis


def redisConn():

    host = '127.0.0.1'
    port = '6379'
    db = '0'

    try:
        conn = redis.StrictRedis(host=host, port=port, db=db, charset="utf-8", decode_responses=True)
        #print(conn)
        conn.ping()
        #print('Connected!')
        return conn
    except Exception as ex:
        print('Error:', ex)
        return 0

def redisCmdHget(name, key):
    r = redisConn()
    result = r.hget(name, key)
    return result

def redisCmdHset(name, key, value):
    r = redisConn()
    result = r.hset(name, key, value)
    return result

def redisCmdZadd(name, timestamp, value):
    r = redisConn()
    result = r.zadd(name, timestamp, value)
    return result