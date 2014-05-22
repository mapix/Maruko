# -*- coding: utf-8 -*-

import os

DEBUG = True
APP_DIR = os.path.abspath(os.path.dirname(__file__))
VAR_DIR = os.path.join(os.path.dirname(APP_DIR), 'var')

if not os.path.exists(VAR_DIR):
    os.mkdir(VAR_DIR)

SECRET_KEY = os.environ.get('SECRET_KEY') or 'DEV SECRET KEY'
SQLALCHEMY_ECHO = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(VAR_DIR, 'data.sqlite')

GCM_PROXY = '10.8.0.1:8118'
GCM_PROXY = None
