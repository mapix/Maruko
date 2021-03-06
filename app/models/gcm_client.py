# -*- coding: utf-8 -*-

from gcm import GCM as _GCM

from app.config import GCM_PROXY
from .consts import GCM_API_KEY, MESSAGE_TYPE
from .registration import Registration


class GCMClient(object):

    client = _GCM(GCM_API_KEY, proxy=GCM_PROXY)

    @classmethod
    def send_message(cls, message):
        registration_ids = [registration.id for registration in message.user.registrations]
        cls._send(MESSAGE_TYPE.MESSAGE, registration_ids, message.to_dict(message.user))

    @classmethod
    def send_statistics(cls, flower, wetness, temperature, lightness):
        data = {
            'wetness': wetness,
            'temperature': temperature,
            'lightness': lightness,
        }
        data['flower'] = flower.to_dict(flower.owner)
        registration_ids = [registration.id for registration in flower.owner.registrations]
        if registration_ids:
            cls._send(MESSAGE_TYPE.STATISTIC, registration_ids, data)

        data['flower'] = flower.to_dict(flower.guardian)
        registration_ids = [registration.id for registration in flower.guardian.registrations]
        if registration_ids:
            cls._send(MESSAGE_TYPE.STATISTIC, registration_ids, data)

    @classmethod
    def _send(cls, message_type, registration_ids, data):
        if not registration_ids:
            return
        gcm_payload = {
            'type': message_type,
            'payload': data,
        }
        response = cls.client.json_request(registration_ids=registration_ids, data=gcm_payload)

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
            user = registration.user
            registration.delete()
            Registration.online(user, canonical_id)
