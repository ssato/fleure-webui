#
# -*- coding: utf-8 -*-
# Copyright (C) 2015 Satoru SATOH <ssato@redhat.com>
# License: MIT
#
# .. note:: suppress false-positive warnings around werkzeug
# pylint: disable=no-member
"""Fleure's Web UI
"""
from __future__ import absolute_import

import flask
import hashlib
import os.path
import os
import werkzeug
import uuid

from flask import render_template
from . import main
from .forms import UploadForm, AnalyzeForm, gen_hid

import fleure.main


def _gen_filepath(filename):
    """
    Generate relative file path from filename to avoid filename conflicts.
    """
    return os.path.join(gen_hid().split('-')[0], filename)


def _listify(objs):
    """
    Listify `objs` :: str

    >>> _listify("aaa bbb ccc")
    ['aaa', 'bbb', 'ccc']
    >>> _listify("aaa, bbb, ccc")
    ['aaa', 'bbb', 'ccc']
    >>> _listify("aaa, bbb, c c c")
    ['aaa', 'bbb', 'c c c']
    """
    return [s.strip() for s in objs.split(',' if ',' in objs else None)]


@main.route('/', methods=("GET", "POST"))
def upload():
    """Start page to upload files.
    """
    arcpath = flask.session.get("arcpath", None)
    if arcpath is not None:
        arcfile = os.path.basename(arcpath)
        flask.flash("Analysis finished: %s" % arcfile)

        resp = flask.make_response(open(arcpath, 'rb').read())
        resp.headers["Pragma"] = "public"
        resp.headers["Content-Encoding"] = "public"
        resp.headers["Content-Transfer-Encoding"] = "binary"
        resp.headers["Content-Type"] = "application/zip"
        resp.headers["Content-Disposition"] = \
            "attachement; filename=\"%s\";" % arcfile

        flask.session.clear()
        return resp

    form = UploadForm()
    if form.validate_on_submit():
        # ..note::
        #   filename must be renamed to some unique one to avoid collisions.
        filename = werkzeug.secure_filename(form.filename.data.filename)
        filepath = _gen_filepath(filename)

        uploaddir = flask.current_app.config["UPLOADDIR"]
        fileabspath = os.path.join(uploaddir, filepath)
        os.makedirs(os.path.dirname(fileabspath))
        form.filename.data.save(fileabspath)

        flask.session["filepath"] = filepath
        flask.session["hostid"] = form.hostid.data
        flask.flash("Uploaded: %s" % filename)

        return flask.redirect(flask.url_for(".analyze"))
    else:
        filename = None

    return render_template("upload.html", form=form, filename=filename,
                           arcpath=arcpath)


@main.route("/analyze", methods=("GET", "POST"))
def analyze():
    """Show basic info of uploaded file and start analysis.
    """
    filepath = flask.session.get("filepath", None)
    hostid = flask.session.get("hostid", None)
    if filepath is None or hostid is None:
        return flask.redirect(flask.url_for(".upload"))

    # Paranoid and unnecessary ? (CSRF issue)
    filename = werkzeug.secure_filename(os.path.basename(filepath))
    filepath = os.path.join(os.path.dirname(filepath), filename)

    # Convert to absolute path:
    uploaddir = flask.current_app.config["UPLOADDIR"]
    filepath = os.path.join(uploaddir, filepath)

    form = AnalyzeForm()
    # TBD: Set repos by selected dist dynamically.
    # form.repos.data.choices = [...]  # Select by dist.

    if form.validate_on_submit():
        workdir = os.path.join(flask.current_app.config["WORKDIR"],
                               os.path.dirname(filepath))

        _kwds = _listify(form.keywords.data)
        _rpms = _listify(form.core_rpms.data)

        cnf = dict(hid=hostid, workdir=workdir, repos=form.repos.data,
                   errata_keywords=_kwds, core_rpms=_rpms, archive=True)

        # .. note:: Analysis will take some time until its finish:
        arcpath = fleure.main.main(filepath, verbosity=2, **cnf)
        flask.session["arcpath"] = arcpath

        return flask.redirect(flask.url_for(".upload"))

    return render_template("analyze.html", form=form, filepath=filepath)


@main.route("/results")
def download_results():
    """Download analysis results.
    """
    arcpath = flask.session["arcpath"]
    if arcpath is None:
        return flask.redirect(flask.url_for(".analyze"))  # Or top?

    (arcdir, arcfile) = (os.path.dirname(arcpath), os.path.basename(arcpath))
    return flask.send_from_directory(arcdir, arcfile,
                                     mimetype="application/zip")

# vim:sw=4:ts=4:et:
