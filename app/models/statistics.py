# -*- coding: utf-8 -*-

from datetime import datetime

from app import store
from app.libs.serialization import serialize_datatime
from .gcm_client import GCMClient


class Statistics(store.Model):

    __tablename__ = 'statistics'

    id = store.Column(store.Integer, primary_key=True, autoincrement=True)
    flower_id = store.Column(store.Integer, store.ForeignKey('flowers.id'))
    create_time = store.Column(store.DateTime, default=datetime.now)
    wetness = store.Column(store.Float, default=0.0)
    temperature = store.Column(store.Float, default=0.0)
    lightness = store.Column(store.Float, default=0.0)

    def __repr__(self):
        return '%s(id=%s, flower_id=%s)' % (self.__class__.__name__, self.id, self.flower_id)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.id

    def __cmp__(self, other):
        return cmp(self.id, other.id)

    def __bool__(self):
        return True

    __nonzero__ = __bool__

    @classmethod
    def add(cls, flower, wetness, temperature, lightness):
        statistics = cls(flower=flower, wetness=wetness, temperature=temperature, lightness=lightness)
        store.session.add(statistics)
        store.session.commit()
        GCMClient.send_statistics(flower, wetness, temperature, lightness)
        return statistics

    @classmethod
    def get(cls, id):
        return cls.query.filter(cls.id == id).first()

    def to_dict(self, user=None):
        return {
            'id': str(self.id),
            'flower_id': str(self.flower_id),
            'wetness': self.wetness,
            'temperature': self.temperature,
            'lightness': self.lightness,
            'flower': self.flower.to_dict(user),
            'create_time': serialize_datatime(self.create_time),
        }
