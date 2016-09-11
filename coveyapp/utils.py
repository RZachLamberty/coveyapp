#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: utils.py
Author: zlamberty
Created: 2016-08-20

Description:
    utilities for the covey app

Usage:
    <usage>

"""

import argparse
import time

import eri.logging as logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

logger = logging.getLogger(__name__)
logging.configure()


# ----------------------------- #
#   utils funcs                 #
# ----------------------------- #

def log_config(app):
    """log all elements in a configuration dictionary"""
    logger.warning('application configuration')
    confkeys = sorted(app.config.keys())
    for k in confkeys:
        logger.debug("{}: {}".format(k, app.config[k]))


def timestamp():
    return int(time.time())
