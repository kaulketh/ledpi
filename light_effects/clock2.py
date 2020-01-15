#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
another clock for 24-LEDs-strip
"""
import datetime
import time

from neopixel import *

import logger
from light_effects.effects import color_wipe

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

log = logger.get_logger("Clock 2")
stop_flag = None


def stop_clock2():
    global stop_flag
    stop_flag = True
    log.debug('clock 2 stop_flag was set to ' + str(stop_flag))
    return stop_flag


def run_clock2():
    from light_effects import get_strip
    strip = get_strip()

    global stop_flag
    stop_flag = False
    log.info('clock 2 started, stop_flag = ' + str(stop_flag))

    for i in range(0, strip.numPixels(), 1):
        strip.setPixelColor(i, Color(0, 0, 0))
    while True:
        # noinspection PyBroadException
        try:
            now = datetime.datetime.now()

            # Low light during 18-8 o'clock
            if 8 < now.hour < 18:
                strip.setBrightness(127)
            else:
                strip.setBrightness(25)

            hour = now.hour % 12 * 2
            minute = (now.minute / 5 % 12 * 2) + 1
            second = now.second / 5 * 2
            secondmodulo = now.second % 5
            timeslot_in_microseconds = secondmodulo * 1000000 + now.microsecond
            for i in range(0, strip.numPixels(), 1):
                secondplusone = second + 1 if (second < 23) else 0
                secondminusone = second - 1 if (second > 0) else 23
                colorarray = [0, 0, 0]

                if i == second:
                    if timeslot_in_microseconds < 2500000:
                        colorarray[0] = int(
                            0.0000508 * timeslot_in_microseconds) + 126
                    else:
                        colorarray[0] = 382 - \
                                        int(0.0000508 * timeslot_in_microseconds)
                if i == secondplusone:
                    colorarray[0] = int(0.0000256 * timeslot_in_microseconds)
                if i == secondminusone:
                    colorarray[0] = int(
                        0.0000256 * timeslot_in_microseconds) * -1 + 128
                if i == minute:
                    colorarray[2] = 200
                if i == hour:
                    colorarray[1] = 200
                strip.setPixelColor(
                    i, Color(colorarray[0], colorarray[1], colorarray[2]))
            strip.show()
            time.sleep(0.1)
            if stop_flag:
                break

        except KeyboardInterrupt:
            log.warn("KeyboardInterrupt: {0}", exec_info=1)
            color_wipe(strip, Color(0, 0, 0), 10)
            exit()

        except Exception:
            log.error("Any error occurs: {0}", exec_info=1)

    log.info('clock 2 run stopped')
    color_wipe(strip, Color(0, 0, 0), 10)
    log.debug('LED stripe cleared')
    return


if __name__ == '__main__':
    pass
