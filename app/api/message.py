# -*- coding: utf-8 -*-

from flask import g
from flask_restful import Resource

from app.libs.serialization import jsonize
from app.models.message import Message
from .utils import login_required


class MessageResource(Resource):

    @login_required
    @jsonize
    def get(self):
        user = g.user
        messages = Message.query.filter(Message.user_id == user.id).all()
        return [message.to_dict(user) for message in messages]
