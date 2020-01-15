#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
simulation of advent/xmas calendar for 24-LEDs-strip
"""
import time
from datetime import date, timedelta, datetime

from neopixel import Color

import logger
from light_effects.candles import candle
from light_effects.effects import color_wipe_full, clear, theater_chase

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

log = logger.get_logger("Advent")
stop_flag = None
# any warm white / no bright yellow
red = 195
green = 150
blue = 50
div = 20
favorite_color = Color(green / div, red / div, blue / div)


# from http://stackoverflow.com/questions/2003870/how-can-i-select-all-of-the-sundays-for-a-year-using-python
# noinspection PyShadowingNames
def allsundays(year):
    # start with Nov-27 which is the first possible day of Advent
    # 4 advents == 4 weeks == 28 days -> 25th Dec - 28 day = 27th Nov ;-)
    d = date(year, 11, 27)
    # find the next Sunday after the above date
    d += timedelta(days=6 - d.weekday())
    while d.year == year:
        yield d
        d += timedelta(days=7)


# noinspection PyBroadException
def december_cycle(strip):
    advent = []
    year = datetime.now().year

    try:
        while True:
            xmas = date(year, 12, 25)
            for d in allsundays(year):
                if d < xmas:
                    advent.append(d)

            # advent test
            # for a in advent:
            #     print str(advent.index(a) + 1) + ".Advent " + str(year) + ": " + str(a)
            #     color_wipe(strip, Color(green / div, red / div, blue / div), a.day, 15)
            #     time.sleep(5)
            #     color_wipe(strip, Color(0, 0, 0), 24, 5)
            #     time.sleep(5)

            # color_wipe(strip, favorite_color, advent[1].day, 0)
            # time.sleep(3)

            day = datetime.now().day
            if strip.numPixels() > day:
                candle(strip, day)
            else:
                candle(strip, strip.numPixels())
            global stop_flag
            if stop_flag:
                break

    except KeyboardInterrupt:
        log.warn("KeyboardInterrupt")
        color_wipe_full(strip, Color(0, 0, 0), 10)
        exit()

    except Exception:
        log.error("Any error occurs.")
        exit()


def stop_advent():
    global stop_flag
    stop_flag = True
    log.debug('advent stop_flag was set to ' + str(stop_flag))
    return stop_flag


def run_advent():
    month = datetime.now().month
    from light_effects.led_strip import get_strip
    strip = get_strip()
    global stop_flag
    stop_flag = False
    log.info('advent started, stop_flag = ' + str(stop_flag))
    while True:
        if month != 12:
            log.warn('Wrong month for xmas/advent animation, it\'s {0}!'.format(time.strftime("%B")))
            global stop_flag
            while not stop_flag:
                theater_chase(strip, Color(0, 15, 0))
            clear(strip)
        else:
            december_cycle(strip)
        if stop_flag:
            break
    return


if __name__ == '__main__':
    pass
