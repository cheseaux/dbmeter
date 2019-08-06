#!/usr/bin/python

from flask import Flask
from flask import jsonify

from settings import *
from dbwatcher import *
import httplib

app = Flask(__name__)

@app.route("/test/warn")
def test_warning():
  warning()
  
@app.route("/test/alarm")
def test_alarm():
  alarm()

