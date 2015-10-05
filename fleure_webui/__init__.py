#
# Copyright (C) 2015 Satoru SATOH <ssato@redhat.com>
# License: MIT
#
from __future__ import absolute_import

import flask
import flask.ext.bootstrap
import flask.ext.wtf.csrf

from .config import CNF


def create_app(cnf_name="development"):
    """
    :param cnf_name: Config name, e.g. "development"
    """
    cnf = CNF[cnf_name]

    app = flask.Flask(__name__)
    app.config.from_object(cnf)
    cnf.init_app(app)

    bootstrap = flask.ext.bootstrap.Bootstrap()
    bootstrap.init_app(app)

    csrf = flask.ext.wtf.csrf.CsrfProtect()
    csrf.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

# vim:sw=4:ts=4:et:
