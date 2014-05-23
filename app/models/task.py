# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import and_

from app import store


class Task(store.Model):

    __tablename__ = 'tasks'

    id = store.Column(store.Integer, primary_key=True, autoincrement=True)
    done = store.Column(store.Boolean, index=True, default=False)
    user_id = store.Column(store.Integer, store.ForeignKey('users.id'))
    action = store.Column(store.String(10))
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
    def add(cls, user, song, action):
        task = cls(user=user, song=song, action=action)
        cls.query.delete()
        store.session.add(task)
        store.session.commit()
        return task

    @classmethod
    def pick_one(cls, user):
        return cls.query.filter(and_(cls.user_id == user.id, not cls.done)).first()

    def mark_done(self):
        self.done = True
        store.session.add(self)
        store.session.commit()

    def to_dict(self, user=None):
        return {
            'object': 'song',
            'action': self.action,
            'song_id': self.song_id,
        }
