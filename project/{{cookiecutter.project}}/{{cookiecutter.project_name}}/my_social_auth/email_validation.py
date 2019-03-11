# -*- coding: utf-8 -*-

import ujson as json
import re

from flask import url_for

from {{cookiecutter.project_name}}.constants import *
from {{cookiecutter.project_name}} import cfg
from {{cookiecutter.project_name}} import util
from {{cookiecutter.project_name}}.util import Error


def email_validation(strategy, backend, code, session_token, *args, **kwargs):
    '''
    send email with verification url
    '''

    cfg.logger.warning('strategy: %s backend: %s code: (%s/%s/%s), session_token: %s args: %s kwargs: %s', strategy, backend, code, type(code), code.code, session_token, args, kwargs)

    url = url_for('social.complete',
                  backend=backend.name,
                  _external=True)

    url += '?verification_code=' + code.code
    cfg.logger.warning('url: %s', url)
