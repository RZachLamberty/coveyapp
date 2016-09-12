#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: forms.py
Author: zlamberty
Created: 2016-09-04

Description:
    wtf form management ftw

Usage:
    <usage>

"""

import eri.logging as logging

from flask_wtf import Form
from wtforms import BooleanField, IntegerField, PasswordField, StringField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Optional


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

logger = logging.getLogger(__name__)
logging.configure()


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

class LoginForm(Form):
    nickname = StringField('Nickname', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    rememberMe = BooleanField('Remember Me', default=False)
    signin = SubmitField('Sign In')
    register = SubmitField('Register')


class NewTaskForm(Form):
    title = StringField('Title', validators=[DataRequired(), Length(max=128)])
    deadline = DateField('Deadline', format='%Y-%m-%d', validators=[Optional()])
    notes = StringField('Notes', validators=[Length(max=1024)])
    important = BooleanField('Important', default=False)
    urgent = BooleanField('Urgent', default=False)
    submit = SubmitField('Do it to it!')


class UpdateTaskForm(Form):
    id = IntegerField('id', validators=[DataRequired()])
    deadline = DateField('Deadline', format='%Y-%m-%d', validators=[Optional()])
    notes = StringField('Notes', validators=[Length(max=1024)])
    important = BooleanField('Important', default=False)
    urgent = BooleanField('Urgent', default=False)
    submit = SubmitField('Update task')
    closed = SubmitField('Close')
