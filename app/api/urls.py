# -*- coding: utf-8 -*-

from flask_restful import Api

from .flower import FlowerResource
from .song import SongResource
from .user import UserResource
from .message import MessageResource
from .statistics import StatisticsResource
from .registration import RegistrationResource


RESOURCE_URLS = [
    (UserResource,   '/users/<int:user_id>', 'user'),
    (FlowerResource, '/flowers', 'flowers'),
    (FlowerResource, '/flowers/<int:flower_id>', 'flower'),
    (SongResource,   '/songs', 'songs'),
    (SongResource,   '/songs/<int:song_id>', 'song'),
    (MessageResource, '/messages', 'messages'),
    (StatisticsResource, '/statistics', 'statistics'),
    (RegistrationResource, '/registrations', 'registrations'),
]


def init_urls(api):
    api_manager = Api(api)
    for resource, url, endpoint in RESOURCE_URLS:
        api_manager.add_resource(resource, url, endpoint=endpoint)
