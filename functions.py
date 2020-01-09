#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
will be containing the functions to control lights
"""

from clock import run_clock, clear_clock


def stop_threads(threads):
    for thread in threads:
        thread.pause()
        if not thread.stopped() and thread.isAlive():
            # log.debug('stopping ' + thread.getName())
            thread.stop()
    # clock.clear(led_strip.strip)
    return


def xmas():
    print('xmas')
    #return


def animate():
    print('animation')
    return


def clock():
    print('clock')
    run_clock()
    return


def advent():
    print('advent')
    return


def all_off():
    print('all off')
    clear_clock(True)
    return
