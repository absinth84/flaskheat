import redis_connector
from ds18b20 import DS18B20
import time
import datetime

redisPrefix = "flaskheat"
days = ['mon','tue','wed','thu','fri','sat','sun']
delta = 0.25
relay = 0

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



#Control Heat Relay




if redis_connector.redisCmdHget(redisPrefix + ':general', 'enabled'):
    # Start for maintain temp > min
    if temperature < float(redis_connector.redisCmdHget(redisPrefix + ':general', 'minTemp') - delta):
        realy = 1
        print("Start")
    elif temperature > float(redis_connector.redisCmdHget(redisPrefix + ':general', 'minTemp') + delta):
        #check current weeklyplan configuration
        currentPeriod = datetime.datetime.now()
        currentConfig = redis_connector.redisCmdHget(redisPrefix + ':weeklyplan:' + days[currentPeriod.weekday()] , currentPeriod.hour)
        #OFF
        if currentConfig == 0:
            realy = 0
            print("Stop")
        #DAY
        elif currentPeriod == 1:
            if temperature < float(redis_connector.redisCmdHget(redisPrefix + ':general', 'dayTemp') - delta):
                realy = 1
                print("Start")
            elif temperature > float(redis_connector.redisCmdHget(redisPrefix + ':general', 'dayTemp') + delta):
                realy = 0
                print("Stop")
        #NIGHT    
        elif currentPeriod == 2:
            if temperature < float(redis_connector.redisCmdHget(redisPrefix + ':general', 'nightTemp') - delta):
                realy = 1
                print("Start")
            elif temperature > float(redis_connector.redisCmdHget(redisPrefix + ':general', 'nightTemp') + delta):
                realy = 0
                print("Stop")
    else:
       print("Stop") 

print("Relay: ", relay)




    

