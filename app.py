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


# Define login and registration forms (for flask-login)
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
        return db.session.query(User).filter_by(login=self.login.data).first()


class PasswordForm(Form):
    old_password = PasswordField('Old password:', validators=[validators.required()])
    new_password = PasswordField('New password:', validators=[validators.required()])
    confirm_password = PasswordField('Confirm password:', validators=[validators.required()])


# class RegistrationForm(form.Form):
#     login = fields.StringField(validators=[validators.required()])
#     email = fields.StringField()
#     password = fields.PasswordField(validators=[validators.required()])

#     def validate_login(self, field):
#         if db.session.query(User).filter_by(login=self.login.data).count() > 0:
#             raise validators.ValidationError('Duplicate username')


# Initialize flask-login
def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)


# Create customized model view class
class PvwtcModelView(sqla.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated


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
        link = '' #'<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(PvwtcAdminIndexView, self).index()

    # @expose('/register/', methods=('GET', 'POST'))
    # def register_view(self):
    #     form = RegistrationForm(request.form)
    #     if helpers.validate_form_on_submit(form):
    #         user = User()

    #         form.populate_obj(user)
    #         # we hash the users password to avoid saving it as plaintext in the db,
    #         # remove to use plain text:
    #         user.password = generate_password_hash(form.password.data)

    #         db.session.add(user)
    #         db.session.commit()

    #         login.login_user(user)
    #         return redirect(url_for('.index'))
    #     link = '' #'<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
    #     self._template_args['form'] = form
    #     self._template_args['link'] = link
    #     return super(PvwtcAdminIndexView, self).index()

    @expose('/password/', methods=('GET', 'POST'))
    def password_view(self):
        form = PasswordForm(request.form)
        if request.method == 'POST':
			warn = ""

			old_password=request.form['old_password']
			new_password=request.form['new_password']
			confirm_password=request.form['confirm_password']

			user = db.session.query(User).filter_by(login="root").first()

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

	# @expose('/password/', methods=('GET', 'POST'))
	# def password_view(self):
	# 	print 'DEBUG: PasswordView ==================================='
	# 	form = PasswordForm(request.form)
	# 	print form.errors
	# 	if request.method == 'POST':
	# 		print "POST"
	# 	# return self.render('password.html')
	# 	# return render_template('password.html', form=form)


# Password view
# class PasswordView(BaseView):
#     @expose('/', methods=('GET', 'POST'))
#     def index(self):
#         print 'DEBUG: PasswordView ==================================='
#         form = PasswordForm(request.form)
#         return render_template('password.html', form=form)


# Flask views
@app.route('/')
def index():
    # return render_template('index.html')
    return redirect(url_for('admin.login_view'))


# Initialize flask-login
init_login()

# Create admin
admin = admin.Admin(app, 'PVWTC2', index_view=PvwtcAdminIndexView(), base_template='pvwtc_master.html')

# Add view
admin.add_view(PvwtcModelView(User, db.session))
# admin.add_view(PasswordView(name='', endpoint='password')) # name='Password'



def build_biosmart_db():
    """
    Создание БД
    """
    import string
    import random

    # db.drop_all()
    db.create_all()
    # passwords are hashed, to use plaintext passwords instead:
    # test_user = User(login="test", password="test")
    default_user = User(login="root", password=generate_password_hash("bio0root"))
    if db.session.query(User).filter_by(login=default_user.login).count() == 0:        
        db.session.add(default_user)
        db.session.commit()
    return

if __name__ == '__main__':
    try:
        db.connect()
        db.execute("select * from user")
    except:
        build_biosmart_db()

    # Start app
    app.run(host='0.0.0.0', port=5001, debug=True)

# Запуск встроенного веб-сервера
# from app import app
#app.run(debug = True)


