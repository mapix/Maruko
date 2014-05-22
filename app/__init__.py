# -*- coding: utf-8 -*-

import sys
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy, event
from flask.ext.bootstrap import Bootstrap

store = SQLAlchemy(session_options={'expire_on_commit': False})


def create_app():
    app = Flask(__name__)

    from . import config
    app.config.from_object(config)

    from .libs.json import CustomJSONEncoder
    app.json_encoder = CustomJSONEncoder

    bootstrap = Bootstrap()
    bootstrap.init_app(app)

    store.init_app(app)
    store.app = app
    store.session.expire_on_commit = False

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
    app.run()
