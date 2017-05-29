import time
import json
import os

import Pyro4
from flask import Flask, render_template, jsonify, request
import requests

ns = Pyro4.locateNS('localhost', 50010)
proxy = Pyro4.Proxy(ns.lookup("LAN"))

with open("./api_keys.json", 'r') as f_keys:
	keys = json.load(f_keys)

app = Flask(__name__)

@app.route("/")
def main():
	return render_template('index.html')

@app.route("/<api_key>/get-ip")
def get_ip(api_key):
	if api_key in keys:
		ip_address = proxy.get_ip()
	else:
		ip_address = '127.0.0.1'
	return jsonify(result=json.dumps({'ip':ip_address}))

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5002, debug=True)
