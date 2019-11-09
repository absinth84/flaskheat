import redis_connector
from ds18b20 import DS18B20


sensor = DS18B20()
temperature = sensor.get_temperature()
print("The temperature is %s celsius" % temperature)


