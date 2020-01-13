#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
simulation of advent calendar for 24-LEDs-strip
"""

import logger
from light_effects.led_strip import get_strip

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

log = logger.get_logger("Advent")
stop_flag = None

log.debug("Initialize LED strip.")
strip = get_strip()


def stop_advent():
    global stop_flag
    stop_flag = True
    log.debug('advent stop_flag was set to ' + str(stop_flag))
    return


def run_advent():
    # TODO: advent function
    global stop_flag
    stop_flag = False
    log.info('advent started, stop_flag = ' + str(stop_flag))
    return


if __name__ == '__main__':
    pass
