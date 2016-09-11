#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: models.py
Author: zlamberty
Created: 2016-08-20

Description:
    model definitions for coveyapp items (spec: tasks)

Usage:
    <usage>

"""

import binascii
import os

import eri.logging as logging

from flask import abort, url_for
from itsdangerous import (
    TimedJSONWebSignatureSerializer, BadSignature, SignatureExpired
)
from werkzeug.security import generate_password_hash, check_password_hash

from . import app, db
from .utils import timestamp


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

logger = logging.getLogger(__name__)
logging.configure()


# ----------------------------- #
#   model definitions           #
# ----------------------------- #

class User(db.Model):
    """the user model"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    createdAt = db.Column(db.Integer, default=timestamp)
    lastloginat = db.Column(db.Integer, default=timestamp, onupdate=timestamp)
    nickname = db.Column(db.String(32), nullable=False, unique=True)
    pwhash = db.Column(db.String(256), nullable=False)
    tasks = db.relationship('Task', lazy='dynamic', backref='user')

    def __init__(self, *args, **kwargs):
        self.authenticated = False
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return "<User {}>".format(self.nickname)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.pwhash = generate_password_hash(password)
        self.token = None

    def verify_password(self, password):
        return check_password_hash(self.pwhash, password)

    def generate_token(self, expiration=600):
        s = TimedJSONWebSignatureSerializer(
            app.config['SECRET_KEY'], expires_in=expiration
        )
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data['id'])
        return user

    @staticmethod
    def create(data):
        """create a new user"""
        user = User()
        user.from_dict(data, partialUpdate=False)
        return user

    def from_dict(self, data, partialUpdate=True):
        """import task data from a dictionary"""
        for (k, v) in data.items():
            try:
                setattr(self, k, v)
            except:
                if not partialUpdate:
                    abort(400)

    def to_dict(self):
        return {
            'id': self.id,
            'createdAt': self.createdAt,
            'lastloginat': self.lastloginat,
            'nickname': self.nickname,
            '_links': {
                'self': url_for('api.get_user', id=self.id),
                'tasks': url_for('api.get_tasks', userid=self.id),
                'tokens': url_for('api.new_token'),
            },
        }

    # flask-login integration
    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class Task(db.Model):
    """The task model"""
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    createdAt = db.Column(db.Integer, default=timestamp)
    updatedAt = db.Column(db.Integer, default=timestamp, onupdate=timestamp)
    title = db.Column(db.String(128), nullable=False)
    deadline = db.Column(db.DATETIME)
    notes = db.Column(db.String(1024))
    important = db.Column(db.Boolean, default=False)
    urgent = db.Column(db.Boolean, default=False)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Task "{}">'.format(self.title)

    @staticmethod
    def create(data):
        """create a new task object"""
        task = Task()
        task.from_dict(data, partialUpdate=False)
        return task

    def from_dict(self, data, partialUpdate=True):
        """import task data from a dictionary"""
        for (k, v) in data.items():
            try:
                setattr(self, k, v)
            except:
                if not partialUpdate:
                    abort(400)

    def to_dict(self):
        return {
            'id': self.id,
            'createdAt': self.createdAt,
            'updatedAt': self.updatedAt,
            'title': self.title,
            'deadline': self.deadline,
            'notes': self.notes,
            'important': self.important,
            'urgent': self.urgent,
            '_links': {
                'self': url_for('api.get_task', id=self.id),
            },
        }
