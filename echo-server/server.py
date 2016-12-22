#!/usr/bin/env python
from flask import Flask, url_for, json, request
app = Flask(__name__)

@app.route('/')
def api_root():
    return 'OK'

@app.route('/echo', methods = ['POST'])
def api_echo():
    if request.headers['Content-Type'] == 'text/plain':
        print request.data
        return request.data
    if request.headers['Content-Type'] == 'application/json':
        print json.dumps(request.json)
        return json.dumps(request.json)
    return 'unsupported Content-Type'

if __name__ == '__main__':
    app.run()
