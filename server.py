from flask import Flask, escape, request, render_template, redirect
import redis_connector

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True





@app.route('/')
def home():
    
    lastTemp = redis_connector.redisCmdHget('flaskheat:general', 'lastTemp')
    lastOutTemp = redis_connector.redisCmdHget('flaskheat:general', 'outTemp')
    return render_template('home.html', lastTemp = lastTemp, lastOutTemp = lastOutTemp)

@app.route('/weeklyplan')
def weeklyplan():
    return render_template('weeklyplan.html')


@app.route('/generalsettings', methods=['GET', 'POST'])
def generalsettings():
    if request.method == 'GET':
        enabled = redis_connector.redisCmdHget('flaskheat:general', 'enabled')
        dayTemp = redis_connector.redisCmdHget('flaskheat:general', 'dayTemp')
        nightTemp = redis_connector.redisCmdHget('flaskheat:general', 'nightTemp')
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
            redis_connector.redisCmdHset('flaskheat:general', 'enabled', request.form['enabled'])
            redis_connector.redisCmdHset('flaskheat:general', 'dayTemp', request.form['dayTemp'])
            redis_connector.redisCmdHset('flaskheat:general', 'nightTemp', request.form['nightTemp'])
            return redirect("/generalsettings", code=302)

        except:
            return EnvironmentError



