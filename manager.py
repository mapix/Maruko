#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.script import Manager

from app import app, store

manager = Manager(app)


@manager.command
def recreate_store():
    """ Create database. """
    from app.models.user import User                   # NOQA
    from app.models.flower import Flower               # NOQA
    from app.models.song import Song                   # NOQA
    from app.models.task import Task                   # NOQA
    from app.models.statistics import Statistics       # NOQA
    from app.models.message import Message             # NOQA
    from app.models.registration import Registration   # NOQA
    store.drop_all()
    store.create_all()
    print "Database recreate successfully !"


@manager.command
def prepare_models():
    from app.models.user import User
    from app.models.flower import Flower
    from app.models.song import Song

    user_owner = User.add('mapix.me@gmail.com', 'mapix', 'mapix')
    user_guardian = User.add('luoweifeng@douban.com', 'imapix', 'imapix')
    Flower.add(user_owner, user_guardian)
    Song.add('Hello,I Love You 2014', '小普')
    Song.add('欢迎你来大工厂demo', '邵小毛')
    Song.add('Dear Mama Remix', '马戏团小丑')
    Song.add('四月挽歌', '周云蓬')


@manager.command
def serve():
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    manager.run()
