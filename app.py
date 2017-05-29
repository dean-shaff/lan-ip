import time
import json

import Pyro4
from flask import Flask, render_template, jsonify, request
import requests

ns = Pyro4.locateNS('localhost', 50010)
proxy = Pyro4.Proxy(ns.lookup("LAN"))

app = Flask(__name__)

@app.route("/")
def main():
	return render_template('index.html')

@app.route("/get-ip")
def get_ip():
	ip_address = proxy.get_ip()
	return jsonify(result=json.dumps({'ip':ip_address}))

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5002, debug=True)
