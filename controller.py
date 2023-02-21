#!/usr/bin/env python3

# Glody Mutebwa
# Controller for the entire program

import Adafruit_BBIO.GPIO as GPIO
import math
import src
import smbus
import time
import sys
import json
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

conf_init = {
    "server":"chat.freenode.net",
    "port":6667,
    "channel": "BeagleCom",
    "username":"",
    "password":"",
}

# Route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['user'] == "" or request.form['passwd'] == "":
            error = 'Invalid Credentials. Please try again.'
        else:
            conf_init["username"] =  request.form['user']
            conf_init["password"] =  request.form['passwd']   #Use when implementing SSL
            json_object = json.dumps(conf_init, indent=4)
            with open("config.json", "w") as outfile:
                outfile.write(json_object)
            return redirect(url_for('chat'))
    return render_template('login.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    print("In Chat!")
    templateData = {
      		    'User' : conf_init["username"]
      	    }
    if request.method == 'POST':
        msg = request.form['message']
        print(msg)
        return render_template('chat.html', **templateData)
    else:        
        return render_template('chat.html', **templateData)

@app.route('/send', methods=['GET', 'POST'])
def sendfile():
    print("Supposed to send now")
    return render_template('chat.html')


if __name__ == "__main__":                                      # run Flask server
        app.run(host='0.0.0.0', port=8081, debug=True)