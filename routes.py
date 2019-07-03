#!/usr/bin/python

from flask import Flask
from settings import *
from dbwatcher import *
import httplib

app = Flask(__name__)

#TODO error handling

@app.route("/update/<key>/<val>")
def update_config(key, val):
  update_settings(key, val)
  return '{} successfully set to {}'.format(key,val), httplib.OK
  
@app.route("/warn_test/")
def warn_test():
  print "warn test..."
  
app.run(host='0.0.0.0', port= 8090)
