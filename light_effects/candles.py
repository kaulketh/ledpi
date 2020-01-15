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

from light_effects.effects import color_wipe

log = logger.get_logger("Candles")
stop_flag = None
# any warm white / no bright yellow
sR = 195
sG = 150
sB = 50


def stop_candles():
    global stop_flag
    stop_flag = True
    log.debug('candles stop_flag was set to ' + str(stop_flag))
    return stop_flag


def run_candles():
    from light_effects import get_strip
    strip = get_strip()
    global stop_flag
    stop_flag = False
    log.info('candles started, stop_flag = ' + str(stop_flag))
    try:
        while True:
            for i in range(strip.numPixels()):
                div = randint(randint(6, 8), randint(30, 40))
                strip.setPixelColor(i, Color(sG / div, sR / div, sB / div))
            strip.show()
            time.sleep(0.15)

            if stop_flag:
                break

    except KeyboardInterrupt:
        print()
        log.warn("KeyboardInterrupt: {0}", exec_info=1)
        color_wipe(get_strip(), Color(0, 0, 0), 10)
        exit()

    except Exception:
        log.error("Any error occurs: {0}", exec_info=1)

    log.info('candles run stopped')
    color_wipe(get_strip(), Color(0, 0, 0), 10)
    log.debug('LED stripe cleared')
    return


if __name__ == '__main__':
    pass
