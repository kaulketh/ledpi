#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
contains methods to call light effect functions
"""

import time

import logger
from light_effects.advent import run_advent, stop_advent
from light_effects.animation import run_animation, stop_animation
from light_effects.clock import run_clock, stop_clock
from light_effects.xmas import run_xmas, stop_xmas

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

log = logger.get_logger("Functions")
stop_flag = None
running_function = None

animation = "animation"
advent = "advent"
clock = "clock"
xmas = "xmas"


def observe(function):
    global running_function, stop_flag
    running_function = function
    while True:
        if (not stop_flag) and (running_function == function):
            log.debug(function + " is running")
            time.sleep(0.5)
        else:
            log.debug(function + " stopped")
            break


def func_xmas():
    global stop_flag
    stop_flag = False
    run_xmas()
    observe(xmas)
    return


def func_animate():
    global stop_flag
    stop_flag = False
    run_animation()
    observe(animation)
    return


def func_clock():
    global stop_flag
    stop_flag = False
    run_clock()
    observe(clock)
    return


def func_advent():
    global stop_flag
    stop_flag = False
    run_advent()
    observe(advent)
    return


def functions_off():
    log.info("functions off")
    global running_function, stop_flag
    running_function = ""
    stop_flag = True
    log.debug('stop_flag: = ' + str(stop_flag))
    stop_clock()
    stop_animation()
    stop_advent()
    stop_xmas()
    return


if __name__ == '__main__':
    pass
