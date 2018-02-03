#!env/bin/python
# coding=utf-8
import os
from flask import Flask, url_for, redirect, render_template, request, Response
from flask_sqlalchemy import SQLAlchemy
from wtforms import fields, validators,  Form, TextField, TextAreaField, PasswordField, StringField, SubmitField, BooleanField
from wtforms.validators import Required, DataRequired
from flask_admin.contrib import sqla
from flask_admin import helpers, expose, BaseView
import flask_admin as admin
import flask_login as login
import pvwtc_db as pvwtc_db


# Create Flask application
app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

class SettingsForm(Form):
	# Заполнение значений полей формы
	value_setting_one = "value_setting_one"
	value_setting_two = "value_setting_two"
	# Определение полей формы
	setting_one = StringField('Setting one: *', validators = [Required()], default = value_setting_one)
	setting_two = StringField('Setting two:', default = value_setting_two)

class SettingsView(BaseView):
	@expose('/', methods=('GET', 'POST'))
	def settings_view(self):
		form = SettingsForm(request.form)
		if request.method == 'POST':
			# Проверка заполнения полей - параметр validators в определении полей в SettingsForm
			if not helpers.validate_form_on_submit(form):
				helpers.flash_errors(form, "Please fill fields with *")
				return self.render('settings.html', form=form)

			# Сообщение на форме после всех полей
			message = ""

			# Значения полей
			setting_one = request.form['setting_one']
			setting_two = request.form['setting_two']

			# Проверка значений
			if len(setting_one) > 5:
				helpers.flash("Setting one value too long: " + str(len(setting_one)) + ". Only 5 allowed")
				return self.render('settings.html', form=form)

			# Сохранение значений
			# TODO: place your code there

			# Значения проверены - сообщение ок
			if not message:
				message = "Settings saved"

			# Готово
			return self.render('settings.html', form=form, message = message)
		# /POST

		# рендер формы
		return self.render('settings.html', form=form)

	# Проверка залогиненного пользователя
	def is_accessible(self):
		return login.current_user.is_authenticated

	# Неаутентифицированный пользователь перенаправляется на страницу логина
	def inaccessible_callback(self, name, **kwargs):
		return redirect(url_for('admin.login_view'))

