#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
contains methods to call light effect functions
"""

import logger
from light_effects.advent import run_advent, stop_advent
from light_effects.candles import run_candles, stop_candles
from light_effects.rainbow import run_rainbow, stop_rainbow
from light_effects.clock import run_clock, stop_clock
from light_effects.clock2 import run_clock2, stop_clock2
from light_effects.theater import run_theater, stop_theater


__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

log = logger.get_logger("Functions")

stop_flag = None
running_function = None
status = None

theater = "theater"
advent = "advent"
clock1 = "clock 1"
clock2 = "clock 2"
rainbow = "rainbow"
candles = "candles"
off = "all off"


def get_status():
    global status
    if status is None:
        status = off
    log.debug('Status: ' + status.upper())
    return status


def set_status(state):
    global status
    status = state
    log.debug('Status set to ' + status.upper())
    return


# TODO: implement switcher for function calls and refactor
def func_candles():
    if functions_off():
        global stop_flag
        stop_flag = False
        set_status(candles)
        run_candles()
        return


def func_rainbow():
    if functions_off():
        global stop_flag
        stop_flag = False
        set_status(rainbow)
        run_rainbow()
        return


def func_theater():
    if functions_off():
        global stop_flag
        stop_flag = False
        set_status(theater)
        run_theater()
        return


def func_clock1():
    if functions_off():
        global stop_flag
        stop_flag = False
        set_status(clock1)
        run_clock()
        return


def func_clock2():
    if functions_off():
        global stop_flag
        stop_flag = False
        set_status(clock2)
        run_clock2()
    return


def func_advent():
    if functions_off():
        global stop_flag
        stop_flag = False
        set_status(advent)
        run_advent()
    return


def functions_off():
    global running_function
    running_function = ""
    global stop_flag
    stop_flag = True
    log.debug('stop_flag: = ' + str(stop_flag))
    if stop_clock() and stop_clock2() and stop_theater() and stop_advent() and stop_rainbow() and stop_candles():
        set_status(off)
        log.info("functions off")
        return True
    else:
        return False


if __name__ == '__main__':
    pass
