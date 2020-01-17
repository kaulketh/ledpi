#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
main script for app and flask
"""
import os
import time
from multiprocessing import Process

from flask import Flask, render_template

import functions
import logger
from functions import func_theater, functions_off, func_advent, func_circus, func_clock1, func_clock2, func_candles, \
    get_status

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

candles_proc = None
theater_proc = None
clock_proc = None
clock2_proc = None
circus_proc = None
advent_proc = None
running_processes = []

app_name = "PiApp"
log = logger.get_logger(app_name)
app = Flask(app_name, template_folder="/home/pi/led/templates", static_folder="/home/pi/led/static")


# region pages
@app.route("/", methods=['GET', 'POST'])
def index():
    log.info("Browse UI")
    return render_template("index.html", status=get_status().upper())


@app.route("/service", methods=['GET'])
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
    theater_proc = start_process(func_theater(), functions.theater)
    return msg


@app.route("/advent", methods=["GET"])
def advent_view():
    msg = "advent calendar process called"
    log.info(msg)
    global advent_proc
    advent_proc = start_process(func_advent(), functions.advent)
    return msg


@app.route("/clock 1", methods=["GET"])
def clock_view():
    msg = "clock 1 process called"
    log.info(msg)
    global clock_proc
    clock_proc = start_process(func_clock1(), functions.clock1)
    return msg


@app.route("/clock 2", methods=["GET"])
def clock2_view():
    msg = "clock 2 process called"
    log.info(msg)
    global clock2_proc
    clock2_proc = start_process(func_clock2(), functions.clock2)
    return msg


@app.route("/circus", methods=["GET"])
def xmas_view():
    msg = "circus process called"
    log.info(msg)
    global circus_proc
    circus_proc = start_process(func_circus(), functions.circus)
    return msg


@app.route("/candles", methods=["GET"])
def candles_view():
    msg = "candles process called"
    log.info(msg)
    global candles_proc
    candles_proc = start_process(func_candles(), functions.candles)
    return msg


@app.route("/all off", methods=["GET"])
def off_view():
    stop_everything()
    msg = "all should paused"
    log.info(msg)
    return msg


# TODO: implement hidden functions for service and maintenance
@app.route("/help", methods=["GET"])
def help():
    # implement help
    pass


@app.route("/panic", methods=["GET"])
def panic():
    reboot()


@app.route("/shutdown <param>", methods=["GET"])
def sutdown(param):
    stop_everything()
    msg = "device shut down with parameter: " + param
    log.info(msg)
    os.system('sudo shutdown ' + param)


@app.route("/reboot", methods=["GET"])
def reboot():
    stop_everything()
    msg = "device reboot"
    log.info(msg)
    os.system('sudo reboot')


# endregion


# region methods
def start_process(ftarget, fname):
    # noinspection PyBroadException
    try:
        global running_processes
        proc = Process(target=ftarget, name=fname)
        log.debug('start and append to process list: ' + proc.name)
        running_processes.append(proc)
        proc.daemon = True
        proc.start()
        return proc
    except Exception:
        log.error("Failed to start process " + fname)
    except KeyboardInterrupt:
        log.warn("KeyboardInterrupt")


def stop_process(process_to_stop):
    global running_processes
    running_processes.remove(process_to_stop)
    log.debug(process_to_stop.name + ' removed from process list')
    process_to_stop.terminate()
    log.debug(process_to_stop.name + ' process terminated')
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


def start_flask_app():
    # noinspection PyBroadException
    try:
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5000,
            threaded=True)
    except Exception as e:
        log.error("Failed to start FLASK app: " + str(e))
        exit()
    except KeyboardInterrupt:
        log.warn("KeyboardInterrupt")
        exit()
    log.info("FLASK app started")


# endregion


if __name__ == '__main__':
    start_flask_app()
