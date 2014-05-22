# -*- coding: utf-8 -*-

from flask import g, request
from flask_restful import Resource

from app.libs.serialization import jsonize
from app.models.flower import Flower
from app.models.user import User
from .errors import ApiError, API_SUCCESS
from .utils import login_required


class FlowerResource(Resource):

    @login_required
    @jsonize
    def get(self, flower_id):
        user = g.user
        flower = Flower.get(flower_id)
        if not flower:
            ApiError.abort(ApiError.flower_not_exists)
        return flower.to_dict(user)

    @login_required
    @jsonize
    def post(self):
        user = g.user
        guardian_id = request.form.get('guardian_id', type=str)
        guardian = User.get(guardian_id)
        if not guardian:
            ApiError.abort(ApiError.user_not_exists)
        flower = Flower.add(user, guardian)
        return flower.to_dict(user)

    @login_required
    @jsonize
    def delete(self, flower_id):
        flower = Flower.get(flower_id)
        if flower:
            flower.delete()
        return API_SUCCESS
