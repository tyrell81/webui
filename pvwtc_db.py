#!env/bin/python
# coding=utf-8
import os
from flask import Flask, url_for, redirect, render_template, request, Response
from flask_sqlalchemy import SQLAlchemy
from wtforms import form, fields, validators,  Form, TextField, TextAreaField, PasswordField, StringField, SubmitField, BooleanField
from wtforms.validators import Required, DataRequired
import flask_admin as admin
import flask_login as login
from flask_admin.contrib import sqla
from flask_admin import helpers, expose, BaseView
from werkzeug.security import generate_password_hash, check_password_hash


# Create Flask application
app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

# Create user model.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(64))

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username

class employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_schedule = db.Column(db.Integer)
    last_name = db.Column(db.String)
    fisrt_name = db.Column(db.String)
    middle_name = db.Column(db.String)
    card = db.Column(db.Integer)
    pin = db.Column(db.Integer)
    type = db.Column(db.Integer)
    block = db.Column(db.Integer)
    was_local_changes = db.Column(db.Integer)

    def __unicode__(self):
        return self.username
