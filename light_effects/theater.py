#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
any animation for 24-LEDs-strip
"""

import logger

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
    from neopixel import Color
    from light_effects import get_strip
    from light_effects.effects import color_wipe, theater_chase, theater_chase_rainbow, rainbow_cycle, rainbow

    strip = get_strip()
    global stop_flag
    stop_flag = False
    log.info('theater started, stop_flag = ' + str(stop_flag))
    for i in range(0, strip.numPixels(), 1):
        strip.setPixelColor(i, Color(0, 0, 0))

    while True:
        try:
            if stop_flag:
                break
            color_wipe(strip, Color(127, 0, 0))  # Green wipe
            # if stop_flag:
            #     break
            #rainbow_cycle(strip)
            if stop_flag:
                break
            color_wipe(strip, Color(0, 127, 0))  # Red wipe
            if stop_flag:
                break
            #rainbow(strip)
            # if stop_flag:
            #     break
            color_wipe(strip, Color(0, 0, 127))  # Blue wipe
            if stop_flag:
                break
            theater_chase(strip, Color(127, 127, 127))  # White theater chase
            if stop_flag:
                break
            #color_wipe(strip, Color(0, 0, 127))  # Blue wipe
            # if stop_flag:
            #     break
            #theater_chase(strip, Color(127, 0, 0))  # Green theater chase
            # if stop_flag:
            #     break
            #color_wipe(strip, Color(0, 127, 0))  # Red wipe
            # if stop_flag:
            #     break
            theater_chase(strip, Color(0, 0, 127))  # Blue theater chase
            if stop_flag:
                break
            # color_wipe(strip, Color(127, 0, 0))  # Green wipe
            # if stop_flag:
            #     break
            # theater_chase(strip, Color(80, 80, 80))  # White theater chase
            # if stop_flag:
            #     break
            # color_wipe(strip, Color(0, 0, 80))  # Blue wipe
            # if stop_flag:
            #     break
            theater_chase(strip, Color(80, 0, 0))  # Green theater chase
            if stop_flag:
                break
            # color_wipe(strip, Color(0, 80, 0))  # Red wipe
            # if stop_flag:
            #     break
            # theater_chase(strip, Color(0, 0, 80))  # Blue theater chase
            # if stop_flag:
            #     break
            # color_wipe(strip, Color(80, 0, 0))  # Green wipe
            # if stop_flag:
            #     break
            # #theater_chase_rainbow(strip)
            # if stop_flag:
            #     break

        except KeyboardInterrupt:
            log.warn("KeyboardInterrupt: {0}", exec_info=1)
            color_wipe(strip, Color(0, 0, 0), 10)
            exit()

        except Exception:
            log.error("Any error occurs: {0}", exec_info=1)

    log.info('theater run stopped')
    color_wipe(strip, Color(0, 0, 0), 10)
    log.debug('LED stripe cleared')
    return


if __name__ == '__main__':
    pass
