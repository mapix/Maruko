# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import and_

from app import store
from app.libs.serialization import serialize_datatime


class Task(store.Model):

    __tablename__ = 'tasks'

    id = store.Column(store.Integer, primary_key=True, autoincrement=True)
    done = store.Column(store.Boolean, index=True, default=False)
    user_id = store.Column(store.Integer, store.ForeignKey('users.id'))
    song_id = store.Column(store.Integer, store.ForeignKey('songs.id'))
    create_time = store.Column(store.DateTime, default=datetime.now)
    update_time = store.Column(store.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return '%s(id=%s, user_id=%s)' % (self.__class__.__name__, self.id, self.user_id)

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
    def pick_one(cls, user):
        return cls.query.filter(and_(cls.user_id == user.id, not cls.done)).first()

    def mark_done(self):
        self.done = True
        store.session.add(self)
        store.session.commit()

    def to_dict(self, user=None):
        return {
            'id': str(self.id),
            'done': self.done,
            'user_id': str(self.user_id),
            'song_id': str(self.song_id),
            'create_time': serialize_datatime(self.create_time),
            'update_time': serialize_datatime(self.update_time),

            'user': self.user.to_dict(user),
            'song': self.song.to_dict(user),
        }
