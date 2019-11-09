import redis_connector
from ds18b20 import DS18B20
import time

redisPrefix = "flaskheat"

sensor = DS18B20()
temperature = sensor.get_temperature()
print("The temperature is %s celsius" % temperature)

#Save temp on redis

redis_connector.redisCmdHset(redisPrefix + ':general', 'lastTemp', temperature)

#set historical temp if enabled
if redis_connector.redisCmdHget(redisPrefix + ':general', 'enableHistoricalData'):
    timestamp = time.time()
    print(timestamp, temperature)
    redis_connector.redisCmdZadd(redisPrefix + 'temperature', timestamp, temperature)