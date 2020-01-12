#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
clock for 24-LEDs-strip
"""
import datetime
import time

from neopixel import *

import logger

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

from light_effects.led_strip import get_strip

hR = 200
hG = 0
hB = 0

mR = 0
mG = 0
mB = 200

sR = 184
sG = 134
sB = 11

log = logger.get_logger("Clock")
stop_flag = None
strip = get_strip()


# noinspection PyShadowingNames
def color_wipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)
    return


def stop_clock():
    global stop_flag
    stop_flag = True
    log.debug('clock stop_flag was set to ' + str(stop_flag))
    # color_wipe(strip, Color(0, 0, 0), 10)
    return


def run_clock():
    global stop_flag
    stop_flag = False
    log.info('clock started, stop_flag = ' + str(stop_flag))

    for i in range(0, strip.numPixels(), 1):
        strip.setPixelColor(i, Color(0, 0, 0))

    while True:
        # noinspection PyBroadException
        try:
            now = datetime.datetime.now()
            hour = int(int(now.hour) % 12 * 2)
            minute = (int(int(now.minute) / 5 % 12 * 2)) + 1
            second = int(int(now.second) / 2.5)

            # Low light during given period
            if 8 < int(now.hour) < 18:
                strip.setBrightness(200)
            else:
                strip.setBrightness(25)

            for i in range(0, strip.numPixels(), 1):

                # hour
                strip.setPixelColorRGB(hour, hG, hR, hB)

                # minute
                if minute == hour:
                    # TODO doesnt work
                    strip.setPixelColorRGB(minute + 1, mG, mR, mB)
                else:
                    strip.setPixelColorRGB(minute, mG, mR, mB)

                if minute > 30:
                    if hour <= 22:
                        strip.setPixelColorRGB(hour + 1, hG, hR, hB)
                    else:
                        strip.setPixelColorRGB(0, hG, hR, hB)

                # second
                if i == second:
                    strip.setPixelColorRGB(i, sG, sR, sB)
                else:
                    strip.setPixelColorRGB(i, 0, 0, 0)

            strip.show()
            time.sleep(0.1)
            global stop_flag
            if stop_flag:
                break

        except KeyboardInterrupt:
            print()
            log.warn("KeyboardInterrupt: {0}", exec_info=1)
            color_wipe(strip, Color(0, 0, 0), 10)
            exit()

        except Exception:
            log.error("Any error occurs: {0}", exec_info=1)

    log.debug('clock run stopped')
    color_wipe(strip, Color(0, 0, 0), 10)
    log.debug('LED stripe cleared')
    return


if __name__ == '__main__':
    pass
