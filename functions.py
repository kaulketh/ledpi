#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
conains function calls to control lights
"""
import time
import logger
from light_effects.clock import run_clock, stop_clock


# TODO: Simplify functions and summarize / refactor

animation = "animation"
advent = "advent"
clock = "clock"
xmas = "xmas"


log = logger.get_logger("Functions")
stop_flag = None
running_function = None
check_time = 2


def func_xmas():
    global running_function
    running_function = xmas
    global stop_flag
    stop_flag = False
    # TODO: insert 'Xmas' call here
    while True:
        if (not stop_flag) and (running_function == xmas):
            log.info(xmas + " is running")
            time.sleep(check_time)
        else:
            log.info(xmas + " stopped")
            break
    return


def func_animate():
    global running_function
    running_function = animation
    global stop_flag
    stop_flag = False
    # TODO: insert 'animation' call here
    while True:
        if (not stop_flag) and (running_function == animation):
            log.info(animation + " is running")
            time.sleep(check_time)
        else:
            log.info(animation + " stopped")
            break
    return


def func_clock():
    global running_function
    running_function = clock
    global stop_flag
    stop_flag = False
    run_clock()
    while True:
        if (not stop_flag) and (running_function == clock):
            log.info(clock + " is running")
            time.sleep(check_time)
        else:
            log.info(clock + " stopped")
            break
    return


def func_advent():
    global running_function
    running_function = advent
    global stop_flag
    stop_flag = False
    # TODO: insert 'advent' call here
    while True:
        if (not stop_flag) and (running_function == advent):
            log.info(advent + "is running")
            time.sleep(check_time)
        else:
            log.info(advent  + " stopped")
            break
    return


def functions_off():
    log.info('called functions off')
    global running_function
    running_function = None
    global stop_flag
    stop_flag = True
    log.debug('stop_flag: = ' + str(stop_flag))
    stop_clock()
    # TODO: insert stop calls of every functions here
    # .
    # .
    # .
    return
