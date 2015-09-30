"""HTML Forms.

License: BSD as the part of this code is derived from flask.wtf.

References:
  - Flask-flask_wtf: https://flask-wtf.readthedocs.org
  - wtforms: http://wtforms.simplecodes.com/docs/0.6.1/validators.html
"""
from __future__ import absolute_import

import flask_wtf.file
import flask_wtf
import wtforms.validators as WV
import wtforms

import fleure.globals


class FileAllowedEx(flask_wtf.file.FileAllowed):
    """
    A little bit modified version of flask_wtf.FileAllowed to allow complex
    file extensions such as .tar.xz, .tar.gz, etc.

    ..seealso:: :class:`~flask_wtf.file.FileAllowed`, etc.
    ..seealso:: https://github.com/lepture/flask-wtf/issues/201
    ..todo:: Write doctest cases
    """
    def __call__(self, form, field):
        """Modified from parent to allow complex exntesions.
        """
        if not field.has_file():
            return

        filename = field.data.filename.lower()

        if isinstance(self.upload_set, (tuple, list)):
            if any(filename.endswith('.' + x) for x in self.upload_set):
                return
            message = ("File does not end with any of allowed extensions: "
                       "{}".format(self.upload_set))
            raise WV.StopValidation(self.message or message)

        if not self.upload_set.file_allowed(field.data, filename):
            msg = self.message or 'File does not have an approved extension'
            raise WV.StopValidation(msg)


class UploadForm(flask_wtf.Form):
    """Form to upload RPM DB archive files.
    """
    vtrs = [flask_wtf.file.FileRequired(),
            FileAllowedEx(("zip", "tar.xz", "tar.bz2", "tar.gz"),
                          "Archive files only!")]

    filename = flask_wtf.file.FileField("archive", validators=vtrs)
    submit = wtforms.SubmitField("Upload")


class AnalysisInfoForm(flask_wtf.Form):
    """Form to input/select some basic information to start analysis.
    """
    # TODO: Select repos dynamically by dist.
    # See also: https://gist.github.com/Overdese/abebc48e878662377988
    #
    # dists = [("auto", "Auto detection"), ("rhel5", "RHEL 5"),
    #         ("rhel6", "RHEL 6"), ("rhel7", "RHEL 7")]
    # dist = wtforms.SelectField("OS Distribution", choices=dists,
    #                           default="auto")
    repos = wtforms.SelectMultipleField("Yum Repo[s]")

    _wds_msg = ("A string of letters (a-zA-Z0-9), or "
                "strings of letters separated by spaces")
    _wds_vrts = [WV.Required(),
                 WV.Regexp(r"^\w+(?:\W+\w+)*$", message=_wds_msg)]

    _kwds_default = ' '.join(fleure.globals.ERRATA_KEYWORDS)
    keywords = wtforms.StringField("Errata filtering keywords",
                                   validators=_wds_vrts, default=_kwds_default)
    _rpms_default = ' '.join(fleure.globals.CORE_RPMS)
    core_rpms = wtforms.StringField("Core RPMs", validators=_wds_vrts,
                                    default=_rpms_default)

    # TBD:
    # start_date = wtforms.DateTimeField("Start date", format="%Y-%m-%d")
    # end_date = wtforms.StringField("End date", format="%Y-%m-%d")

    submit = wtforms.SubmitField("Analyze")

# vim:sw=4:ts=4:et:
