# -*- coding: utf-8 -*-

from datetime import datetime

from app import store
from app.libs.serialization import serialize_datatime


class Registration(store.Model):

    __tablename__ = 'registrations'

    id = store.Column(store.String(162), primary_key=True)
    active = store.Column(store.Boolean, default=True)
    user_id = store.Column(store.Integer, store.ForeignKey('users.id'))
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
    def get(cls, registration_id):
        return cls.query.filter(cls.id == registration_id).first()

    @classmethod
    def online(cls, user, registration_id):
        registration = cls.get(registration_id)
        if not registration:
            registration = cls(id=registration_id, user=user)
            store.session.add(registration)
            store.session.commit()
        elif registration.user != user:
            registration.user = user
            store.session.add(registration)
            store.session.commit()
        if not registration.active:
            registration.active = True
            store.session.add(registration)
            store.session.commit()
        return registration

    @classmethod
    def offline(cls, user):
        Registration.query.filter(cls.user_id == user.id).delete()
        store.session.commit()

    def delete(self):
        store.session.delete(self)
        store.session.commit()

    def to_dict(self, user=None):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'active': self.active,
            'create_time': serialize_datatime(self.create_time),
            'update_time': serialize_datatime(self.update_time),
            'user': self.user.to_dict(user),
        }
