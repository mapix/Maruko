# -*- coding: utf-8 -*-

from flask import g, request
from flask_restful import Resource

from app.libs.serialization import jsonize
from app.models.registration import Registration
from .errors import API_SUCCESS
from .utils import login_required


class RegistrationResource(Resource):

    @login_required
    @jsonize
    def post(self):
        user = g.user
        registration_id = request.form.get('registration_id', type=str)
        Registration.online(user, registration_id)
        return API_SUCCESS

    @login_required
    @jsonize
    def delete(self):
        user = g.user
        Registration.offline(user)
        return API_SUCCESS
