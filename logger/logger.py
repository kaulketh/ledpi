#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
logger.py
logging tool
"""
import os

import logging

from logging.config import fileConfig

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

this_folder = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(this_folder, 'logger.ini')
fileConfig(config_file)


def get_logger(name=None):
    if name is None:
        name = __name__
    logger = logging.getLogger(name[0:15])
    return logger


if __name__ == '__main__':
    pass
