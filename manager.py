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
    from app.models.user_flower import UserFlower      # NOQA
    store.drop_all()
    store.create_all()
    print "Database recreate successfully !"

@manager.command
def serve_api():
    app.run()

@manager.command
def serve_censor():
    pass

if __name__ == '__main__':
    manager.run()
