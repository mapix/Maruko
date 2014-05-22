# -*- coding: utf-8 -*-

from functools import wraps
from flask import g

from .errors import ApiError


def login_required(func):
    @wraps(func)
    def _(*args, **kwargs):
        user = g.get('user')
        if not user:
            ApiError.abort(ApiError.need_permission)
        return func(*args, **kwargs)
    return _
