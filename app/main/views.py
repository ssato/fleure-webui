#
# -*- coding: utf-8 -*-
# Copyright (C) 2015 Satoru SATOH <ssato@redhat.com>
# License: MIT
#
"""Fleure's Web UI
"""
from __future__ import absolute_import

import flask
import os.path
import os
import werkzeug
import uuid

from flask import render_template
from . import main
from .forms import UploadForm, AnalysisInfoForm

import fleure.main


def gen_filepath(filename):
    """
    Generate relative file path from filename to avoid filename conflicts.
    """
    return os.path.join(str(uuid.uuid4()), filename)


@main.route('/', methods=("GET", "POST"))
def upload():
    """Start page to upload files.
    """
    form = UploadForm()
    if form.validate_on_submit():
        # ..note::
        #   filename must be renamed to some unique one to avoid collisions. 
        filename = werkzeug.secure_filename(form.filename.data.filename)
        filepath = gen_filepath(filename)
        fileabspath = os.path.join(flask.current_app.config["UPLOAD_FOLDER"],
                                   filepath)
        os.makedirs(os.path.dirname(fileabspath))
        form.filename.data.save(fileabspath)

        flask.flash("Uploaded: %s" % filename)
        return flask.redirect(flask.url_for("start_analysis",
                                            filepath=filepath))
    else:
        filename = None

    return render_template("upload.html", form=form, filename=filename)


@main.route("/analyze"):
def start_analysis():
    """Show basic info of uploaded file and start analysis.
    """
    filepath = flask.request.args.get("filepath", None)
    if filepath is None:
        return flask.redirect(flask.url_for('/'))

    # Paranoid and unnecessary ? (CSRF issue)
    filename = werkzeug.secure_filename(os.path.basename(filepath))
    filepath = os.path.join(os.path.dirname(filepath), filename)

    # Convert to absolute path:
    filepath = os.path.join(flask.current_app.config["UPLOAD_FOLDER"],
                            filepath)

    form = AnalysisInfoForm()
    # TBD: Set repos by selected dist dynamically.
    # form.repos.data.choices = [...]  # Select by dist.

    if form.validate_on_submit():
        workdir = os.path.join(flask.current_app.config["WORKDIR"],
                               os.path.dirname(filepath))

        cnf = dict(workdir=workdir, repos=form.repos.data,
                   errata_keywords=form.keywords.data.split(),
                   core_rpms=form.core_rpms.data.split())

        # .. note:: Analysis will take some time until its finish:
        arcpath = fleure.main.main(filepath, verbosity=2, **cnf)
        return flask.redirect(flask.url_for("analysis_result",
                                            arcpath=arcpath))

    return render_template("start_analysis.html", form=form, filepath=filepath)


@main.route("/results")
def analysis_result():
    """Download analysis results.
    """
    arcpath = flask.request.args.get("arcpath", None)
    if arcpath is None:
        return flask.redirect(flask.url_for("start_analysis"))  # Or top?

    (arcdir, arcfile) = (os.path.dirname(arcpath), os.path.basename(arcpath))
    return flask.send_from_directory(arcdir, arcfile)

# vim:sw=4:ts=4:et:
