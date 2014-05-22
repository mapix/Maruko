# -*- coding: utf-8 -*-

from functools import wraps
from datetime import datetime
from flask import jsonify
from flask.json import JSONEncoder


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return serialize_datatime(obj)
        except TypeError:
            pass
        return JSONEncoder.default(self, obj)


def jsonize(func):
    @wraps(func)
    def _(*args, **kwargs):
        result = func(*args, **kwargs)
        return jsonify(result)
    return _


def serialize_datatime(obj):
    return obj.strftime('%Y-%m-%d %H:%M:%S')
