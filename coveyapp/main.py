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
from flask_login import current_user, login_user, logout_user, login_required

from . import db
from .auth import verify_password
from .forms import LoginForm, NewTaskForm, UpdateTaskForm
from .models import User, Task


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
    updatetaskform = UpdateTaskForm()
    return render_template(
        'index.html',
        loginform=loginform,
        newtaskform=newtaskform,
        updatetaskform=updatetaskform
    )


@main.route('/', methods=['POST'])
@login_required
def new_task():
    """serve client-side application"""
    newtaskform = NewTaskForm()

    if newtaskform.validate_on_submit():
        ntdict = newtaskform.data

        logger.info(ntdict)
        ntdict['userid'] = current_user.id
        ntdict['closed'] = None
        t = Task.create(ntdict)

        db.session.add(t)
        db.session.commit()

        logger.info(t.to_dict())
    else:
        logger.warning('invalid new task form!')
        logger.info(newtaskform.data)
        logger.info(newtaskform.errors)

    return redirect(url_for('.index'))


@main.route('/login', methods=["POST"])
def login():
    loginform = LoginForm()

    session['loginerror'] = None
    if loginform.validate_on_submit():
        if loginform.data['signin']:
            user = User.query.filter_by(nickname=loginform.data['nickname']).first()

            if user is None:
                session['loginerror'] = 'Invalid credentials. Try again or register new user'

            login_user(user)

        elif loginform.data['register']:
            # make new user
            user = User.create(loginform.data)

            db.session.add(user)
            db.session.commit()

            login_user(user)
    else:
        session['loginerror'] = loginform.errors

    return redirect(url_for('.index'))


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.index'))


@main.route('/task', methods=['POST'])
@login_required
def update_task():
    updatetaskform = UpdateTaskForm()
    logger.info(updatetaskform.data)
    if updatetaskform.validate_on_submit():
        tskdata = updatetaskform.data
        tsk = Task.query.get(tskdata['id'])
        tsk.from_dict(tskdata)
        db.session.add(tsk)
        db.session.commit()
    else:
        logger.warning('invalidated form! {}'.format(updatetaskform.errors))
        logger.info(updatetaskform.data)
        logger.info(updatetaskform.errors)

    return redirect(url_for('.index'))
