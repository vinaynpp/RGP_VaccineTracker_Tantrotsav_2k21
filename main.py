from datetime import date
import os
import requests
import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

from werkzeug.datastructures import ImmutableMultiDict

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

corehost = "https://cdn-api.co-vin.in/api/"

def dateconvert(date):
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    date = date.strftime('%d-%m-%Y')
    return date


def getres(url, param):
    host = corehost + url
    print(param)
    response = requests.get(host, params=param)
    response = response.json()
#    print(response)
    return response

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/getstates')
def getstates():
    param = {}
    stateres = getres(url="v2/admin/location/states", param=param)
    print(stateres["states"])
    return render_template('index.html', states=stateres["states"])

@app.route('/getdistricts', methods=['GET', 'POST'])
def getdistricts():
    if request.method == 'POST':
        param = {}
        stateres = getres(url="v2/admin/location/states", param=param)
        stateid =int(request.form['states'])
        session["stateid"] = stateid
        print(session)
    #    param["state_id"] = session["stateid"]
        districtres = getres(url="v2/admin/location/districts/"+ str(stateid) , param=param)
 #       print(districtres["districts"])

        return render_template('index.html', states=stateres["states"], districts=districtres["districts"])

@app.route('/getvd', methods=['GET', 'POST'])
def getvd():
    if request.method == 'POST':
        session["districtid"] = request.form['districts']
        session["date"] = dateconvert( request.form['date'])
 #       print(session)
        param = {"district_id": str(session["districtid"]), "date": str(session["date"])}
        findByDistrict = getres(url="v2/appointment/sessions/public/findByDistrict", param=param)
        print(findByDistrict)
        return render_template("getvd.html")
    


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(threaded=True, port=port, debug=True)