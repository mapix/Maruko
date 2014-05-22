# -*- coding: utf-8 -*-

from datetime import datetime

from app import store


class Flower(store.Model):

    __tablename__ = 'flowers'

    id = store.Column(store.Integer, primary_key=True, autoincrement=True)
    owner_id = store.Column(store.Integer, store.ForeignKey('users.id'))
    guardian_id = store.Column(store.Integer, store.ForeignKey('users.id'))
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

    @classmethod
    def get(cls, id):
        return cls.query.filter(cls.id == id).first()

    def to_dict(self, user=None):
        return {
            'id': str(self.id),
            'owner_id': str(self.owner_id),
            'guardian_id': str(self.guardian_id),
            'create_time': self.create_time,
            'update_time': self.update_time,
            'owner': self.owner.to_dict(user),
            'guardian': self.guardian.to_dict(user),
        }

