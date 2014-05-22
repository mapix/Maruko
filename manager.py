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
    from app.models.message import Message             # NOQA
    from app.models.registration import Registration   # NOQA
    store.drop_all()
    store.create_all()
    print "Database recreate successfully !"

@manager.command
def serve():
    app.run()

if __name__ == '__main__':
    manager.run()
