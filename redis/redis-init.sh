redis_host=127.0.0.1
redis_db=0


#Docker sudo docker run --name redis-flaskheat -v $(pwd)/redis:/data -d -p 127.0.0.1:6379:6379 --rm redis 

#Weekly plan
for day in {mon,tue,wed,thu,fri,sat,sun}; do
    for hour in {0..23}; do
        echo "$day $hour"
        redis-cli -h $redis_host -n $redis_db HSET flaskheat:weeklyplan:$day $hour 0
    done
done


#General setting 

redis-cli -h $redis_host -n $redis_db HSET flaskheat:general enabled false
redis-cli -h $redis_host -n $redis_db HSET flaskheat:general enableHistoricalData true
redis-cli -h $redis_host -n $redis_db HSET flaskheat:general enableMinTemp false
redis-cli -h $redis_host -n $redis_db HSET flaskheat:general minTemp 0
redis-cli -h $redis_host -n $redis_db HSET flaskheat:general dayTemp 10
redis-cli -h $redis_host -n $redis_db HSET flaskheat:general nightTemp 10
redis-cli -h $redis_host -n $redis_db HSET flaskheat:general lastTemp 20 
redis-cli -h $redis_host -n $redis_db HSET flaskheat:general outTemp 15
redis-cli -h $redis_host -n $redis_db HSET flaskheat:general delta 0.1
redis-cli -h $redis_host -n $redis_db HSET flaskheat:general enableExtTemp true
redis-cli -h $redis_host -n $redis_db HSET flaskheat:general extTempUrl "http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=ILOMBARD38&format=1"
redis-cli -h $redis_host -n $redis_db HSET flaskheat:general relay 0
redis-cli -h $redis_host -n $redis_db HSET flaskheat:general relayGpio 25




