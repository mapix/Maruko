# -*- coding: utf-8 -*-

from datetime import datetime
from gcm import GCM

from app import store
from app.config import GCM_API_KEY
from .registration import Registration

gcm = GCM(GCM_API_KEY)


class Message(store.Model):

    __tablename__ = 'messages'

    id = store.Column(store.Integer, primary_key=True, autoincrement=True)
    user_id = store.Column(store.Integer, store.ForeignKey('users.id'))
    flower_id = store.Column(store.Integer, store.ForeignKey('flowers.id'))
    create_time = store.Column(store.DateTime, default=datetime.now)

    def send(self, registration_ids):
        registration_ids = [registration.id for registration in self.user.registrations]
        if not registration_ids:
            return

        response = gcm.json_request(registration_ids=registration_ids, data=self.to_dict(self.user))

        for error, registration_ids in response.get('errors', {}).items():
            if error is not 'NotRegistered':
                continue
            for registration_id in registration_ids:
                registration = Registration.get(registration_id)
                if not registration:
                    continue
                registration.delete()

        for registration_id, canonical_id in response.get('canonical', {}).items():
            registration = Registration.get(registration_id)
            if not registration:
                continue
            registration.delete()
            Registration.add(self.user, canonical_id)
