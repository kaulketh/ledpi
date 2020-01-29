#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
config and init 24-LEDs-stripe
"""
from neopixel import *

import logger
from light_effects.effects import  color_wipe_full

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

# LED stripe configuration:
LED_COUNT = 24  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 200  # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False

log = logger.get_logger("LED stripe")
stop_flag = None


def get_strip():
    # Create NeoPixel object with appropriate configuration.
    log.debug("Create NeoPixel object with appropriate configuration (LED Strip).")
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    # Initialize the library (must be called once before other functions).
    log.debug("Initialize: " + str(strip))
    strip.begin()
    return strip


def reset_strip(strip):
    strip.setBrightness(LED_BRIGHTNESS)
    color_wipe_full(strip, Color(0,0,0), 20)
    log.debug('LED stripe cleared.')
    return


# noinspection PyProtectedMember
def _cleanup_strip(strip: Adafruit_NeoPixel):
    strip._cleanup()
