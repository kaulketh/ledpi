#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
any animation for 24-LEDs-strip
"""
import time
from random import randint

from neopixel import Color

import logger

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

from light_effects.effects import color_wipe_full

log = logger.get_logger("Candles")
stop_flag = None
# any warm white / no bright yellow
red = 195
green = 150
blue = 50


def stop_candles():
    global stop_flag
    stop_flag = True
    log.debug('candles stop_flag was set to ' + str(stop_flag))
    return stop_flag


# noinspection PyBroadException
def run_candles():
    from light_effects import get_strip
    strip = get_strip()
    global stop_flag
    stop_flag = False
    log.info('candles started, stop_flag = ' + str(stop_flag))
    try:
        while True:
            candle(strip, strip.numPixels())
            if stop_flag:
                break

    except KeyboardInterrupt:
        log.warn("KeyboardInterrupt")
        exit()

    except Exception as e:
        log.error("Any error occurs: " + str(e))
        exit()

    log.info('candles run stopped')
    color_wipe_full(strip, Color(0, 0, 0), 10)
    log.debug('LED stripe cleared')
    return


# candle lights from 0 to leds
def candle(strip, leds):
    for i in range(leds):
        div = randint(randint(6, 8), randint(30, 40))
        strip.setPixelColor(i, Color(green / div, red / div, blue / div))
    strip.show()
    time.sleep(0.15)


if __name__ == '__main__':
    pass
