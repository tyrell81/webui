#!env/bin/python
# coding=utf-8

# Запуск встроенного веб-сервера
from app import app
app.run(host='0.0.0.0', port=5001, debug=True)

