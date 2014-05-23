# -*- coding: utf-8 -*-

from datetime import datetime

from app import store
from app.libs.serialization import serialize_datatime
from .consts import MESSAGE_KIND
from .statistics import Statistics
from .message import Message


class Flower(store.Model):

    __tablename__ = 'flowers'

    id = store.Column(store.Integer, primary_key=True, autoincrement=True)
    owner_id = store.Column(store.Integer, store.ForeignKey('users.id'))
    guardian_id = store.Column(store.Integer, store.ForeignKey('users.id'))
    create_time = store.Column(store.DateTime, default=datetime.now)
    update_time = store.Column(store.DateTime, default=datetime.now, onupdate=datetime.now)

    statisticses = store.relationship(Statistics, lazy='dynamic', backref='flower', cascade='all, delete-orphan', order_by=Statistics.id.desc())
    messages = store.relationship(Message, lazy='dynamic', backref='flower', cascade='all, delete-orphan')

    def __repr__(self):
        return '%s(id=%s, owner_id=%s)' % (self.__class__.__name__, self.id, self.owner_id)

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
    def add(cls, owner, guardian):
        flower = cls(owner=owner, guardian=guardian)
        store.session.add(flower)
        store.session.commit()
        return flower

    @classmethod
    def get(cls, id):
        return cls.query.filter(cls.id == id).first()

    def process_statistics(self, wetness, temperature, lightness):
        old_statisticses = self.statisticses.limit(10)
        new_statistics = Statistics.add(self, wetness, temperature, lightness)

        if not old_statisticses:
            return

        if new_statistics.wetness > old_statisticses[-1].wetness:
            return Message.add(self.owner, self, '主银主银, %s给你浇水了' % self.guardian.name, MESSAGE_KIND.WATERING)

        messages = []
        if new_statistics.wetness < 200:
            messages.append("该浇水了")
        elif new_statistics.wetness > 700:
            messages.append("太潮湿")

        if new_statistics.lightness < 50:
            messages.append("太暗了")
        elif new_statistics.lightness > 500:
            messages.append("太亮了")

        if new_statistics.temperature < 10:
            messages.append("太冷了")
        elif new_statistics.temperature > 30:
            messages.append("太热了")

        if messages:
            Message.add(self.guardian, self, '主银主银, %s' % ', '.join(messages), MESSAGE_KIND.MESSAGE)

    def to_dict(self, user=None):
        return {
            'id': str(self.id),
            'owner_id': str(self.owner_id),
            'guardian_id': str(self.guardian_id),
            'create_time': serialize_datatime(self.create_time),
            'update_time': serialize_datatime(self.update_time),
            'owner': self.owner.to_dict(user),
            'guardian': self.guardian.to_dict(user),
        }
