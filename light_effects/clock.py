#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
another clock for 24-LEDs-stripe
"""
import datetime
import time

from neopixel import *

import logger
from light_effects.led_strip import get_strip, reset_strip

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

log = logger.get_logger("Clock 1")
stop_flag = None


def stop_clock():
    global stop_flag
    stop_flag = True
    log.debug('clock 1 stop_flag was set to ' + str(stop_flag))
    return stop_flag


def run_clock():
    strip = get_strip()
    global stop_flag
    stop_flag = False
    log.info('clock 1 started, stop_flag = ' + str(stop_flag))
    for i in range(0, strip.numPixels(), 1):
        strip.setPixelColor(i, Color(0, 0, 0))

    while not stop_flag:
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

            _seconds(leds_per_2500ms, strip)

            _minute(led_for_minute, led_for_hour, strip)

            _hour(led_for_hour, led_for_minute, strip)

            strip.show()
            if leds_per_2500ms == strip.numPixels():
                time.sleep(1.5)
                _clear(strip)

        except KeyboardInterrupt:
            log.warn("KeyboardInterrupt.")
            _wipe(strip, 0)
            exit()

        except Exception as e:
            log.error("Any error occurs: " + str(e))
            exit()

    log.info('clock 1 run stopped')
    _wipe(strip, 0)
    reset_strip(strip)
    return


def _wipe(stripe, wait_ms=50, color=Color(0, 0, 0)):
    for i in range(stripe.numPixels()):
        stripe.setPixelColor(i, color)
        stripe.show()
        time.sleep(wait_ms / 1000.0)


def _clear(stripe):
    for i in range(0, stripe.numPixels()):
        stripe.setPixelColor(i, Color(0, 0, 0))


def _seconds(leds_per_2500ms, stripe):
    for led in range(0, leds_per_2500ms, 1):
        if 0 < (led + 1) < stripe.numPixels():
            stripe.setPixelColorRGB(led + 1, sG, sR, sB)
        if (led + 1) == stripe.numPixels():
            stripe.setPixelColorRGB(0, sG, sR, sB)


def _minute(led, led_hour, stripe):
    if led < stripe.numPixels():
        if led == led_hour:
            _set_minute_led_before_and_after(stripe, led)
        else:
            stripe.setPixelColorRGB(led, mG, mR, mB)
    if led >= stripe.numPixels():
        if led == led_hour:
            _set_minute_led_before_and_after(stripe, led_hour)
            stripe.setPixelColorRGB(0, mG, mR, mB)
        else:
            stripe.setPixelColorRGB(0, mG, mR, mB)


def _set_minute_led_before_and_after(stripe, led):
    stripe.setPixelColorRGB(led - 1, int(mG / 5), int(mR / 5), int(mB / 5))
    stripe.setPixelColorRGB(led + 1, int(mG / 5), int(mR / 5), int(mB / 5))


def _hour(led, led_minute, stripe):
    if 0 < led < stripe.numPixels():
        # past half
        if led_minute > 12:
            stripe.setPixelColorRGB(led, hG, hR, hB)
            stripe.setPixelColorRGB(led + 1, int(hG / 5), int(hR / 5), int(hB / 5))
        # past quarter to next hour
        if led_minute > 18:
            stripe.setPixelColorRGB(led, int(hG / 5), int(hR / 5), int(hB / 5))
            stripe.setPixelColorRGB(led + 1, hG, hR, hB)
            stripe.setPixelColorRGB(led + 2, int(hG / 5), int(hR / 5), int(hB / 5))
        else:
            stripe.setPixelColorRGB(led, hG, hR, hB)
    if led >= stripe.numPixels():
        stripe.setPixelColorRGB(0, hG, hR, hB)


if __name__ == '__main__':
    run_clock()
