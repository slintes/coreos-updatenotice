#!/usr/bin/env python
from flask import Flask, url_for, json, request
import logging
app = Flask(__name__)

@app.before_first_request
def init():
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)

@app.route('/')
def api_root():
    app.logger.info("OK")
    return 'OK'

@app.route('/echo', methods = ['POST'])
def api_echo():
    if request.headers['Content-Type'] == 'text/plain':
        app.logger.info(request.data)
        return request.data
    if request.headers['Content-Type'] == 'application/json':
        if request.json is None:
            app.logger.info("empty json")
        else:
            app.logger.info(json.dumps(request.json))
        return json.dumps(request.json)
    app.logger.error("unsupported content type")
    return 'unsupported Content-Type'

if __name__ == '__main__':
    app.run()
