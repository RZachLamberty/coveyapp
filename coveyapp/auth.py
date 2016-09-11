#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: auth.py
Author: zlamberty
Created: 2016-08-21

Description:
    authentication for users of the covey todo app

Usage:
    <usage>

"""

import eri.logging as logging

from flask import jsonify, session, g
from flask_httpauth import HTTPBasicAuth
from flask_login import LoginManager

from . import app, db
from .models import User


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

logger = logging.getLogger(__name__)
logging.configure()


# ----------------------------- #
#   api auth setup              #
# ----------------------------- #

apiauth = HTTPBasicAuth()


@apiauth.verify_password
def verify_password(nicknameOrToken, password):
    """Password verification callback."""
    # try token auth first (will be None if expired or invalid token)
    user = User.verify_auth_token(nicknameOrToken)

    if not user:
        # nickname / pw auth
        user = User.query.filter_by(nickname=nicknameOrToken).first()
        if user is None or not user.verify_password(password):
            return False

    # remember -- g is in the request context so this has to be set every time
    g.current_user = user

    # to record "updated at" (i.e. last login) stats
    db.session.add(user)
    db.session.commit()

    return True


@apiauth.error_handler
def password_error():
    """Return a 401 error to the client."""
    # To avoid login prompts in the browser, use the "Bearer" realm.
    return (
        jsonify({'error': 'authentication required'}),
        401,
        {'WWW-Authenticate': 'Bearer realm="Authentication Required"'}
    )


# ----------------------------- #
#   webpage auth setup          #
# ----------------------------- #

mainauth = LoginManager()
mainauth.init_app(app)


@mainauth.user_loader
def user_loader(userid):
    return User.query.get(userid)


@mainauth.request_loader
def request_loader(request):
    pass
