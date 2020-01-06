#!/usr/bin/python
# -*- coding: utf-8 -*-


from flask import Flask, render_template
from raspi import RaspberryThread
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
    # Pause any running threads
    any(thread.pause() for thread in threads)

    # Start the target thread if it is not running
    if not animate_thread.isAlive():
        animate_thread.start()
    # Unpause the thread and thus execute its function
    animate_thread.resume()
    return "animation started"


@app.route("/advent", methods=["GET"])
def advent_view():
    clear_clock()
    any(thread.pause() for thread in threads)
    if not advent_thread.isAlive():
        advent_thread.start()
    advent_thread.resume()
    return "advent calendar started"


@app.route("/clock", methods=["GET"])
def clock_view():
    any(thread.pause() for thread in threads)
    if not clock_thread.isAlive():
        clock_thread.start()
    clock_thread.resume()
    return "clock started"


@app.route("/russianxmas", methods=["GET"])
def russianxmas_view():
    clear_clock()
    any(thread.pause() for thread in threads)
    if not russian_xmas_thread.isAlive():
        russian_xmas_thread.start()
    russian_xmas_thread.resume()
    return "russian xmas started"


@app.route("/shutdown", methods=['GET'])
def shutdown():
    any(thread.pause() for thread in threads)
    all_off()
    clear_clock()
    return "all threads paused"


if __name__ == '__main__':
    # Create threads
    animate_thread = RaspberryThread(function=animate)
    clock_thread = RaspberryThread(function=clock)
    russian_xmas_thread = RaspberryThread(function=russian_xmas)
    advent_thread = RaspberryThread(function=advent)

    # collect threads
    threads = [
        animate_thread,
        clock_thread,
        russian_xmas_thread,
        advent_thread
    ]

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
