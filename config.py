#
# Copyright (C) 2015 Satoru SATOH <ssato@redhat.com>
# License: MIT
#
"""Fleure's Web UI: Default Config
"""
from __future__ import absolute_import

import os
import uuid


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Default configuration
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or str(uuid.uuid4())

    FLEURE_UPLOAD_FOLDER = "/tmp/uploads"
    FLEURE_WORKDIR = "/tmp/uploads"

    @staticmethod
    def init_app(app):
        """Initialize application.
        """
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


CNF = dict(development=DevelopmentConfig,
           testing=TestingConfig,
           production=ProductionConfig,
           default=DevelopmentConfig)

# vim:sw=4:ts=4:et:
