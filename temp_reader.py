import redis_connector
from ds18b20 import DS18B20
import time
import datetime
import os


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
    print(int(timestamp), temperature)
<<<<<<< HEAD
    #redis_connector.redisCmdZadd(redisPrefix + ':temperature', temperature, int(timestamp))
    redis_connector.redisCmdRpush(redisPrefix + ':temperature', int(timestamp) + ":" + temperature )
=======
    redis_connector.redisCmdZadd(redisPrefix + ':temperature', temperature, int(timestamp)
>>>>>>> 8ea36206389960019224732c23656d9c68747303



#Control Heat Relay




if redis_connector.redisCmdHget(redisPrefix + ':general', 'enabled') == 'true':
    # temp > min
    if temperature < (float(redis_connector.redisCmdHget(redisPrefix + ':general', 'minTemp')) - delta):
        relay = 1
        print("Start for min")
    elif temperature > (float(redis_connector.redisCmdHget(redisPrefix + ':general', 'minTemp')) + delta):
        #check current weeklyplan configuration
        currentPeriod = datetime.datetime.now()
        currentConfig = redis_connector.redisCmdHget(redisPrefix + ':weeklyplan:' + days[currentPeriod.weekday()] , currentPeriod.hour)
        
        #OFF
        if currentConfig == '0':
            relay = 0
            print("Stop for min")
        #DAY
        elif currentConfig == '1':
            if temperature < (float(redis_connector.redisCmdHget(redisPrefix + ':general', 'dayTemp')) - delta):
                relay = 1
                print("Start for day")
            elif temperature > (float(redis_connector.redisCmdHget(redisPrefix + ':general', 'dayTemp')) + delta):
                relay = 0
                print("Stop for day")
        #NIGHT    
        elif currentConfig == '2':
            if temperature < (float(redis_connector.redisCmdHget(redisPrefix + ':general', 'nightTemp')) - delta):
                relay = 1
                print("Start for night")
            elif temperature > (float(redis_connector.redisCmdHget(redisPrefix + ':general', 'nightTemp')) + delta):
                relay = 0
                print("Stop for night")
    else:
       print("Stop for min ") 
else:
    print("Stop for geralsettin enable")

print("Relay: ", relay)


#Set Relay IO
os.system("echo "  + str(relay) + " > /sys/class/gpio/gpio25/value")

#Update redis temp
redis_connector.redisCmdHset(redisPrefix + ':general', 'lastTemp', temperature)
redis_connector.redisCmdHset(redisPrefix + ':general', 'lastTemp', relay)
    

