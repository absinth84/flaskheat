import redis_connector
from ds18b20 import DS18B20
import time
import datetime
import RPi.GPIO as GPIO
import requests



redisPrefix = "flaskheat"
#get Generlasettings
generalSettings = redis_connector.redisCmdHgetAll(redisPrefix + ':general')

#Set Relay pin
relayPin = int(generalSettings['relayGpio'])

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(relayPin, GPIO.OUT)



days = ['mon','tue','wed','thu','fri','sat','sun']
relay = int(generalSettings['relay'])


sensor = DS18B20()
temperature = round(sensor.get_temperature(), 3)
print("The temperature is %s celsius" % temperature)

#Save temp on redis

redis_connector.redisCmdHset(redisPrefix + ':general', 'lastTemp', temperature)


delta = float(generalSettings['delta'])
#set historical temp if enabled

if generalSettings['enableHistoricalData'] == 'true':
    timestamp = int(time.time())
    print(timestamp, datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'), temperature)
    redis_connector.redisCmdRpush(redisPrefix + ':temperature', str(timestamp) + ":" + str(temperature))



#Control Heat Relay

if redis_connector.redisCmdHget(redisPrefix + ':general', 'enabled') == 'true':
    # temp > min
    print("enable = true")
    currentPeriod = datetime.datetime.now()
    currentConfig = redis_connector.redisCmdHget(redisPrefix + ':weeklyplan:' + days[currentPeriod.weekday()] , currentPeriod.hour)
    if temperature <= (float(generalSettings['minTemp']) - delta):
        relay = 1
        print("Start for min")
    elif temperature > (float(generalSettings['minTemp']) + delta) :
        #check current weeklyplan configuration
        print("Temp > minTemp")
        
        print("Current config=" + currentConfig)
        
        #OFF
        if currentConfig == '0':
            relay = 0
            print("Stop for min")
        #DAY
        elif currentConfig == '1':
            if temperature <= (float(generalSettings['dayTemp']) - delta):
                relay = 1
                print("Start for day")
            elif temperature > (float(generalSettings['dayTemp']) + delta):
                relay = 0
                print("Stop for day")
        #NIGHT    
        elif currentConfig == '2':
            if temperature <= (float(generalSettings['nightTemp']) - delta):
                relay = 1
                print("Start for night")
            elif temperature > (float(generalSettings['nightTemp']) + delta):
                relay = 0
                print("Stop for night")
    else:
        relay = generalSettings['relay']
        if currentConfig == '1':
            if temperature <= (float(generalSettings['dayTemp']) - delta):
                relay = 1
                print("Start for day")
            elif temperature > (float(generalSettings['dayTemp']) + delta):
                relay = 0
                print("Stop for day")
        #NIGHT    
        elif currentConfig == '2':
            if temperature <= (float(generalSettings['nightTemp']) - delta):
                relay = 1
                print("Start for night")
            elif temperature > (float(generalSettings['nightTemp']) + delta):
                relay = 0
                print("Stop for night")
        print("Nothing in the middle of deltas")
else:
    print("Stop for geralsetting disabled")
    relay = 0

print("Relay: ", relay)


#Set Relay IO
try:
    GPIO.output(relayPin, int(relay))
except ValueError as err:
    print(err)

#Update redis relay
redis_connector.redisCmdHset(redisPrefix + ':general', 'relay', relay)

if generalSettings['enableHistoricalData'] == 'true':
    redis_connector.redisCmdRpush(redisPrefix + ':relay', str(timestamp) + ":" + str(relay))
    

if generalSettings['enableExtTemp'] == 'true':
    r = requests.get(url = generalSettings['extTempUrl'])
    extTemp = r.json()["main"]["temp"]
    redis_connector.redisCmdRpush(redisPrefix + ':externalTemp', str(timestamp) + ":" + str(extTemp))
    redis_connector.redisCmdHset(redisPrefix + ':general', 'lastOutTemp', str(extTemp))

