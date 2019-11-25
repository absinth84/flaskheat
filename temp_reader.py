import redis_connector
from ds18b20 import DS18B20
import time
import datetime
import RPi.GPIO as GPIO
import requests


#get Generlasettings
generalSettings = redis_connector.redisCmdHgetAll(redisPrefix + ':general')

#Set Relay pin
relayPin = generalSettings['realyGpio']

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(relayPin, GPIO.OUT)


redisPrefix = "flaskheat"
days = ['mon','tue','wed','thu','fri','sat','sun']


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
    if temperature <= (float(generalSettings['minTemp']) - delta):
        relay = 1
        print("Start for min")
    elif temperature > (float(generalSettings['minTemp']) + delta):
        #check current weeklyplan configuration
        print("Temp > minTemp")
        currentPeriod = datetime.datetime.now()
        currentConfig = redis_connector.redisCmdHget(redisPrefix + ':weeklyplan:' + days[currentPeriod.weekday()] , currentPeriod.hour)
        
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
        print("Nothing in the middle of deltas")
else:
    print("Stop for geralsetting disabled")
    relay = 0

print("Relay: ", relay)


#Set Relay IO
#os.system("echo "  + str(relay) + " > /sys/class/gpio/gpio25/value")
GPIO.output(relayPin, relay)

#Update redis relay
redis_connector.redisCmdHset(redisPrefix + ':general', 'relay', relay)

if generalSettings['enableHistoricalData'] == 'true':
    redis_connector.redisCmdRpush(redisPrefix + ':relay', str(timestamp) + ":" + str(relay))
    

if generalSettings['enableExtTemp'] == 'true':
    r = requests.get(url = generalSettings['extTempUrl'])
    extTemp = r.text.split('\n')[len(r.text.split('\n')) - 3].split(',')[1]
    redis_connector.redisCmdRpush(redisPrefix + ':externalTemp', str(timestamp) + ":" + str(extTemp))
