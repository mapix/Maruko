# -*- coding: utf-8 -*-

from gcm import GCM

from app.config import GCM_API_KEY

gcm = GCM(GCM_API_KEY)


def send_message(registration_ids, data):
    response = gcm.json_request(registration_ids=registration_ids, data=data)
    hander_response_errors(response)


def hander_response_errors(response):
    if 'errors' in response:
        for error, reg_ids in response['errors'].items():
            if error is 'NotRegistered':
                for reg_id in reg_ids:
                    entity.filter(registration_id=reg_id).delete()
    if 'canonical' in response:
        for reg_id, canonical_id in response['canonical'].items():
            entry = entity.filter(registration_id=reg_id)
            entry.registration_id = canonical_id
            entry.save()
