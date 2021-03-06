#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
any animation for 24-LEDs-stripe
"""

from neopixel import Color

import logger
from light_effects.led_strip import get_strip, reset_strip
from light_effects.effects import color_wipe_full, theater_chase

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

log = logger.get_logger("Theater")
stop_flag = None


def stop_theater():
    global stop_flag
    stop_flag = True
    log.debug('theater stop_flag was set to ' + str(stop_flag))
    return stop_flag


# noinspection PyBroadException
def run_theater():
    strip = get_strip()
    global stop_flag
    stop_flag = False
    log.info('theater started, stop_flag = ' + str(stop_flag))
    for i in range(0, strip.numPixels(), 1):
        strip.setPixelColor(i, Color(0, 0, 0))

    while not stop_flag:
        try:
            color_wipe_full(strip, Color(127, 0, 0))  # Green wipe
            if not stop_flag:
                color_wipe_full(strip, Color(0, 127, 0))  # Red wipe
            if not stop_flag:
                color_wipe_full(strip, Color(0, 0, 127))  # Blue wipe
            if not stop_flag:
                theater_chase(strip, Color(127, 127, 127))  # White theater chase
            if not stop_flag:
                theater_chase(strip, Color(0, 0, 127))  # Blue theater chase
            if not stop_flag:
                theater_chase(strip, Color(80, 0, 0))  # Green theater chase

        except KeyboardInterrupt:
            log.warn("KeyboardInterrupt")
            color_wipe_full(strip, Color(0, 0, 0), 0)
            exit()

        except Exception as e:
            log.error("Any error occurs: " + str(e))
            exit()

    log.info('theater run stopped')
    reset_strip(strip)
    return


if __name__ == '__main__':
    run_theater()
