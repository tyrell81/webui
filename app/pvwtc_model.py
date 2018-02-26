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
    password = db.Column(db.String())

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
        return self.login

# CREATE TABLE employee (id INTEGER PRIMARY KEY AUTOINCREMENT, id_schedule INTEGER DEFAULT 0, last_name TEXT, fisrt_name TEXT, middle_name TEXT, 
#    card INTEGER DEFAULT 0, pin INTEGER DEFAULT 0, type INTEGER DEFAULT 0, block INTEGER DEFAULT 0, was_local_changes INTEGER DEFAULT 0, role INTEGER NOT NULL DEFAULT 0)
class employee(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_schedule = db.Column(db.Integer, default=0)
    last_name = db.Column(db.String)
    fisrt_name = db.Column(db.String)
    middle_name = db.Column(db.String)
    card = db.Column(db.Integer)
    pin = db.Column(db.Integer)
    type = db.Column(db.Integer)
    block = db.Column(db.Integer)
    was_local_changes = db.Column(db.Integer)
    role = db.Column(db.Integer, nullable=False)

    depositbox_users = db.relationship('depositbox_user', backref='employee')
    images = db.relationship('image', backref='employee')
    templs = db.relationship('templ', backref='employee')
    templ_images = db.relationship('templ_image', backref='employee')

    def __unicode__(self):
        return self.last_name + ' ' + self.fisrt_name + ' ' + self.middle_name

# CREATE TABLE depositbox (box_id INTEGER PRIMARY KEY, human_number INTEGER NULL, mc_num INTEGER NOT NULL, cpf_num INTEGER NOT NULL, ch_num INTEGER NOT NULL, ident_type INTEGER NOT NULL)
class depositbox(db.Model):
    box_id = db.Column(db.Integer, primary_key=True)
    human_number = db.Column(db.Integer)
    mc_num = db.Column(db.Integer)
    cpf_num = db.Column(db.Integer)
    ch_num = db.Column(db.Integer)
    ident_type = db.Column(db.Integer)    

    depositbox_users = db.relationship('depositbox_user', backref='depositbox')

    def __unicode__(self):
        return str(self.human_number)

# CREATE TABLE depositbox_user (id INTEGER PRIMARY KEY AUTOINCREMENT, id_employee INTEGER NOT NULL, id_depositbox INTEGER NOT NULL, date_start INTEGER NOT NULL, date_finish INTEGER NOT NULL, openings_period INTEGER NOT NULL, openings_numbers INTEGER NOT NULL, open_time INTEGER NOT NULL, access_scenario INTEGER NOT NULL, access_role INTEGER NOT NULL, FOREIGN KEY(id_employee) REFERENCES employee(id) ON DELETE CASCADE, FOREIGN KEY(id_depositbox) REFERENCES depositbox(box_id) ON DELETE CASCADE)
class depositbox_user(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_employee = db.Column(db.Integer, db.ForeignKey('employee.id'))    
    box_id = db.Column(db.Integer, db.ForeignKey('depositbox.box_id'), name='id_depositbox')
    date_start = db.Column(db.Integer)
    date_finish = db.Column(db.Integer)
    openings_period = db.Column(db.Integer)
    openings_numbers = db.Column(db.Integer)
    open_time = db.Column(db.Integer)
    access_scenario = db.Column(db.Integer)
    access_role = db.Column(db.Integer)

    def __unicode__(self):
        return str(self.box_id)

# CREATE TABLE holiday (id INTEGER PRIMARY KEY AUTOINCREMENT, id_holiday_list INTEGER NOT NULL, date TEXT NOT NULL)
class holiday(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_holiday_list = db.Column(db.Integer)
    date = db.Column(db.String)

    def __unicode__(self):
        return str(self.id)

# CREATE TABLE image (id INTEGER PRIMARY KEY AUTOINCREMENT, id_employee INTEGER NOT NULL, img BLOB NOT NULL, FOREIGN KEY(id_employee) REFERENCES employee(id) ON DELETE CASCADE)
class image(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_employee = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    img = db.Column(db.LargeBinary, nullable=False)

    def __unicode__(self):
        return str(self.id)

#CREATE TABLE log (id INTEGER PRIMARY KEY AUTOINCREMENT, id_device INTEGER NOT NULL, id_employee INTEGER NOT NULL, event INTEGER NOT NULL, date TEXT NOT NULL, comment TEXT)        
class log(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_device = db.Column(db.Integer, nullable=False)
    id_employee = db.Column(db.Integer, nullable=False)
    event = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String, nullable=False)
    comment = db.Column(db.String)

    log_images = db.relationship('log_image', backref='log')

    def __unicode__(self):
        return str(self.id)

# CREATE TABLE log_image (id INTEGER PRIMARY KEY AUTOINCREMENT, id_log INTEGER NOT NULL, data BLOB NOT NULL, FOREIGN KEY(id_log) REFERENCES log(id) ON DELETE CASCADE)        
class log_image(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_log = db.Column(db.Integer, db.ForeignKey('log.id'), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)

    def __unicode__(self):
        return str(self.id)

# CREATE TABLE migration (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)        
class migration(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)

    def __unicode__(self):
        return str(self.id)

# CREATE TABLE role (id INTEGER PRIMARY KEY AUTOINCREMENT, studio_id INTEGER NOT NULL, password INTEGER DEFAULT 0, 
#   entry_menu INTEGER DEFAULT 0, entry_info INTEGER DEFAULT 0, entry_errors INTEGER DEFAULT 0, menu_settings INTEGER DEFAULT 0, 
#   sett_system INTEGER DEFAULT 0, sett_network INTEGER DEFAULT 0, sett_display INTEGER DEFAULT 0, sett_date_time INTEGER DEFAULT 0, sett_integration INTEGER DEFAULT 0, 
#   menu_users INTEGER DEFAULT 0, user_change INTEGER DEFAULT 0, user_add INTEGER DEFAULT 0, user_del INTEGER DEFAULT 0, 
#   user_change_palm INTEGER DEFAULT 0, user_change_code INTEGER DEFAULT 0, user_change_card INTEGER DEFAULT 0, user_change_name INTEGER DEFAULT 0)        
class role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    studio_id = db.Column(db.Integer, nullable=False)
    password = db.Column(db.Integer)
    entry_menu = db.Column(db.Integer)
    entry_info = db.Column(db.Integer)
    entry_errors = db.Column(db.Integer)
    menu_settings = db.Column(db.Integer)
    sett_system = db.Column(db.Integer)
    sett_network = db.Column(db.Integer)
    sett_display = db.Column(db.Integer)
    sett_date_time = db.Column(db.Integer)
    sett_integration = db.Column(db.Integer)
    menu_users = db.Column(db.Integer)
    user_change = db.Column(db.Integer)
    user_add = db.Column(db.Integer)
    user_del = db.Column(db.Integer)
    user_change_palm = db.Column(db.Integer)
    user_change_code = db.Column(db.Integer)
    user_change_card = db.Column(db.Integer)
    user_change_name = db.Column(db.Integer)

    def __unicode__(self):
        return str(self.id)

# CREATE TABLE schedule (id INTEGER PRIMARY KEY NOT NULL, id_holiday_list INTEGER DEFAULT 0, start TEXT NOT NULL, stop TEXT NOT NULL, days_count INTEGER NOT NULL)        
class schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_holiday_list = db.Column(db.Integer, nullable=False)
    start = db.Column(db.String, nullable=False)
    stop = db.Column(db.String, nullable=False)
    days_count = db.Column(db.Integer, nullable=False)

    schedule_days = db.relationship('schedule_day', backref='schedule')

    def __unicode__(self):
        return str(self.id)

# CREATE TABLE schedule_day (id INTEGER PRIMARY KEY AUTOINCREMENT, id_schedule INTEGER NOT NULL, day_number INTEGER NOT NULL, start TEXT NOT NULL, stop TEXT NOT NULL, FOREIGN KEY(id_schedule) REFERENCES schedule(id) ON DELETE CASCADE)
class schedule_day(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_schedule = db.Column(db.Integer, db.ForeignKey('schedule.id'), nullable=False)
    day_number = db.Column(db.Integer, nullable=False)
    start = db.Column(db.String, nullable=False)
    stop = db.Column(db.String, nullable=False)

    def __unicode__(self):
        return str(self.id)

# CREATE TABLE templ (id INTEGER PRIMARY KEY AUTOINCREMENT, id_employee INTEGER NOT NULL, type INTEGER NOT NULL, role INTEGER NOT NULL, ident_count INTEGER DEFAULT 0, 
#   size INTEGER NOT NULL, data BLOB NOT NULL, quality INTEGER NOT NULL DEFAULT 0, hand_kind INTEGER NOT NULL DEFAULT 0, FOREIGN KEY(id_employee) REFERENCES employee(id) ON DELETE CASCADE)
class templ(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_employee = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    type = db.Column(db.Integer, nullable=False)
    role = db.Column(db.Integer, nullable=False)
    ident_count = db.Column(db.Integer)
    size = db.Column(db.Integer, nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)
    quality = db.Column(db.Integer, nullable=False)
    hand_kind = db.Column(db.Integer, nullable=False)

    def __unicode__(self):
        return str(self.id)

# CREATE TABLE templ_image (id INTEGER PRIMARY KEY AUTOINCREMENT, id_employee INTEGER NOT NULL, data BLOB NOT NULL, 
#   id_template INTEGER DEFAULT (-1), FOREIGN KEY(id_employee) REFERENCES employee(id) ON DELETE CASCADE)
class templ_image(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_employee = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)
    id_template = db.Column(db.Integer)

    def __unicode__(self):
        return str(self.id)

# CREATE TABLE work_model_branch (id INTEGER PRIMARY KEY AUTOINCREMENT, js TEXT NOT NULL)
class work_model_branch(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    js = db.Column(db.String, nullable=False)

    def __unicode__(self):
        return str(self.id)

# Создание БД
def build_biosmart_db():
    import string
    import random

    print "DEBUG: build_biosmart_db()"
    # db.drop_all()
    db.create_all()
    # passwords are hashed, to use plaintext passwords instead:
    # test_user = User(login="test", password="test")    
    default_user = User(login="root", password=generate_password_hash("bio0root"))
    if db.session.query(User).filter_by(login=default_user.login).count() == 0:        
        db.session.add(default_user)
        db.session.commit()
    return

# START model
print "DEBUG: START model"

try:
    db.connect()
    db.execute("select * from user")
except:
    build_biosmart_db()