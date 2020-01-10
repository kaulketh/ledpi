#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import time
from multiprocessing import Process, Queue

from flask import Flask, render_template


from functions import func_animate, func_all_off, func_advent, func_xmas, func_clock

some_queue = None
animation_proc = None
clock_proc = None
xmas_proc = None
advent_proc = None
running_processes = []

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("ui.html")


@app.route("/control")
def service():
    return render_template("control.html")


@app.route("/animate", methods=["GET"])
def animation_view():
    _processes_stop_all()
    global animation_proc
    animation_proc = __process_start(func_animate())
    msg = "animation process  called"
    print(msg)
    return msg


@app.route("/advent", methods=["GET"])
def advent_view():
    _processes_stop_all()
    global advent_proc
    advent_proc = __process_start(func_advent())
    msg = "advent calendar process  called"
    print(msg)
    return msg


@app.route("/clock", methods=["GET"])
def clock_view():
    _processes_stop_all()
    global clock_proc
    clock_proc = __process_start(func_clock())
    msg = "clock process  called"
    print(msg)
    return msg


@app.route("/xmas", methods=["GET"])
def xmas_view():
    _processes_stop_all()
    global xmas_proc
    xmas_proc = __process_start(func_xmas())
    msg = "xmas process called"
    print(msg)
    return msg


@app.route("/stop", methods=["GET"])
def shutdown():
    func_all_off()
    _processes_stop_all()
    msg = "all paused"
    print(msg)
    return msg


# noinspection PyBroadException
@app.route("/restart", methods=["GET"])
def restart():
    try:
        some_queue.put("something")
        print "Restarted successfully"
        return "Flask restart"
    except Exception:
        print "Failed in restart"
        return "Restart failed"


@app.route("/reboot", methods=["GET"])
def reboot():
    os.system('sudo reboot')
    msg = "device rebooted"
    print(msg)
    return msg


def __process_start(target):
    # noinspection PyBroadException
    try:
        global running_processes
        proc = Process(target=target)
        proc.start()
        print(proc.name + ' started')
        running_processes.append(proc)
        print(proc.name + ' appended to list')
        return proc
    except Exception:
        print("Failed to start process.")


def __process_stop(process_to_stop):
    """

    :return:
    :type process_to_stop: Process
    """
    global running_processes
    running_processes.remove(process_to_stop)
    print process_to_stop.name + ' removed from list'
    process_to_stop.terminate()
    print process_to_stop.name + ' terminated'
    return process_to_stop


def _processes_stop_all():
    global running_processes
    if running_processes.__len__() > 0:
        for p in running_processes:
            __process_stop(p)
    else:
        print('nothing to kill ;-)')
    return


def _start_flask_app(any_queue):
    global some_queue
    some_queue = any_queue

    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        threaded=True)


if __name__ == '__main__':

    queue = Queue()
    flask_proc = Process(target=_start_flask_app, args=(queue,))
    flask_proc.start()
    while True:  # waiting queue, if there is no call than sleep, otherwise break
        if queue.empty():
            time.sleep(0.5)
        else:
            break

    _processes_stop_all()
    flask_proc.terminate()  # terminate flask app and then restart the app on subprocess
    args = [sys.executable] + [sys.argv[0]]
    subprocess.call(args)
