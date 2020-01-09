#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import time
from multiprocessing import Process, Queue

from flask import Flask, render_template

import clock
from functions import animate, all_off, advent, xmas, stop_threads
from raspi import RaspberryThread

some_threads = None
some_queue = None

app = Flask(__name__)


# # CORS(app)
# @app.after_request
# def after_request(response):
#     print('after_request called')
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers',
#                          'Access-Control-Allow-Headers, Origin, Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers')
#     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#     return response


@app.route("/")
def index():
    return render_template("ui.html")


@app.route("/control", strict_slashes=False)
def service():
    return render_template("control.html")


@app.route("/animate", methods=["GET"])
def animation_view():
    # stop_threads(threads)
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
    # stop_threads(threads)
    any(thread.pause() for thread in threads)
    if not advent_thread.isAlive():
        advent_thread.start()
    advent_thread.resume()
    return "advent calendar started"


@app.route("/clock", methods=["GET"])
def clock_view():
    # stop_threads(threads)
    any(thread.pause() for thread in threads)
    if not clock_thread.isAlive():
        clock_thread.start()
    clock_thread.resume()
    return "clock started"


@app.route("/xmas", methods=["GET"])
def xmas_view():
    # stop_threads(threads)
    any(thread.pause() for thread in threads)
    if not xmas_thread.isAlive():
        xmas_thread.start()
    xmas_thread.resume()
    return "russian xmas started"


@app.route("/stop", methods=["GET"])
def shutdown():
    all_off()
    any(thread.pause() for thread in threads)
    # stop_threads(threads)
    return "all threads paused"


@app.route("/restart")
def restart():
    try:
        any(thread.pause() for thread in threads)
        some_queue.put("something")
        print "Restarted successfully"
        return "Quit"
    except:
        print "Failed in restart"
        return "Failed"


@app.route("/reboot", methods=["GET"])
def reboot():
    os.system('sudo reboot')
    return "device rebooted"


# Create threads
threads = []
animate_thread = RaspberryThread(function=animate)
clock_thread = RaspberryThread(function=clock)
xmas_thread = RaspberryThread(function=xmas)
advent_thread = RaspberryThread(function=advent)
# collect threads
threads.append(animate_thread)
threads.append(clock_thread)
threads.append(xmas_thread)
threads.append(advent_thread)


def _start_flaskapp(any_queue, any_threads):
    global some_queue
    some_queue = any_queue

    global some_threads
    some_threads = any_threads

    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        threaded=True)


if __name__ == '__main__':

    queue = Queue()
    process = Process(target=_start_flaskapp, args=(queue, threads,))
    process.start()
    while True:  # wathing queue, if there is no call than sleep, otherwise break
        if queue.empty():
            time.sleep(1)
        else:
            break
    process.terminate()  # terminate flaskapp and then restart the app on subprocess
    args = [sys.executable] + [sys.argv[0]]
    subprocess.call(args)

    # Run server
    # app.run(
    #     debug=True,
    #     host='0.0.0.0',
    #     port=5000,
    #     threaded=True)
