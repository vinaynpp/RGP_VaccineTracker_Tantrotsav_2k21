from datetime import date
import os
import requests
import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

from werkzeug.datastructures import ImmutableMultiDict

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

corehost = "https://cdn-api.co-vin.in/api/"

def dateconvert(date):
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    date = date.strftime('%d-%m-%Y')
    return date
def datereconvert(date):
    date = datetime.datetime.strptime(date, '%d-%m-%Y')
    date = date.strftime('%Y-%m-%d')
    return date


def getres(url, param):
    host = corehost + url
    print(param)
    response = requests.get(host, params=param)
    response = response.json()
#    print(response)
    return response

emailserver = "https://rpgemail.herokuapp.com/json/"



@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        if session["stateid"]:
            session.pop('stateid')
        if session["districtid"]:
            session.pop('districtid')
        if session["pincode"]:
            session.pop('pincode')
        if session["date"]:
            session.pop('date')
    finally:
        param = {}
        stateres = getres(url="v2/admin/location/states", param=param)
        print(stateres["states"])
        return render_template('index.html', states=stateres["states"])

#@app.route('/getstates')
#def getstates():
#    param = {}
#    stateres = getres(url="v2/admin/location/states", param=param)
#    print(stateres["states"])
#    return render_template('index.html', states=stateres["states"])

@app.route('/getdistricts', methods=['GET', 'POST'])
def getdistricts():
    if request.method == 'POST':
        param = {}
        stateid =int(request.form['states'])
        session["stateid"] = stateid
        stateres = getres(url="v2/admin/location/states", param=param)

        print(session)
    #    param["state_id"] = session["stateid"]
        districtres = getres(url="v2/admin/location/districts/"+ str(stateid) , param=param)
 #       print(districtres["districts"])


        return render_template('index.html', states=stateres["states"], districts=districtres["districts"], mystateid = session["stateid"])

@app.route('/getvd', methods=['GET', 'POST'])
def getvd():
    if request.method == 'POST':
        param = {}
        stateres = getres(url="v2/admin/location/states", param=param)
        districtres = getres(url="v2/admin/location/districts/"+ str(session["stateid"]) , param=param)

        session["districtid"] = request.form['districts']
        session["date"] = dateconvert( request.form['date'])
 #       print(session)
        param = {"district_id": str(session["districtid"]), "date": str(session["date"])}
        findByDistrict = getres(url="v2/appointment/sessions/public/findByDistrict", param=param)
        print(session)
        return render_template("index.html",vaccine_details=findByDistrict["sessions"], states=stateres["states"], mystateid = session["stateid"], districts=districtres["districts"], mydistrictid = session["districtid"], mydate = datereconvert(session["date"]) )
    
@app.route('/getvp', methods=['GET', 'POST'])
def getvp():
    if request.method == 'POST':
        param = {}
        stateres = getres(url="v2/admin/location/states", param=param)
        
        session["pincode"] = request.form['pincode']
        session["date"] = dateconvert( request.form['date'])
        param = {"pincode": str(session["pincode"]), "date": str(session["date"])}
        pinres = getres(url="v2/appointment/sessions/public/findByPin", param=param)
        print(session)
        return render_template("index.html",vaccine_details=pinres["sessions"], mydate = datereconvert(session["date"]), mypincode = session["pincode"], states=stateres["states"])
        
@app.route('/instr', methods=['GET', 'POST'])
def instr():
    return render_template('instr.html')

@app.route('/dos', methods=['GET', 'POST'])
def dos():
    return render_template('dos.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/email', methods=['GET', 'POST'])  
def email():
    type = request.form['type']
    id = request.form['email']

    if type=="vp":
        param = {"pincode": str(session["pincode"]), "date": str(session["date"])}
        emailcontent = getres(url="v2/appointment/sessions/public/findByPin", param=param)

    elif type=="vd":
        param = {"district_id": str(session["districtid"]), "date": str(session["date"])}
        emailcontent = getres(url="v2/appointment/sessions/public/findByDistrict", param=param)
    emailcontent = str(emailcontent["sessions"])
    print(emailcontent)

    eparam = {"name": "user", "meraemail": "", "merapswd": "", "email": id, "subject": "Vaccine Information", "contents": emailcontent}
    emailres = requests.get(emailserver, params=eparam)
    print(emailres.text)
    return render_template("index.html" )  

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(threaded=True, port=port, debug=True, host="0.0.0.0")