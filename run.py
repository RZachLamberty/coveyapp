#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: run.py
Author: zlamberty
Created: 2016-08-20

Description:
    just run that ish

Usage:
    <usage>

"""

import argparse


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    import coveyapp
    import coveyapp.utils

    args = coveyapp.parse_args()
    coveyapp.utils.log_config(coveyapp.app)
    coveyapp.app.run(args.host, args.port)
