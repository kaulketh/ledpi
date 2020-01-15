#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
main script for app and flask
"""
import os
import subprocess
import sys
import time
from multiprocessing import Process, Queue

from flask import Flask, render_template, request

import logger
from functions import func_theater, functions_off, func_advent, func_circus, func_clock1, func_clock2, func_candles, \
    get_status

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

from light_effects.advent import run_advent

some_queue = None
candles_proc = None
theater_proc = None
clock_proc = None
clock2_proc = None
circus_proc = None
advent_proc = None
running_processes = []

app_name = "PiApp"
log = logger.get_logger(app_name)
app = Flask(app_name)


# region pages
@app.route("/", methods=['GET', 'POST'])
def index():
    log.info("Browse UI")
    return render_template("index.html", status=get_status().upper())


@app.route("/service", methods=['GET', 'POST'])
def service():
    log.info("Browse Service")
    return render_template("service.html")
# endregion


# region functions
@app.route("/theater", methods=["GET"])
def theater_view():
    msg = "theater process called"
    log.info(msg)
    global theater_proc
    theater_proc = start_process(func_theater())
    return msg


@app.route("/advent", methods=["GET"])
def advent_view():
    msg = "advent calendar process called"
    log.info(msg)
    global advent_proc
    advent_proc = start_process(func_advent())
    return msg


@app.route("/clock 1", methods=["GET"])
def clock_view():
    msg = "clock 1 process called"
    log.info(msg)
    global clock_proc
    clock_proc = start_process(func_clock1())
    return msg


@app.route("/clock 2", methods=["GET"])
def clock2_view():
    msg = "clock 2 process called"
    log.info(msg)
    global clock2_proc
    clock2_proc = start_process(func_clock2())
    return msg


@app.route("/circus", methods=["GET"])
def xmas_view():
    msg = "circus process called"
    log.info(msg)
    global circus_proc
    circus_proc = start_process(func_circus())
    return msg


@app.route("/candles", methods=["GET"])
def candles_view():
    msg = "candles process called"
    log.info(msg)
    global candles_proc
    candles_proc = start_process(func_candles())
    return msg


@app.route("/all off", methods=["GET"])
def off_view():
    stop_everything()
    msg = "all should paused"
    log.info(msg)
    return msg


# noinspection PyBroadException
@app.route("/restart", methods=["GET", 'POST'])
def restart():
    stop_everything()
    try:
        msg = "Flask restart"
        some_queue.put(msg)
        log.info(msg)
        return msg
    except Exception:
        log.error("Failed in restart: {0}", exec_info=1)
        return "Restart failed"
    except KeyboardInterrupt:
        log.warn("KeyboardInterrupt: {0}", exec_info=1)

    return render_template("index.html", status="off".upper())


@app.route("/reboot", methods=["GET"])
def reboot():
    msg = "device reboot"
    log.info(msg)
    os.system('sudo reboot')


# endregion


# region methods
def start_process(target):
    # noinspection PyBroadException
    try:
        global running_processes
        proc = Process(target=target)
        log.debug('start and append to list: ' + proc.name)
        running_processes.append(proc)
        proc.start()
        return proc
    except Exception:
        log.error("Failed to start process: {0}", exec_info=1)
    except KeyboardInterrupt:
        log.warn("KeyboardInterrupt: {0}", exec_info=1)


def stop_process(process_to_stop):
    global running_processes
    running_processes.remove(process_to_stop)
    log.debug(process_to_stop.name + ' removed from list')
    process_to_stop.terminate()
    log.debug(process_to_stop.name + ' terminated')
    return process_to_stop


def stop_everything():
    functions_off()
    time.sleep(0.5)
    global running_processes
    if running_processes.__len__() > 0:
        for p in running_processes:
            log.debug("stopping " + p.name)
            stop_process(p)
    else:
        log.debug('nothing to kill ;-)')
    return


def start_flask_app(any_queue):
    # noinspection PyBroadException
    try:
        global some_queue
        some_queue = any_queue
        log.info("start FLASK app")
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5000,
            threaded=True)
    except Exception:
        log.error("Failed to start FLASK app: {0}", exec_info=1)
    except KeyboardInterrupt:
        log.warn("KeyboardInterrupt: {0}", exec_info=1)


# endregion


if __name__ == '__main__':

    queue = Queue()
    flask_proc = Process(target=start_flask_app, args=(queue,))
    flask_proc.start()
    log.debug("FLASK process started")
    while True:  # waiting stop_flag, if there is no call than sleep, otherwise break
        if queue.empty():
            time.sleep(0.5)
        else:
            break
    flask_proc.terminate()  # terminate flask app and then restart the app on subprocess
    log.debug("FLASK process terminated")
    args = [sys.executable] + [sys.argv[0]]
    subprocess.call(args)
