#
# Copyright (C) 2015 Satoru SATOH <ssato at redhat.com>
#
# .. note:: suppress some false-positive warnings
# pylint: disable=missing-docstring, no-self-use, invalid-name
from __future__ import absolute_import

import flask
import os.path
import os
import unittest

import fleure_webui.main.forms as TT
import tests.common


class TestForms(unittest.TestCase):

    def setUp(self):
        self.workdir = tests.common.setup_workdir()
        self.app = self.create_app()
        self.client = self.app.test_client()

    def tearDown(self):
        tests.common.cleanup_workdir(self.workdir)

    def create_app(self):
        app = flask.Flask(__name__)
        app.config["WTF_CSRF_ENABLED"] = False

        @app.route("/upload", methods=("POST", ))
        def upload():
            form = TT.UploadForm()
            if form.validate_on_submit():
                return "OK"
            return "NG"

        @app.route("/analyze", methods=("POST", ))
        def analyze():
            form = TT.AnalyzeForm()
            if form.validate_on_submit():
                return "OK"
            return "NG"

        return app

    def test_10_UploadForm__ok(self):
        filepath = os.path.join(self.workdir, "fake.zip")
        open(filepath, 'w').write("fake zip file")

        with open(filepath, 'rb') as fobj:
            postdata = dict(filename=fobj)
            resp = self.client.post("/upload", data=postdata)
            self.assertTrue(b"OK" in resp.data)

    def test_12_UploadForm__ng(self):
        filepath = os.path.abspath(__file__)
        with open(filepath, 'rb') as fobj:
            resp = self.client.post("/upload", data=dict(filename=fobj))

        self.assertTrue(b"NG" in resp.data)

    def test_20_AnalyzeForm__ok(self):
        """TODO: make test for AnalyzeForm working.
        """
        return
        postdata = dict(repos=["rhel-7-server-rpms"], keywords=["crash"],
                        core_rpms=["kernel"])
        resp = self.client.post("/analyze", data=postdata)
        self.assertTrue(b"OK" in resp.data)

# vim:sw=4:ts=4:et:
