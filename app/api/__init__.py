# -*- coding: utf-8 -*-

from flask import Blueprint, g, request

from app.models.user import User
from .urls import init_urls

api = Blueprint('api', __name__)
init_urls(api)


@api.before_request
def authenticate_user():
    authorization = request.headers.get('Authorization', '').split(':')
    if len(authorization) != 2:
        return
    _, user_id = authorization
    g.user = User.get(user_id)
