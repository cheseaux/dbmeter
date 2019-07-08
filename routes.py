#!/usr/bin/python

from flask import Flask
from flask import jsonify

from settings import *
from dbwatcher import *
import httplib

app = Flask(__name__)

@app.route("/settings")
def show_settings():
  settings = load_settings()
  return jsonify(settings)
  
@app.route("/update/<key>/<val>")
def update_config(key, val):
  update_settings(key, val)
  return '{} successfully set to {}'.format(key,val), httplib.OK

@app.route("/test/warn")
def test_warning():
  warning()
  
@app.route("/test/alarm")
def test_alarm():
  alarm()

app.run(host='0.0.0.0', port= 8090)
