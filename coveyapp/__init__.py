#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: __init__.py
Author: zlamberty
Created: 2016-08-20

Description:
    a covey four-quadrant todo webpage

Usage:
    <usage>

"""

import argparse
import os

import yaml

import eri.logging as logging

from flask import Flask, render_template, request, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

logger = logging.getLogger("coveyapp")
logging.configure()


# ----------------------------- #
#   flask extensions            #
# ----------------------------- #

db = SQLAlchemy()


# ----------------------------- #
#   app init                    #
# ----------------------------- #

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')


# ----------------------------- #
#   register blueprints         #
# ----------------------------- #

from .main import main as mainbp
app.register_blueprint(mainbp)

from .api import api as apibp
app.register_blueprint(apibp, url_prefix='/api')


# ----------------------------- #
#   initialize extensions       #
# ----------------------------- #

db.init_app(app)
Bootstrap(app)


# ----------------------------- #
#   custom flask commands       #
# ----------------------------- #

@app.cli.command()
def initdb():
    db.create_all()


# ----------------------------- #
#   Command line                #
# ----------------------------- #

def parse_args():
    """ Take a log file from the commmand line """
    parser = argparse.ArgumentParser()

    host = "host name"
    parser.add_argument("--host", help=host, default='0.0.0.0')

    port = "port number"
    parser.add_argument("-p", "--port", help=port, default=8000)

    args = parser.parse_args()

    return args


if __name__ == '__main__':

    args = parse_args()

    main()
