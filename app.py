#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import json
import os
import sqlite3
import csv
import sqlite3 as lite

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
# load 
    con = sqlite3.connect('test.db')
    cur =con.cursor()
    con.text_factory = str
    cur.execute("SELECT * FROM film_info WHERE film_name='%s'" % filmname)
    rows = cur.fetchall()
    for row in rows:
        name = row[0]
        link = row[1]
        time = row[2]
        quality = row[3]
        speech="Thông Tin Phim:"+"\nTên Phim:\t" +name +"\t\nLink:\t"+link +"\t\nThời Lượng:\t"+time +"\t\nChất Lượng:\t"+quality
    con.close()
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
