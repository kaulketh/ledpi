#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
will be containing the functions to control lights
"""

import logger
from clock import run_clock, clear_clock

log = logger.get_logger("Functions")

def func_xmas():
    log.info('xmas')
    return


def func_animate():
    log.info('animation')
    return


def func_clock():
    log.info('clock')
    # run_clock()
    return


def func_advent():
    log.info('advent')
    return


def func_all_off():
    log.info('all off')
    # clear_clock(True)
    return
