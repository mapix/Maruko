# -*- coding: utf-8 -*-

from flask import Blueprint, g, request

from app.models.user import User
from .urls import init_urls

api = Blueprint('api', __name__)
init_urls(api)


@api.before_request
def authenticate_user():
    #request.headers['A']
    g.user = User.get(1)
