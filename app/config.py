# coding=utf-8
# Конфиг приложения
import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SQLALCHEMY_TRACK_MODIFICATIONS = True
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'biosmart.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:////home/root/biosmart.db'
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_ECHO = True

# cross-site reference, и ключ для него
CSRF_ENABLED = True
SECRET_KEY = 'biosmart-secret-key'
WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = "biosmart-secret-key"
# SECRET_KEY используется для подписи cookies, при его изменении пользователям потребуется логиниться заново
# WTF_CSRF_ENABLED и WTF_CSRF_SECRET_KEY защищают от подмены POST-сообщений

THREADS_PER_PAGE = 8