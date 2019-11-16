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
    #print(lastTemp)
    
    if generalSettings['enableHistoricalData'] == 'false':
        #print("No hist data")
        tempData = ""

    elif generalSettings['enableHistoricalData'] == 'true':
        tempData = redis_connector.redisCmdLrange(redisPrefix + ":temperature", "-" + str(samples), -1)
        relayData = redis_connector.redisCmdLrange(redisPrefix + ":relay", "-" + str(samples), -1)
        print("Histdat on")

    #Set Termo color    
    relayTermColor = ""
    if generalSettings['relay'] == '1':
        relayTermColor = "Red"

    return render_template('home.html', lastTemp = lastTemp, lastOutTemp = lastOutTemp, samples = samples, tempData = tempData, relayData = relayData, relayTermColor = relayTermColor)


@app.route('/weeklyplan', methods=['GET', 'POST'])
def weeklyplan():
    

    if request.method == 'GET':
        #Get Weeklyplan from redis
        
        weekly = [[0 for i in range(24)] for i in range(7)]
        #print(weekly)
        i = 0
        for day in days:
            for hour in range(24):
                result = redis_connector.redisCmdHget(redisPrefix + ':weeklyplan:' + day , hour)
                weekly[i][hour] = result
                #print(day, i, hour, weekly[i][hour], result)
            #print(weekly[i])
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
        if generalSettings['minTempEnabled'] == 'true':
            generalSettings['minTempEnabled'] = 'checked'
        #print(enabled, dayTemp, nightTemp, minTempEnabled, minTemp)
        return render_template('generalsettings.html', enabled=generalSettings['enabled'], dayTemp=generalSettings['dayTemp'], nightTemp=generalSettings['nightTemp'], minTempEnabled=generalSettings['minTempEnabled'], minTemp=generalSettings['minTemp'])

    if request.method == 'POST':
        #print("Post method")
        #print(request.form.get)
        

        #Save settings
        try:
            redis_connector.redisCmdHset(redisPrefix + ':general', 'enabled', request.form['enabled'])
            redis_connector.redisCmdHset(redisPrefix + ':general', 'dayTemp', request.form['dayTemp'])
            redis_connector.redisCmdHset(redisPrefix + ':general', 'nightTemp', request.form['nightTemp'])
            redis_connector.redisCmdHset(redisPrefix + ':general', 'minTempEnabled', request.form['minTempEnabled'])
            redis_connector.redisCmdHset(redisPrefix + ':general', 'minTemp', request.form['minTemp'])
            return redirect("/generalsettings", code=301)

        except:
            return EnvironmentError


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)


        

