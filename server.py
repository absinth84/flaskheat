from flask import Flask, escape, request, render_template, redirect
import redis_connector
import string




app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

redisPrefix = "flaskheat"
days = ['mon','tue','wed','thu','fri','sat','sun']
samples = 280


@app.route('/')
def home():

    #get Generlasettings
    generalSettings = redis_connector.redisCmdHgetAll(redisPrefix + ':general')
    
    lastTemp = generalSettings['lastTemp']
    lastOutTemp = generalSettings['outTemp']


    #Set Termo color    
    relayTermColor = ""
    if generalSettings['relay'] == '1':
        relayTermColor = "Red"
    
    if generalSettings['enableHistoricalData'] == 'false':
        return render_template('home_nochart.html', lastTemp = lastTemp, relayTermColor = relayTermColor)
        

    elif generalSettings['enableHistoricalData'] == 'true':
        tempData = redis_connector.redisCmdLrange(redisPrefix + ":temperature", "-" + str(samples), -1)
        #realSample = tempData.count()
        relayData = redis_connector.redisCmdLrange(redisPrefix + ":relay", "-" + str(samples), -1)
        #print("Histdat on")
        return render_template('home.html', lastTemp = lastTemp, lastOutTemp = lastOutTemp, samples = samples, tempData = tempData, relayData = relayData, relayTermColor = relayTermColor)


@app.route('/weeklyplan', methods=['GET', 'POST'])
def weeklyplan():
    

    if request.method == 'GET':
        #Get Weeklyplan from redis
        
        weekly = [[0 for i in range(24)] for i in range(7)]
        #print(weekly)
        i = 0
        for day in days:
            result = redis_connector.redisCmdHgetAll(redisPrefix + ':weeklyplan:' +day)
            #print(result)
            #print(result['0'])
            for hour in range(24):
                weekly[i][hour] = result[str(hour)]
            i = i + 1
        #print(weekly)
        return render_template('weeklyplan.html', weekly = weekly)

    if request.method == 'POST':
        #print("POST method")
        data = request.form
        #print(data)
        i = 0
        for day in days:
            
            for hour in range(24):
                
                if data['element'] == 'formDayHour_' + str(i) + '_' + str(hour):
                    selDay = day
                    selHour = hour
                
                #print(day, 'formDayHour_' + str(i) + '_' + str(hour))    
            i = i + 1
        #print(selDay, hour)

        #save data on Redis
        #print(redisPrefix + ':weeklyplan:' + selDay, selHour, data['value'])
        redis_connector.redisCmdHset(redisPrefix + ':weeklyplan:' + selDay, selHour, data['value'])
        #return "200"
        return redirect("/weeklyplan", code=301)

@app.route('/weeklyplan/reset', methods=['POST'])
def weeklyplanReset():
    #Reset weeklyplan to OFF
    data = request.form
    print(data)
    if request.form['delete'] == 'true':
        print("TRUE")
        for day in days:   
            for hour in range(24):
                redis_connector.redisCmdHset(redisPrefix + ':weeklyplan:' + day, hour, '0')

    return redirect(request.referrer)


@app.route('/generalsettings', methods=['GET', 'POST'])
def generalsettings():

    if request.method == 'GET':
         #get Generlasettings
        generalSettings = redis_connector.redisCmdHgetAll(redisPrefix + ':general')
        if generalSettings['enabled'] == 'true':
            generalSettings['enabled'] = 'checked'
        if generalSettings['enableMinTemp'] == 'true':
            generalSettings['enableMinTemp'] = 'checked'
        if generalSettings['enableHistoricalData'] == 'true':
            generalSettings['enableHistoricalData'] = 'checked'
        if generalSettings['enableExtTemp'] == 'true':
            generalSettings['enableExtTemp'] = 'checked'
        #print(enabled, dayTemp, nightTemp, minTempEnabled, minTemp)
        return render_template('generalsettings.html', generalSettings = generalSettings)

    if request.method == 'POST':
        print("Post method")
        data = request.form
        print(data)


        

        #Save settings
        try:

            try: 
                request.form['enableSwitch']
                redis_connector.redisCmdHset(redisPrefix + ':general', 'enabled', request.form['enableSwitch'])
            except: redis_connector.redisCmdHset(redisPrefix + ':general', 'enabled', 'false')
            print('enableSwitch')

            redis_connector.redisCmdHset(redisPrefix + ':general', 'dayTemp', request.form['formControlDayTemp'])
            redis_connector.redisCmdHset(redisPrefix + ':general', 'nightTemp', request.form['formControlNightTemp'])
            print("formControlNightTemp")

            try: 
                request.form['enableMinTempSwitch']
                redis_connector.redisCmdHset(redisPrefix + ':general', 'enableMinTemp', request.form['enableMinTempSwitch'])
            except: redis_connector.redisCmdHset(redisPrefix + ':general', 'enableMinTemp', 'false')
            print('minTempEnableSwitch')

            redis_connector.redisCmdHset(redisPrefix + ':general', 'minTemp', request.form['formControlMinTemp'])

            try: 
                request.form['enableHistoricalDataSwitch']
                redis_connector.redisCmdHset(redisPrefix + ':general', 'enableHistoricalData', request.form['enableHistoricalDataSwitch'])
            except: redis_connector.redisCmdHset(redisPrefix + ':general', 'enableHistoricalData', 'false')
            print('enableHistoricalDataSwitch')
            try: 
                request.form['enableExtTempSwitch']
                redis_connector.redisCmdHset(redisPrefix + ':general', 'enableExtTemp', request.form['enableExtTempSwitch'])
            except: redis_connector.redisCmdHset(redisPrefix + ':general', 'enableExtTemp', 'false')

            redis_connector.redisCmdHset(redisPrefix + ':general', 'extTempUrl', request.form['extTempUrl'])
            redis_connector.redisCmdHset(redisPrefix + ':general', 'relayGpio', request.form['relayGpio'])

            return redirect("/generalsettings", code=301)

        except:
            return


if __name__ == "__main__":
    app.run()


        

