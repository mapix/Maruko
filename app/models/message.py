# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from app import store
from app.libs.serialization import serialize_datatime
from .gcm_client import GCMClient


class Message(store.Model):

    __tablename__ = 'messages'

    id = store.Column(store.Integer, primary_key=True, autoincrement=True)
    user_id = store.Column(store.Integer, store.ForeignKey('users.id'))
    flower_id = store.Column(store.Integer, store.ForeignKey('flowers.id'))
    type = store.Column(store.String(10))
    text = store.Column(store.String(40))
    create_time = store.Column(store.DateTime, default=datetime.now)

    @classmethod
    def add(cls, user, flower, text, type):
        message = cls(user=user, flower=flower, text=text, type=type)
        store.session.add(message)
        timestamp = datetime.now() - timedelta(seconds=10)
        cls.query.filter(cls.create_time < timestamp).delete()
        store.session.commit()
        GCMClient.send_message(message)
        return message

    @classmethod
    def get(cls, id):
        return cls.query.filter(cls.id == id).first()

    def to_dict(self, user=None):
        return {
            'id': str(self.id),
            'user_id': self.user_id,
            'flower_id': self.flower_id,
            'type': self.type,
            'text': self.text,
            'create_time': serialize_datatime(self.create_time),

            'flower': self.flower.to_dict(user),
            'user': self.user.to_dict(user),
        }
