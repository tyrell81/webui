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
from flask_admin.base import MenuLink, Admin, BaseView, expose
from werkzeug.security import generate_password_hash, check_password_hash

from app import app
import pvwtc_forms as pvwtc_forms
import pvwtc_model as pvwtc_model


# Create Flask application
# app = Flask(__name__)
# app создается в __init__
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

# Define login form (for flask-login)
class LoginForm(form.Form):
    login = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        if not check_password_hash(user.password, self.password.data):
        # to compare plain text passwords use
        # if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):        
        # app.logger.debug("login: %s", self.login.data)
        return db.session.query(pvwtc_model.User).filter_by(login=self.login.data).first()


class PasswordForm(Form):
    old_password = PasswordField('Old password:', validators=[validators.required()])
    new_password = PasswordField('New password:', validators=[validators.required()])
    confirm_password = PasswordField('Confirm password:', validators=[validators.required()])


# Initialize flask-login
def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(pvwtc_model.User).get(user_id)


# Create customized model view class
class PvwtcModelView(sqla.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin.login_view'))


# Create customized index view class that handles login & registration
class PvwtcAdminIndexView(admin.AdminIndexView):
    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(PvwtcAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        link = ''
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(PvwtcAdminIndexView, self).index()

    @expose('/password/', methods=('GET', 'POST'))
    def password_view(self):
        form = PasswordForm(request.form)
        if request.method == 'POST':
            warn = ""

            old_password=request.form['old_password']
            new_password=request.form['new_password']
            confirm_password=request.form['confirm_password']

            user = db.session.query(pvwtc_model.User).filter_by(login="root").first()

            if new_password != confirm_password:
                warn = "Password not match"

            if not new_password or not confirm_password:
                warn = "Please fill all data"
            
            if not check_password_hash(user.password, old_password):
                warn = "Invalid old password"

            if warn:
                return self.render('password.html', form=form, warn = warn)

            user.password = generate_password_hash(new_password)
            db.session.commit()

            # Пароль изменен - логин заново
            login.logout_user()
            return redirect(url_for('.login_view'))

        # password.html
        return self.render('password.html', form=form)

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))

# Flask views
@app.route('/')
# @app.route('/index')
def index():
    # return render_template('index.html')    
    return redirect(url_for('admin.login_view'))

@app.route('/hello')
def hello():
	return "HELLO WORLD"

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Initialize flask-login
init_login()

# Create admin
admin = admin.Admin(app, 'PVWTC2', index_view=PvwtcAdminIndexView(), base_template='pvwtc_master.html')

# Add view
admin.add_view(pvwtc_forms.SettingsView(name='Settings', endpoint='settings'))
admin.add_view(PvwtcModelView(pvwtc_model.depositbox, db.session, category='Database'))
admin.add_view(PvwtcModelView(pvwtc_model.depositbox_user, db.session, category='Database'))
admin.add_view(PvwtcModelView(pvwtc_model.employee, db.session, category='Database'))
admin.add_view(PvwtcModelView(pvwtc_model.holiday, db.session, category='Database'))
admin.add_view(PvwtcModelView(pvwtc_model.image, db.session, category='Database'))
admin.add_view(PvwtcModelView(pvwtc_model.log, db.session, category='Database'))
admin.add_view(PvwtcModelView(pvwtc_model.log_image, db.session, category='Database'))
admin.add_view(PvwtcModelView(pvwtc_model.migration, db.session, category='Database'))
admin.add_view(PvwtcModelView(pvwtc_model.role, db.session, category='Database'))
admin.add_view(PvwtcModelView(pvwtc_model.schedule_day, db.session, category='Database'))
admin.add_view(PvwtcModelView(pvwtc_model.schedule, db.session, category='Database'))
admin.add_view(PvwtcModelView(pvwtc_model.templ, db.session, category='Database'))
admin.add_view(PvwtcModelView(pvwtc_model.templ_image, db.session, category='Database'))
admin.add_view(PvwtcModelView(pvwtc_model.work_model_branch, db.session, category='Database'))
admin.add_view(PvwtcModelView(pvwtc_model.User, db.session, category='Database'))




