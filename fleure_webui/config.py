#
# Copyright (C) 2015 Satoru SATOH <ssato@redhat.com>
# License: MIT
#
"""Fleure's Web UI: Default Config
"""
from __future__ import absolute_import

import os
import uuid


class Config(object):
    """Default configuration
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or str(uuid.uuid4())
    WTF_CSRF_ENABLED = True

    _pkgcachedir = "/var/cache/fleure_webui"
    UPLOADDIR = os.environ.get("FLEURE_UPLOADDIR", _pkgcachedir + "uploads")
    WORKDIR = os.environ.get("FLEURE_WORKDIR", _pkgcachedir + "workdir")

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
