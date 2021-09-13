import os
import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

corehost = "https://cdn-api.co-vin.in/api/"


def getres(url, param):
    host = corehost + url
    response = requests.get(host)
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
        stateid = request.get_data('states')
        param["state_id"] = stateid
        districtres = getres(url="v2/admin/location/districts/"+ str(stateid) , param=param)
        print(districtres["districts"])
        return render_template('index.html', states=stateres["states"], districts=districtres["districts"])


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(threaded=True, port=port, debug=True)