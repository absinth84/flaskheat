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
temperature = round(sensor.get_temperature(), 3)
print("The temperature is %s celsius" % temperature)

#Save temp on redis

redis_connector.redisCmdHset(redisPrefix + ':general', 'lastTemp', temperature)

#get Generlasettings
generalSettings = redis_connector.redisCmdHgetAll(redisPrefix + ':general')
#print(generalSettings)

#set historical temp if enabled

if generalSettings['enableHistoricalData'] == 'true':
    timestamp = int(time.time())
    print(timestamp, datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'), temperature)
    redis_connector.redisCmdRpush(redisPrefix + ':temperature', str(timestamp) + ":" + str(temperature))



#Control Heat Relay

if redis_connector.redisCmdHget(redisPrefix + ':general', 'enabled') == 'true':
    # temp > min
    if temperature < (float(generalSettings['minTemp']) - delta):
        relay = 1
        print("Start for min")
    elif temperature > (float(generalSettings['minTemp']) + delta):
        #check current weeklyplan configuration
        currentPeriod = datetime.datetime.now()
        currentConfig = redis_connector.redisCmdHget(redisPrefix + ':weeklyplan:' + days[currentPeriod.weekday()] , currentPeriod.hour)
        
        #OFF
        if currentConfig == '0':
            relay = 0
            print("Stop for min")
        #DAY
        elif currentConfig == '1':
            if temperature < (float(generalSettings['dayTemp']) - delta):
                relay = 1
                print("Start for day")
            elif temperature > (float(generalSettings['dayTemp']) + delta):
                relay = 0
                print("Stop for day")
        #NIGHT    
        elif currentConfig == '2':
            if temperature < (float(generalSettings['nightTemp']) - delta):
                relay = 1
                print("Start for night")
            elif temperature > (float(generalSettings['nightTemp']) + delta):
                relay = 0
                print("Stop for night")
    else:
       print("Stop for min ") 
else:
    print("Stop for geralsettin enable")

print("Relay: ", relay)


#Set Relay IO
#os.system("echo "  + str(relay) + " > /sys/class/gpio/gpio25/value")

#Update redis relay
redis_connector.redisCmdHset(redisPrefix + ':general', 'relay', relay)

if generalSettings['enableHistoricalData'] == 'true':
    redis_connector.redisCmdRpush(redisPrefix + ':relay', str(timestamp) + ":" + str(relay))
    