# -*- coding: utf-8 -*-

from flask import g, request
from flask_restful import Resource

from app.libs.serialization import jsonize
from app.models.task import Task
from app.models.flower import Flower
from .errors import API_SUCCESS
from .utils import login_required


class StatisticResource(Resource):

    @login_required
    @jsonize
    def post(self, song_id):
        user = g.user
        wetness = request.form.get('wetness', type=int)
        temperature = request.form.get('temperature', type=int)
        lightness = request.form.get('lightness', type=int)
        flower_id = request.form.get('flower_id', type=int)
        flower = Flower.get(flower_id)
        flower.process_statistic(wetness, temperature, lightness)
        task = Task.pick_one(user)
        if task:
            task.mark_done()
            return task.to_dict(user)
        return API_SUCCESS