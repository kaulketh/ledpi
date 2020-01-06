#!/usr/bin/python
# -*- coding: utf-8 -*-


from flask import Flask, render_template
from functions import animate, all_off, clock, advent
from xmas import russian_xmas
from clock import clear_clock

import os

# Load the env variables
if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/animate", methods=['GET'])
def animation_view():
    animate()
    return "animation started"


@app.route("/advent", methods=["GET"])
def advent_view():
    advent()
    return "advent calendar started"


@app.route("/clock", methods=["GET"])
def clock_view():
    clock()
    return "clock started"


@app.route("/russianxmas", methods=["GET"])
def russianxmas_view():
    russian_xmas()
    return "russian xmas started"


@app.route("/shutdown", methods=['GET'])
def shutdown():
    all_off()
    clear_clock()
    return "all threads paused"


if __name__ == '__main__':
    # Run server
    app.run(
        debug=True,
        host='0.0.0.0',
              #os.environ.get("192.168.0.106"),
        port=5000,
              #os.environ.get(80),
        threaded=True)

    # app.run(
    #    debug=True,
    #    threaded=True)
