#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: main.py
Author: zlamberty
Created: 2016-08-20

nDescription:
    webpage routes

Usage:
    <usage>

"""

import datetime

import eri.logging as logging

from flask import (
    Blueprint, g, redirect, render_template, request, session, url_for
)
from flask_login import login_user, logout_user

from . import db
from .auth import verify_password
from .forms import LoginForm, NewTaskForm
from .models import User


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

logger = logging.getLogger(__name__)
logging.configure()


# ----------------------------- #
#   blueprint                   #
# ----------------------------- #

main = Blueprint('main', __name__)


# ----------------------------- #
#   main routes                 #
# ----------------------------- #

@main.route('/')
def index():
    """serve client-side application"""
    loginform = LoginForm()
    newtaskform = NewTaskForm()
    return render_template(
        'index.html',
        loginform=loginform,
        newtaskform=newtaskform
    )


@main.route('/login', methods=["POST"])
def login():
    loginform = LoginForm()

    if loginform.validate_on_submit():
        if loginform.data['signin']:
            user = User.query.filter_by(nickname=loginform.data['nickname']).first()

            if user is None:
                session['loginerror'] = 'Invalid credentials. Try again or register new user'
                return redirect(url_for('.index'))

            session['loginerror'] = None
            login_user(user)
            return redirect(url_for('.index'))

        elif loginform.data['register']:
            # make new user
            return "register"
    else:
        session['loginerror'] = loginform.errors
        return redirect(url_for('.index'))


@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('.index'))
