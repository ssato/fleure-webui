#
# Copyright (C) 2015 Satoru SATOH <ssato@redhat.com>
# License: MIT
#
"""Fleure's Web UI
"""
from __future__ import absolute_import
import flask

main = flask.Blueprint("main", __name__)

from . import views, errors

# vim:sw=4:ts=4:et:
