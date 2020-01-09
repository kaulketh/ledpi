#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import time

from neopixel import *

# LED strip configuration:
LED_COUNT = 24  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False

hR = 200
hG = 0
hB = 0

mR = 0
mG = 0
mB = 200

sR = 184
sG = 134
sB = 11

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
# Initialize the library (must be called once before other functions).
strip.begin()

global active

def __get_active():
    global active
    return active


def color_wipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)


def clear_clock(stop):
    global active
    active = not stop
    print('clock active was set to ' + str(active))
    color_wipe(strip, Color(0, 0, 0), 10)



def run_clock():
    global active
    active = True
    # Create NeoPixel object with appropriate configuration.
    # strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    # Initialize the library (must be called once before other functions).
    # strip.begin()

    for i in range(0, strip.numPixels(), 1):
        strip.setPixelColor(i, Color(0, 0, 0))

    while active:
        global active
        active = __get_active()
        print('clock should run = ' + str(active))
        if not active:
            clear_clock(True)
            break

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
            # print("Clock " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))
            time.sleep(0.1)

        except KeyboardInterrupt:
            print()
            print("Program interrupted")
            color_wipe(strip, Color(0, 0, 0), 10)
            exit()

        except Exception:
            print("Any error occurs")


if __name__ == '__main__':
    run_clock()
