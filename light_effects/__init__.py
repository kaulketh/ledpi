#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
light_effects/__init__py
"""
from led_strip import get_strip
from light_effects.advent import stop_advent
from light_effects.candles import stop_candles
from light_effects.effects import clear
from light_effects.theater import stop_theater
from light_effects.clock import stop_clock
from light_effects.clock2 import stop_clock2
from light_effects.led_strip import get_strip
from light_effects.circus import stop_circus

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"


def stop_light_effects():
    if stop_clock():
        if stop_clock2():
            if stop_theater():
                if stop_advent():
                    if stop_circus():
                        if stop_candles():
                            return clear(get_strip())
