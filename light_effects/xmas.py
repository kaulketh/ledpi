#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
christmas animation for 24-LEDs-strip
"""

import logger

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

from light_effects.led_strip import get_strip

log = logger.get_logger("Xmas")
stop_flag = None
strip = get_strip()


def stop_xmas():
    global stop_flag
    stop_flag = True
    log.debug('xmas stop_flag was set to ' + str(stop_flag))
    return


def run_xmas():
    # TODO: xmas function
    global stop_flag
    stop_flag = False
    log.info('xmas started, stop_flag = ' + str(stop_flag))
    return


if __name__ == '__main__':
    pass
