#!/usr/bin/python3
# -*- coding: utf-8 -*-

from neopixel import *

import logger
from light_effects.led_strip import get_strip, reset_strip
from light_effects.effects import rainbow_cycle  # , theater_chase_rainbow

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

log = logger.get_logger("Rainbow")
stop_flag = None


def stop_rainbow():
    global stop_flag
    stop_flag = True
    log.debug('rainbow stop_flag was set to ' + str(stop_flag))
    return stop_flag


def run_rainbow():
    strip = get_strip()
    global stop_flag
    stop_flag = False
    log.info('rainbow started, stop_flag = ' + str(stop_flag))
    for i in range(0, strip.numPixels(), 1):
        strip.setPixelColor(i, Color(0, 0, 0))
    b = 80
    while not stop_flag:
        try:
            strip.setBrightness(b)
            rainbow_cycle(strip)
            # theater_chase_rainbow(stripe)
            if not stop_flag:
                b -= 10
            if b <= 30 and not stop_flag:
                while b <= 80 and not stop_flag:
                    strip.setBrightness(b)
                    rainbow_cycle(strip)
                    # theater_chase_rainbow(stripe)
                    if not stop_flag:
                        b += 10
                if not stop_flag:
                    b = 80

        except KeyboardInterrupt:
            log.warn("KeyboardInterrupt")
            exit()

        except Exception as e:
            log.error("Any error occurs: " + str(e))
            exit()

    log.info('rainbow run stopped')
    reset_strip(strip)
    return


if __name__ == '__main__':
    run_rainbow()
