#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
any animation for 24-LEDs-stripe
"""
import time
from random import randint

from neopixel import Color

import logger
from light_effects.led_strip import get_strip, reset_strip

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

log = logger.get_logger("Candles")
stop_flag = None
# any warm white / no bright yellow
red = 195
green = 125
blue = 30


def stop_candles():
    global stop_flag
    stop_flag = True
    log.debug('candles stop_flag was set to ' + str(stop_flag))
    return stop_flag


# noinspection PyBroadException
def run_candles():
    strip = get_strip()
    global stop_flag
    stop_flag = False
    log.info('candles started, stop_flag = ' + str(stop_flag))
    for i in range(0, strip.numPixels(), 1):
        strip.setPixelColor(i, Color(0, 0, 0))
    try:
        while not stop_flag:
            candle(strip, strip.numPixels())

    except KeyboardInterrupt:
        log.warn("KeyboardInterrupt")
        exit()

    except Exception as e:
        log.error("Any error occurs: " + str(e))
        exit()

    log.info('candles run stopped')
    reset_strip(strip)
    return


def percent():
    scope = randint(3, 10)
    return float(scope) / float(100)


# candle lights from 0 to leds
def candle(strip, leds):
    for turns in range(leds):
        for i in range(leds):
            p = percent()
            strip.setPixelColor(i, Color(int(green * p), int(red * p), int(blue * p)))
        strip.show()
    time.sleep(randint(13, 15) / 100.0)


if __name__ == '__main__':
    run_candles()
