from flask import Flask, escape, request, render_template, redirect
import redis_connector

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

redisPrefix = "flaskheat"
days = ['mon','tue','wed','thu','fri','sat','sun']



@app.route('/')
def home():
    
    lastTemp = redis_connector.redisCmdHget(redisPrefix + ':general', 'lastTemp')
    lastOutTemp = redis_connector.redisCmdHget(redisPrefix + ':general', 'outTemp')
    return render_template('home.html', lastTemp = lastTemp, lastOutTemp = lastOutTemp)

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
        print(weekly)
        return render_template('weeklyplan.html', weekly = weekly)

    if request.method == 'POST':
        print("POST method")
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
        enabled = redis_connector.redisCmdHget(redisPrefix + ':general', 'enabled')
        dayTemp = redis_connector.redisCmdHget(redisPrefix + ':general', 'dayTemp')
        nightTemp = redis_connector.redisCmdHget(redisPrefix + ':general', 'nightTemp')
        if enabled == 'true':
            enabled = 'checked'
        print(enabled, dayTemp, nightTemp)
        return render_template('generalsettings.html', enabled=enabled, dayTemp=dayTemp, nightTemp=nightTemp)

    if request.method == 'POST':
        print("Post method")
        print(request.form.get)
        print(request.form['dayTemp'])

        #Save settings
        try:
            redis_connector.redisCmdHset(redisPrefix + ':general', 'enabled', request.form['enabled'])
            redis_connector.redisCmdHset(redisPrefix + ':general', 'dayTemp', request.form['dayTemp'])
            redis_connector.redisCmdHset(redisPrefix + ':general', 'nightTemp', request.form['nightTemp'])
            return redirect("/generalsettings", code=301)

        except:
            return EnvironmentError



