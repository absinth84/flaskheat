#Redis Connection
import redis


def redisConn():

    host = '127.0.0.1'
    port = '6379'
    db = '0'

    try:
        conn = redis.StrictRedis(host=host, port=port, db=db, charset="utf-8", decode_responses=True)
        print(conn)
        conn.ping()
        print('Connected!')
        return conn
    except Exception as ex:
        print('Error:', ex)
        return 0

def redisCmdget():
    r = redisConn()
    r.get()

def redisCmdHget(key1, key2):
    r = redisConn()
    result = r.hget(key1, key2)
    return result

def redisCmdSet():
    r = redisConn()


def redisCmdHset():
    r = redisConn()

