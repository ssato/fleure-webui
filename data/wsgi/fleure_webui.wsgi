#
# Copyright (C) 2015 Satoru SATOH <ssato@redhat.com>
# License: MIT
#
from __future__ import absolute_import

import os
import fleure_webui


_cnf = os.getenv("FLEURE_CONFIG") or "production"
application = fleure_webui.create_app(_cnf)

# vim:sw=4:ts=4:et:ft=python:
