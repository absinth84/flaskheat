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
        print(request.form.get)
        enable = redis_connector.redisCmdHget('flaskheat:general', 'enable')
        dayTemp = redis_connector.redisCmdHget('flaskheat:general', 'dayTemp')
        nightTemp = redis_connector.redisCmdHget('flaskheat:general', 'nightTemp')
        print(enable, dayTemp, nightTemp)
        return render_template('generalsettings.html', enable = enable, dayTemp=dayTemp, nightTemp=nightTemp)

    if request.method == 'POST':
        print("Post method")
        print(request.form.get)
        #return redirect("/generalsettings", code=302)
        return str(request.form.get)



