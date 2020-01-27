#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
another clock for 24-LEDs-strip
"""
import datetime
import time

from neopixel import *

import logger
from light_effects.effects import color_wipe_full, clear

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

# color hours
hR = 100
hG = 20
hB = 0

# color minutes
mR = 20
mG = 0
mB = 100

# color seconds
sR = 6
sG = 30
sB = 10

log = logger.get_logger("Clock")
stop_flag = None


def stop_clock():
    global stop_flag
    stop_flag = True
    log.debug('clock 1 stop_flag was set to ' + str(stop_flag))
    return stop_flag


def run_clock():
    from light_effects import get_strip
    strip = get_strip()

    global stop_flag
    stop_flag = False
    log.info('clock 1 started, stop_flag = ' + str(stop_flag))

    for i in range(0, strip.numPixels(), 1):
        strip.setPixelColor(i, Color(0, 0, 0))

    while True:
        # noinspection PyBroadException
        try:
            now = datetime.datetime.now()
            led_for_hour = int(int(now.hour) % 12 * 2)
            led_for_minute = int(round(now.minute / 2.5))
            leds_per_2500ms = int(round(now.second / 2.5))

            # Low light during given period
            if 8 < int(now.hour) < 18:
                strip.setBrightness(127)
            else:
                strip.setBrightness(50)

            __seconds(leds_per_2500ms, strip)

            __minute(led_for_minute, led_for_hour, strip)

            __hour(led_for_hour, led_for_minute, strip)

            strip.show()
            if leds_per_2500ms == strip.numPixels():
                time.sleep(1.5)
                clear(strip)

            if stop_flag:
                break

        except KeyboardInterrupt:
            print()
            log.warn("KeyboardInterrupt.")
            color_wipe_full(strip, Color(0, 0, 0), 10)
            exit()

        except Exception as e:
            log.error("Any error occurs: " + str(e))
            exit()

    log.info('clock 1 run stopped')
    color_wipe_full(strip, Color(0, 0, 0), 10)
    log.debug('LED stripe cleared')
    return


def __wipe(strip, wait_ms=50, color=Color(0, 0, 0)):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)


def __clear(strip):
    for i in range(0, strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))


def __seconds(leds_per_2500ms, strip):
    for led in range(0, leds_per_2500ms, 1):
        if 0 < (led + 1) < strip.numPixels():
            strip.setPixelColorRGB(led + 1, sG, sR, sB)
        if (led + 1) == strip.numPixels():
            strip.setPixelColorRGB(0, sG, sR, sB)


def __minute(led, led_hour, strip):
    if led < strip.numPixels():
        if led == led_hour:
            __set_minute_led_before_and_after(strip, led)
        else:
            strip.setPixelColorRGB(led, mG, mR, mB)
    if led >= strip.numPixels():
        if led == led_hour:
            __set_minute_led_before_and_after(strip, led_hour)
            strip.setPixelColorRGB(0, mG, mR, mB)
        else:
            strip.setPixelColorRGB(0, mG, mR, mB)


def __set_minute_led_before_and_after(strip, led):
    strip.setPixelColorRGB(led - 1, int(mG / 5), int(mR / 5), int(mB / 5))
    strip.setPixelColorRGB(led + 1, int(mG / 5), int(mR / 5), int(mB / 5))


def __hour(led, led_minute, strip):
    if 0 < led < strip.numPixels():
        # past half
        if led_minute > 12:
            strip.setPixelColorRGB(led, hG, hR, hB)
            strip.setPixelColorRGB(led + 1, int(hG / 5), int(hR / 5), int(hB / 5))
        # past quarter to next hour
        if led_minute > 18:
            strip.setPixelColorRGB(led, int(hG / 5), int(hR / 5), int(hB / 5))
            strip.setPixelColorRGB(led + 1, hG, hR, hB)
            strip.setPixelColorRGB(led + 2, int(hG / 5), int(hR / 5), int(hB / 5))
        else:
            strip.setPixelColorRGB(led, hG, hR, hB)
    if led >= strip.numPixels():
        strip.setPixelColorRGB(0, hG, hR, hB)


if __name__ == '__main__':
    pass
