# -*- coding: utf-8 -*-

from flask import g
from flask_restful import Resource

from app.libs.serialization import jsonize
from app.models.user import User
from .errors import ApiError
from .utils import login_required


class UserResource(Resource):

    @jsonize
    @login_required
    def get(self, user_id):
        visitor = g.user
        user = User.get(user_id)
        if not user:
            ApiError.abort(ApiError.user_not_exists)
        return user.to_dict(visitor)
