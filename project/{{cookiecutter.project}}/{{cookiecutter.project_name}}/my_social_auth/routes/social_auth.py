# -*- coding: utf-8 -*-

import ujson as json
import re

from flask import g, Blueprint, request, make_response
from flask_login import login_required, login_user

from social_core.actions import do_auth, do_complete, do_disconnect
from social_flask.utils import psa

from {{cookiecutter.project_name}}.constants import *
from {{cookiecutter.project_name}} import cfg
from {{cookiecutter.project_name}} import util
from {{cookiecutter.project_name}}.util import Error
from {{cookiecutter.project_name}}.utils.util_flask import _process_header


social_auth = Blueprint('social', __name__)


@social_auth.route('/login/<path:backend>/', methods=('OPTIONS',))
def options(backend):
    cfg.logger.warning('backend: %s', backend)
    resp = make_response('', 200)
    resp = _process_header(resp, request, mime='application/json')
    return resp


@social_auth.route('/login/<string:backend>/', methods=('GET', 'POST'))
@psa('social.complete')
def auth(backend):
    resp = do_auth(g.backend)
    resp = _process_header(resp, request)
    cfg.logger.warning('resp: %s headers: %s', resp, resp.headers)
    return resp


@social_auth.route('/complete/<string:backend>/', methods=('GET', 'POST'))
@psa('social.complete')
def complete(backend, *args, **kwargs):
    """Authentication complete view, override this view if transaction
    management doesn't suit your needs."""
    cfg.logger.warning('start: backend: %s args: %s kwargs: %s', backend, args, kwargs)
    resp = do_complete(g.backend, login=do_login, user=g.user._get_current_object(),
                       *args, **kwargs)
    cfg.logger.warning('resp: %s headers: %s', resp, resp.headers)

    return resp


@social_auth.route('/disconnect/<string:backend>/', methods=('GET', 'POST',))
@social_auth.route('/disconnect/<string:backend>/<int:association_id>/',
                   methods=('GET', 'POST',))
@social_auth.route('/disconnect/<string:backend>/<string:association_id>/',
                   methods=('GET', 'POST',))
@login_required
@psa()
def disconnect(backend, association_id=None):
    """Disconnects given backend from current logged in user."""
    return do_disconnect(g.backend, g.user, association_id)


def do_login(backend, user, social_user):
    name = backend.strategy.setting('REMEMBER_SESSION_NAME', 'keep')
    remember = backend.strategy.session_get(name) or \
        request.cookies.get(name) or \
        request.args.get(name) or \
        request.form.get(name) or \
        False
    return login_user(user, remember=remember)
