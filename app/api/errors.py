# -*- coding: utf-8 -*-

from flask_restful import abort as _abort

API_SUCCESS = {'code': '11000', 'message': 'success', 'status': 200}


class ApiError(object):

    forbidden = (11004, 'forbidden', 403)
    need_permission = (11005, 'need_permission', 403)

    user_not_exists = (11006, 'user_not_exists', 404)
    flower_not_exists = (11007, 'flower_not_exists', 404)
    song_not_exists = (11008, 'song_not_exists', 404)

    @classmethod
    def abort(cls, error, **kwargs):
        code, message, status = error
        _abort(status, status=status, code=code, message=message, **kwargs)
