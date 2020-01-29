#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
main script for app and flask
"""
import os
from multiprocessing import Process

import flask_monitoringdashboard as dashboard
from flask import Flask, render_template

import functions
import logger
from functions import func_theater, functions_off, func_advent, func_rainbow, func_clock1, func_clock2, func_candles, \
    get_status

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

candles_proc = None
theater_proc = None
clock_proc = None
clock2_proc = None
rainbow_proc = None
advent_proc = None
running_processes = []

app_name = "PiApp"
log = logger.get_logger(app_name)
app = Flask(app_name)
dashboard.bind(app)


# region pages
@app.route("/", methods=['GET', 'POST'])
def index():
    log.info("Browse start page")
    return render_template("index.html", status=get_status().upper())


@app.route("/service", methods=['GET'])
def service():
    log.info("Browse service page")
    return render_template("service.html")
# endregion


# region functions
@app.route("/theater", methods=["GET"])
def theater_view():
    msg = "Theater process called"
    log.info(msg)
    global theater_proc
    theater_proc = start_process(func_theater(), functions.theater)
    return msg


@app.route("/advent", methods=["GET"])
def advent_view():
    msg = "Advent calendar process called"
    log.info(msg)
    global advent_proc
    advent_proc = start_process(func_advent(), functions.advent)
    return msg


@app.route("/clock 1", methods=["GET"])
def clock_view():
    msg = "Clock 1 process called"
    log.info(msg)
    global clock_proc
    clock_proc = start_process(func_clock1(), functions.clock1)
    return msg


@app.route("/clock 2", methods=["GET"])
def clock2_view():
    msg = "Clock 2 process called"
    log.info(msg)
    global clock2_proc
    clock2_proc = start_process(func_clock2(), functions.clock2)
    return msg


@app.route("/rainbow", methods=["GET"])
def circus_view():
    msg = "Rainbow process called"
    log.info(msg)
    global rainbow_proc
    rainbow_proc = start_process(func_rainbow(), functions.rainbow)
    return msg


@app.route("/candles", methods=["GET"])
def candles_view():
    msg = "Candles process called"
    log.info(msg)
    global candles_proc
    candles_proc = start_process(func_candles(), functions.candles)
    return msg


@app.route("/all off", methods=["GET"])
def off_view():
    stop_everything()
    msg = "All should paused"
    log.info(msg)
    return msg


# TODO: implement hidden functions for service and maintenance
@app.route("/help", methods=["GET"])
def help_me():
    # implement help
    pass


@app.route("/panic", methods=["GET"])
def panic():
    reboot()


@app.route("/shutdown <param>", methods=["GET"])
def sutdown(param):
    stop_everything()
    msg = "Device shut down with parameter: " + param
    log.info(msg)
    os.system('sudo shutdown ' + param)


@app.route("/reboot", methods=["GET"])
def reboot():
    stop_everything()
    msg = "Device reboot"
    log.info(msg)
    os.system('sudo reboot')
# endregion


# region methods
def start_process(ftarget, fname):
    try:
        global running_processes
        proc = Process(target=ftarget, name=fname)
        log.debug('Start and append to process list: ' + proc.name)
        running_processes.append(proc)
        proc.daemon = True
        proc.start()
        return proc
    except Exception as e:
        log.error("Failed to start process " + fname + ': ' + str(e))
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
    if functions_off():
        global running_processes
        if running_processes.__len__() > 0:
            for p in running_processes:
                log.debug("Stopping " + p.name)
                stop_process(p)
        else:
            log.debug('Nothing to kill ;-)')


def start_flask_app():
    try:
        app.run(
            debug=False,
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
