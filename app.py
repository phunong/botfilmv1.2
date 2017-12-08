#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)
@app.route('/welcome')
def welcome():
    return "Welcome to service!"
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))
    
    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "filminfo":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    filmname = parameters.get("film_name")

    film_info={'Diep Vien Bao Thu':'Link: http://www.phimmoi.net/phim/diep-vien-bao-thu-i3-5741/'}
    film_info2={'Diep Vien Bao Thu':'Time: 114 minutes'}
    film_info3={'Diep Vien Bao Thu':'Quality: HD'}
    speech = "Infomation" + filmname + ":" + str(film_info[filmname]) + str(film_info2[filmname])+ str(film_info3[filmname])
    print("Response:")
    print(speech)
    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        #"contextOut": [],
        "source": "NVPBOT"
    }
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" %(port))

    app.run(debug=True, port=port, host='0.0.0.0')
