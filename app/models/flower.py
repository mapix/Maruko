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
        old_statisticses = self.statisticses.limit(3)
        new_statistics = Statistics.add(self, wetness, temperature, lightness)
        if not old_statisticses: return
        text = ""
        if new_statistics.wetness > old_statisticses[-1].wetness + 10:
            Message.add(self.guardian, self, '大石老师刚刚给你浇水了', MESSAGE_KIND.WATERING)
            Message.add(self.owner, self, '大石老师刚刚给你浇水了', MESSAGE_KIND.WATERING)
        elif new_statistics.wetness < 200:
            text = "好干燥，快来给我浇水！"
        # elif new_statistics.wetness > 700:
        #     text = "太湿"
        elif new_statistics.temperature < 10:
            text = "天气好冷！"
        elif new_statistics.temperature > 30:
            text = "天气好热！快点变凉快吧"
        elif new_statistics.lightness < 50:
            text = "见不到太阳啊主人~"
        elif new_statistics.lightness > 500:
            text = "今天已经晒够啦，快挪我到阴凉处"
        if text:
            Message.add(self.guardian, self, text, MESSAGE_KIND.MESSAGE)
            Message.add(self.owner, self, text, MESSAGE_KIND.MESSAGE)

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
