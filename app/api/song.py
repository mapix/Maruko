# -*- coding: utf-8 -*-

from flask import g
from flask_restful import Resource

from app.libs.serialization import jsonize
from app.models.song import Song
from .errors import ApiError, API_SUCCESS
from .utils import login_required


class SongResource(Resource):

    @login_required
    @jsonize
    def get(self, question_id):
        user = g.user
        songs = Song.query.all()
        return {song.to_dict(user) for song in songs}

    @login_required
    @jsonize
    def post(self, song_id):
        user = g.user
        song = Song.get(song_id)
        if not song:
            ApiError.abort(ApiError.song_not_exists)
        song.play(user)
        return API_SUCCESS

    @login_required
    @jsonize
    def delete(self, song_id):
        user = g.user
        song = Song.get(song_id)
        if not song:
            ApiError.abort(ApiError.song_not_exists)
        song.stop(user)
        return API_SUCCESS
