"""HTML Forms.

License: BSD as the part of this code is derived from flask.wtf.

References:
  - Flask-flask_wtf: https://flask-wtf.readthedocs.org
  - wtforms: http://wtforms.simplecodes.com/docs/0.6.1/validators.html
"""
from __future__ import absolute_import

import flask_wtf.file
import flask_wtf
import uuid
import wtforms.validators as WV
import wtforms

from wtforms import StringField

import fleure.globals
import fleure.utils


def gen_hid():
    """Generate Host ID.
    """
    return str(uuid.uuid4())


class FileAllowedEx(flask_wtf.file.FileAllowed):
    """
    A little bit modified version of flask_wtf.FileAllowed to allow composite
    file extensions such like .tar.xz, .tar.gz, etc.

    ..seealso:: :class:`~flask_wtf.file.FileAllowed`, etc.
    ..seealso:: https://github.com/lepture/flask-wtf/issues/201
    ..todo:: Write doctest cases
    """
    def __call__(self, form, field):
        """Modified from parent to allow composite extensions.
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
    _vrts = [WV.Required(),
             WV.Regexp(r"^\S+$", 0, "Must consists of non-blank letters")]
    hostid = StringField("Hostname or Host ID",
                         description="Enter hostname or any word identify "
                                     "the target host as needed",
                         validators=_vrts, default=gen_hid())

    _vtrs = [flask_wtf.file.FileRequired(),
             FileAllowedEx(("zip", "tar.xz", "tar.bz2", "tar.gz"),
                           "Archive files only!")]
    filename = flask_wtf.file.FileField("archive", validators=_vtrs)

    submit = wtforms.SubmitField("Upload")


def _repo_choices(repos_map=None):
    """Make up repo choices.
    """
    if repos_map is None:
        repos_map = fleure.globals.REPOS_MAP

    rss = [[(k, v) for v in vs] for k, vs in repos_map.items()]
    return fleure.utils.uconcat(rss)


class AnalyzeForm(flask_wtf.Form):
    """Form to input/select some basic information to start analysis.
    """
    # TODO: Select repos dynamically by dist.
    # See also: https://gist.github.com/Overdese/abebc48e878662377988
    #
    # dists = [("auto", "Auto detection"), ("rhel5", "RHEL 5"),
    #         ("rhel6", "RHEL 6"), ("rhel7", "RHEL 7")]
    # dist = wtforms.SelectField("OS Distribution", choices=dists,
    #                           default="auto")
    _repos_desc = ("Yum repos to access. Only select some of them explicitly "
                   "if you know needed yum repos clearly.")
    repos = wtforms.SelectMultipleField("Yum Repo[s]", description=_repos_desc,
                                        choices=_repo_choices())

    _wvrts = [WV.Required(),
              WV.Regexp(r"^(\w+(?:,?\s+\w+)*)$",
                        message="Must consists of strings of letters "
                                "(a-zA-Z0-9), separated with a comma (',')"
                                "or space")]

    keywords = StringField("Errata Filter Keywords",
                           description="Keywords to select some Important "
                                       "errata separated with comma ','.",
                           validators=_wvrts,
                           default=(", ".join(fleure.globals.ERRATA_KEYWORDS)))
    core_rpms = StringField("Core RPMs",
                            description="Special RPMs to foucs on",
                            validators=_wvrts,
                            default=(" ".join(fleure.globals.CORE_RPMS)))

    # TBD:
    # start_date = wtforms.DateTimeField("Start date", format="%Y-%m-%d")
    # end_date = StringField("End date", format="%Y-%m-%d")

    submit = wtforms.SubmitField("Analyze")

# vim:sw=4:ts=4:et:
