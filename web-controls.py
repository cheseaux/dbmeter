from flask import Flask
from dbwatcher import *
import httplib

app = Flask(__name__)

@app.route("/blink")
def blink_call():
  blink(print_matrix, cross_8x8)
  return '', httplib.NO_CONTENT

app.run(host='0.0.0.0', port= 8090)
