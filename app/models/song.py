# -*- coding: utf-8 -*-

from datetime import datetime

from app import store


class Song(store.Model):

    __tablename__ = 'songs'

    id = store.Column(store.Integer, primary_key=True, autoincrement=True)
    title = store.Column(store.String(64), nullable=False)
    artist = store.Column(store.String(64))
    play_count = store.Column(store.Integer, default=0)
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
    def add(cls, owner, guardian):
        flower = cls(owner=owner, guardian=guardian)
        store.session.add(flower)
        store.session.commit()
        return flower

    def play(self):
        pass

    @classmethod
    def get(cls, id):
        return cls.query.filter(cls.id == id).first()

    def to_dict(self, user=None):
        return {
            'id': str(self.id),
            'title': self.title,
            'artist': self.artist,
            'play_count': self.play_count,
            'create_time': self.create_time,
            'update_time': self.update_time,
        }
