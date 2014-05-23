# -*- coding: utf-8 -*-

import sys
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy, event
from flask.ext.bootstrap import Bootstrap
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView


store = SQLAlchemy(session_options={'expire_on_commit': False})


def create_app():
    app = Flask(__name__)

    from . import config
    app.config.from_object(config)

    from .libs.serialization import CustomJSONEncoder
    app.json_encoder = CustomJSONEncoder

    bootstrap = Bootstrap()
    bootstrap.init_app(app)

    store.init_app(app)
    store.app = app
    store.session.expire_on_commit = False

    admin = Admin(app)

    from app.models.user import User                   # NOQA
    from app.models.flower import Flower               # NOQA
    from app.models.song import Song                   # NOQA
    from app.models.task import Task                   # NOQA
    from app.models.message import Message             # NOQA
    from app.models.registration import Registration   # NOQA
    from app.models.statistics import Statistics       # NOQA

    admin.add_view(ModelView(User, store.session))
    admin.add_view(ModelView(Flower, store.session))
    admin.add_view(ModelView(Song, store.session))
    admin.add_view(ModelView(Message, store.session))
    admin.add_view(ModelView(Task, store.session))
    admin.add_view(ModelView(Registration, store.session))
    admin.add_view(ModelView(Statistics, store.session))

    @event.listens_for(store.engine, "connect")
    def change_text_factory(connection, connection_record):
        connection.text_factory = str

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api")
    return app


reload(sys)
sys.setdefaultencoding('utf8')
app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
