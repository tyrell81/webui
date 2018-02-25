#!env/bin/python
# coding=utf-8
from flask import Flask
# from flask import Flask, render_template, url_for, request
app = Flask(__name__)
# app.config.from_object("config")

# модуль pvwtc в каталоге app
from app import pvwtc
#import pvwtc

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5001)