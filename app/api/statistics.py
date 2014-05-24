# -*- coding: utf-8 -*-

from flask import g, request
from flask_restful import Resource

from app.libs.serialization import jsonize
from app.models.task import Task
from app.models.flower import Flower
from .errors import API_SUCCESS
from .utils import login_required


class StatisticsResource(Resource):

    @login_required
    @jsonize
    def post(self):
        user = g.user
        wetness = request.form.get('wetness', type=float)
        temperature = request.form.get('temperature', type=float)
        lightness = request.form.get('lightness', type=float)
        flower_id = request.form.get('flower_id', type=int)
        flower = Flower.get(flower_id)
        flower.process_statistics(wetness, temperature, lightness)
        task = Task.pick_one(user)
        if task:
            task.mark_done()
            return task.to_dict(user)
        return API_SUCCESS
