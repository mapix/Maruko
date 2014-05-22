# -*- coding: utf-8 -*-

import hashlib
from datetime import datetime
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash

from app import store
from app.libs.serialization import serialize_datatime
from .flower import Flower
from .registration import Registration
from .message import Message


class User(store.Model):

    __tablename__ = 'users'

    id = store.Column(store.Integer, primary_key=True, autoincrement=True)
    name = store.Column(store.String(20), nullable=False)
    email = store.Column(store.String(20), nullable=False)
    avatar_hash = store.Column(store.String(32))
    password_hash = store.Column(store.String(128))
    create_time = store.Column(store.DateTime, default=datetime.now)
    update_time = store.Column(store.DateTime, default=datetime.now, onupdate=datetime.now)

    messages = store.relationship(Message, lazy='dynamic', backref='user', cascade='all, delete-orphan')
    registrations = store.relationship(Registration, lazy='dynamic', backref='user', cascade='all, delete-orphan')
    owned_flowers = store.relationship(Flower, foreign_keys=[Flower.owner_id], lazy='dynamic', backref='owner', cascade='all, delete-orphan')
    guardianed_flowers = store.relationship(Flower, foreign_keys=[Flower.guardian_id], lazy='dynamic', backref='guardian', cascade='all, delete-orphan')

    def __repr__(self):
        return '%s(id=%s, name=%s)' % (self.__class__.__name__, self.id, self.name)

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
    def add(cls, email, name, password):
        user = cls(email=email, name=name, avatar_hash=hashlib.md5(email).hexdigest(),
                   password_hash=generate_password_hash(password))
        store.session.add(user)
        store.session.commit()
        return user

    @classmethod
    def get(cls, id):
        return cls.query.filter(cls.id == id).first()

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size=100, default='identicon', rating='g'):
        url = 'https://secure.gravatar.com/avatar' if request.is_secure else 'http://www.gravatar.com/avatar'
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url, hash=self.avatar_hash, size=size, default=default, rating=rating)

    def to_dict(self, user=None):
        return {
            'id': str(self.id),
            'name': self.name,
            'email': self.email,
            'avatar': self.avatar(),
            'create_time': serialize_datatime(self.create_time),
            'update_time': serialize_datatime(self.update_time),
        }
