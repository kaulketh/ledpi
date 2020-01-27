#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
simulation of advent/xmas calendar for 24-LEDs-strip
"""
import time
from datetime import date, timedelta, datetime
from random import randint

from neopixel import Color

import logger
from light_effects.candles import candle, percent
from light_effects.effects import color_wipe_full, clear, theater_chase

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

log = logger.get_logger("Advent")
stop_flag = None

# any warm white / no bright yellow
fav_red = 195
fav_green = 125
fav_blue = 30

adv_red = 200
adv_green = 30
adv_blue = 0


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
def december_cycle(strip, month):
    advent = []
    year = datetime.now().year

    try:
        # collect advent dates
        xmas = date(year, month, 25)
        for d in allsundays(year):
            if d < xmas:
                advent.append(d.day)

        while True:
            # advent = [2, 8, 12, 16]  # uncomment and adapt to test
            day = datetime.now().day
            # day = 22  # uncomment and adapt to test
            # ensure only the day related LEDs are set as candle
            if strip.numPixels() > day:
                for i in range(day):
                    p = percent()
                    # set up different colors for days
                    if (i + 1) in advent:
                        strip.setPixelColor(i, Color(int(adv_green * p), int(adv_red * p), int(adv_blue * p)))
                    else:
                        strip.setPixelColor(i, Color(int(fav_green * p), int(fav_red * p), int(fav_blue * p)))
                    strip.show()
                time.sleep(randint(13, 15) / 100.0)
            else:
                candle(strip, strip.numPixels())

            global stop_flag
            if stop_flag:
                break

    except KeyboardInterrupt:
        log.warn("KeyboardInterrupt")
        color_wipe_full(strip, Color(0, 0, 0), 10)
        exit()

    except Exception as e:
        log.error("Any error occurs: " + str(e))
        exit()


def stop_advent():
    global stop_flag
    stop_flag = True
    log.debug('advent stop_flag was set to ' + str(stop_flag))
    return stop_flag


def run_advent():
    month = datetime.now().month
    # month = 12  # uncomment to test
    from light_effects.led_strip import get_strip
    strip = get_strip()
    global stop_flag
    stop_flag = False
    log.info('advent started, stop_flag = ' + str(stop_flag))
    while True:
        if month != 12:
            log.warn('Wrong month for xmas/advent animation, it\'s {0}!'.format(time.strftime("%B")))
            while not stop_flag:
                theater_chase(strip, Color(0, 15, 0))
            clear(strip)
        else:
            december_cycle(strip, month)
        if stop_flag:
            break
    return


if __name__ == '__main__':
    pass
