#!/usr/bin/env python
# -*- coding: utf-8 -*-


def load_user_ns():
    from app import app, store                     # NOQA

    app.app_context().push()

    from app.models.user import User               # NOQA
    from app.models.question import Question       # NOQA

    return locals()


def start_shell():
    try:
        from IPython import start_ipython
        start_ipython(argv=[], user_ns=load_user_ns())
    except ImportError:
        print "Install IPython to get it works."
    else:
        print "Interactive shell exit successfully."


if __name__ == '__main__':
    start_shell()
