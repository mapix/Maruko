# -*- coding: utf-8 -*-

from json import loads, dumps  # NOQA
from functools import wraps
from datetime import datetime
from flask import jsonify
from flask.json import JSONEncoder


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
        except TypeError:
            pass
        return JSONEncoder.default(self, obj)


def jsonize(func):
    @wraps(func)
    def _(*args, **kwargs):
        result = func(*args, **kwargs)
        return jsonify(result)
    return _
