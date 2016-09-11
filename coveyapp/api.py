#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: api.py
Author: zlamberty
Created: 2016-08-20

Description:
    webpage routes

Usage:
    <usage>

"""

import eri.logging as logging

from flask import Blueprint, abort, g, jsonify, render_template, request, url_for

from . import db
from .auth import apiauth
from .models import User, Task
from .utils import timestamp


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

logger = logging.getLogger(__name__)
logging.configure()


# ----------------------------- #
#   blueprint                   #
# ----------------------------- #

api = Blueprint('api', __name__)


# ----------------------------- #
#   api routes                  #
# ----------------------------- #

@api.route('/')
def index():
    """serve client-side application"""
    return jsonify({'message': 'api endpoint'})


@api.route('/help')
@api.route('/docs')
@api.route('/doc')
def documentation():
    """blah"""
    return jsonify({'message': 'docs coming!'})


@api.route('/users', methods=['POST'])
def new_user():
    """create or edit a new user object"""
    user = User.create(request.get_json() or {})
    if User.query.filter_by(nickname=user.nickname).first() is not None:
        return (
            jsonify({'message': 'nickname {} is already taken'.format(user.nickname)}),
            403
        )
    db.session.add(user)
    db.session.commit()
    r = jsonify(user.to_dict())
    r.status_code = 201
    r.headers['Location'] = url_for('api.get_user', id=user.id)
    return r


def wrong_user_response(user):
    """wrapper for normalizing how we respond requests to resources restricted
    to certain users

    """
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    else:
        return (
            jsonify({'message': "You don't have permission to view this user"}),
            403
        )


@api.route('/users', methods=['GET'])
@apiauth.login_required
def get_user():
    """return a single users details as json (if authed as *that* user)"""
    return jsonify(g.current_user.to_dict())


@api.route('/users/', methods=['POST'])
@api.route('/users/<id>', methods=['POST'])
@apiauth.login_required
def edit_user(id=None):
    """edit an existing user (must be authenticated as that user)"""
    if id is None:
        user = g.current_user
    else:
        user = User.query.get(id)
        if user != g.current_user:
            return wrong_user_response(user)

    user.from_dict(request.get_json() or {})
    db.session.add(user)
    db.session.commit()
    return '', 204


@api.route('/tokens', methods=['POST'])
@apiauth.login_required
def new_token():
    """Request a user token."""
    token = g.current_user.generate_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@api.route('/tasks', methods=['POST'])
@apiauth.login_required
def new_task():
    """Post a new task."""
    d = request.get_json() or {}
    d['userid'] = g.current_user.id
    tsk = Task.create(d)
    db.session.add(tsk)
    db.session.commit()
    r = jsonify(tsk.to_dict())
    r.status_code = 201
    r.headers['Location'] = url_for('api.get_task', id=tsk.id)
    return r


@api.route('/tasks', methods=['GET'])
@apiauth.login_required
def get_tasks():
    """Return list of tasks."""
    return jsonify({'tasks': [tsk.to_dict() for tsk in g.current_user.tasks]})


@api.route('/tasks/<id>', methods=['GET'])
@apiauth.login_required
def get_task(id):
    """Return a task."""
    tsk = Task.query.get(id)

    u = tsk.user
    if u != g.current_user:
        return wrong_user_response(u)

    return jsonify(tsk.to_dict())


@api.route('/tasks/<id>', methods=['POST'])
@apiauth.login_required
def edit_task(id):
    """Modify an existing task."""
    tsk = Task.query.get(id)
    if tsk is None:
        return jsonify({'message': 'task id {} not found'.format(id)}), 400

    u = tsk.user
    if u != g.current_user:
        return wrong_user_response(u)

    tsk.from_dict(request.get_json() or {})
    db.session.add(tsk)
    db.session.commit()
    return '', 204
