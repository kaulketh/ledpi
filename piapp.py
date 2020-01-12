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

from flask import Flask, render_template

import logger
from functions import func_animate, functions_off, func_advent, func_xmas, func_clock

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

app_name = "PiApp"
log = logger.get_logger(app_name)

some_queue = None
animation_proc = None
clock_proc = None
xmas_proc = None
advent_proc = None
running_processes = []

app = Flask(app_name)


# region pages
@app.route("/")
def index():
    log.info("Browse UI")
    return render_template("ui.html")


@app.route("/control")
def service():
    log.info("Browse Service")
    return render_template("control.html")
# endregion


# region functions
@app.route("/animate", methods=["GET"])
def animation_view():
    msg = "animation process called"
    log.info(msg)
    stop_everything()
    global animation_proc
    animation_proc = start_process(func_animate())
    return msg


@app.route("/advent", methods=["GET"])
def advent_view():
    msg = "advent calendar process called"
    log.info(msg)
    stop_everything()
    global advent_proc
    advent_proc = start_process(func_advent())
    return msg


@app.route("/clock", methods=["GET"])
def clock_view():
    msg = "clock process called"
    log.info(msg)
    stop_everything()
    global clock_proc
    clock_proc = start_process(func_clock())
    return msg


@app.route("/xmas", methods=["GET"])
def xmas_view():
    msg = "xmas process called"
    log.info(msg)
    stop_everything()
    global xmas_proc
    xmas_proc = start_process(func_xmas())
    return msg


@app.route("/stop", methods=["GET"])
def shutdown():
    msg = "all should paused"
    log.info(msg)
    stop_everything()
    return msg


# noinspection PyBroadException
@app.route("/restart", methods=["GET"])
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
    """

    :return:
    :type process_to_stop: Process
    """
    global running_processes
    running_processes.remove(process_to_stop)
    log.debug(process_to_stop.name + ' removed from list')
    process_to_stop.terminate()
    log.debug(process_to_stop.name + ' terminated')
    return process_to_stop


def stop_everything():
    functions_off()
    time.sleep(1)
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
            debug=False,
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
