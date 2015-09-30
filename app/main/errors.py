"""Error pages.
"""
from __future__ import absolute_import
from flask import render_template
from . import main


@main.app_errorhandler(404)
def page_not_found(err):
    """404 error page"""
    return render_template("error.html", error="404 Not Found"), 404


@main.app_errorhandler(500)
def internal_server_error(err):
    """500 error page"""
    return render_template("error.html",
                           error="500 Internal Server Error"), 500

# vim:sw=4:ts=4:et:
