#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gevent.monkey
gevent.monkey.patch_all()

import ujson as json
import re
import argparse
import copy
from gevent.wsgi import WSGIServer
import traceback

import flask
import flask_login
from flask.json import jsonify
from flask import make_response, request, session, send_from_directory, Response, stream_with_context, render_template
from flask_security import login_required
from flask_security import login_user
from social_flask_mongoengine.models import init_social
from wtforms import Form, TextField

from {{cookiecutter.project}}.constants import *
from {{cookiecutter.project}} import cfg
from {{cookiecutter.project}} import util
from {{cookiecutter.project}}.utils import util_flask
from {{cookiecutter.project}}.utils.util_flask import app, login_manager, User, _process_options_header, _process_header, crossdomain, db, LoginForm
from {{cookiecutter.project}}.util import Error

from {{cookiecutter.project}}.my_social_auth.routes import social_auth


@app.before_request
def global_user():
    flask.g.user = flask_login.current_user


@app.route('/')
@crossdomain()
def dummy():
    params = _process_params()
    result, status, headers = _process_result(None, 1)
    cfg.logger.info('result: %s status: %s headers: %s', result, status, headers)
    return result, status, headers


@app.route('/dummy')
@login_required
@crossdomain()
def dummy2():
    params = _process_params()
    result, status, headers = _process_result(None, "dummy")
    cfg.logger.info('result: %s status: %s headers: %s', result, status, headers)
    return result, status, headers


def _process_query():
    qs_dict = request.args

    result = {}
    for key, val in qs_dict.items():
        result_val = val if not isinstance(val, list) else val[-1]
        result[key] = result_val

    return result


def _process_params():
    qs_dict = request.values
    form_dict = request.form

    result = {}
    for key, val in qs_dict.items():
        result_val = val if not isinstance(val, list) else val[-1]
        result[key] = result_val

    for key, val in form_dict.items():
        result_val = val if not isinstance(val, list) else val[-1]
        result[key] = result_val

    return result


def _process_file_content():
    the_file = request.files.get('file', None)
    if not the_file:
        return Error(S_ERR, 'no file'), None

    content = ''
    error = None
    try:
        content = the_file.read()
    except Exception as e:
        error = Error(S_ERR, 'unable to read content: e: %s' % (e))

    if error:
        return error, None

    return None, content


def _process_json_request():
    return util.json_loads_ne(_process_body_request())


def _process_body_request():
    f = request.body
    f.seek(0)
    return f.read()


def _process_result(error, the_obj, status_code=200, mime='application/json', headers=None):
    if headers is None:
        headers = {}

    headers['Content-Type'] = mime

    if error:
        http_result = {'success': False, 'error': str(error)}
    else:
        http_result = {'success': True, 'data': the_obj}

    return util.json_dumps_ne(http_result), status_code, headers


def parse_args():
    ''' '''
    parser = argparse.ArgumentParser(description='{{cookiecutter.project}}')
    parser.add_argument('-i', '--ini', type=str, required=True, help="ini filename")
    parser.add_argument('-l', '--log_filename', type=str, default='', required=False, help="log filename")
    parser.add_argument('-p', '--port', type=int, required=True, help="port")
    parser.add_argument('-c', '--is_csrf', type=bool, required=False, default=False, help="csrf")

    args = parser.parse_args()

    return None, args


def _init_app(args):
    app.config.update({
        'SECRET_KEY': cfg.config.get('flask_secret_key', 'default_secret_key'),
        # 'SERVER_NAME': cfg.config.get('flask_server_name', ''),
        # 'PREFERRED_URL_SCHEME': 'http',
        'DEBUG': True,
        'MONGODB_SETTINGS': {
            'db': 'flask_mongoengine',
            'host': cfg.config.get('flask_mongoengine_host', 'localhost'),
            'port': cfg.config.get('flask_mongoengine_port', 27017),
        },
        'SESSION_PROTECTION': 'strong',
        'SECURITY_PASSWORD_HASH': 'sha512_crypt',
        'SECURITY_PASSWORD_SALT': cfg.config.get('flask_security_salt', 'default_salt'),
        'SECURITY_RECOVERABLE': True,
        'SECURITY_REGISTERABLE': False,
        'SECURITY_CONFIRMABLE': cfg.config.get('flask_security_confirmable', True),
        'SECURITY_POST_LOGOUT_VIEW': '/login',
        'SECURITY_LOGIN_USER_TEMPLATE': 'security/index.html',
        'SOCIAL_AUTH_STORAGE': 'social_flask_mongoengine.models.FlaskStorage',
        'MAIL_SERVER': cfg.config.get('mail_server', 'localhost'),
        'MAIL_DEFAULT_SENDER': 'noreply@example.com',
        'MAIL_PORT': cfg.config.get('mail_port', 465),
        'MAIL_USE_SSL': cfg.config.get('mail_use_ssl', True),
        'MAIL_USER_NAME': cfg.config.get('mail_username', ''),
        'MAIL_PASSWORD': cfg.config.get('mail_password', ''),
        # 'SOCIAL_AUTH_USER_MODEL': '{{cookiecutter.project}}.utils.util_flask.User',
        # 'SOCIAL_AUTH_FIELDS_STORED_IN_SESSION': ['keep'],
        # 'SOCIAL_AUTH_AUTHENTICATION_BACKENDS': [
        #     'social_core.backends.email.EmailAuth',
        # ],
        # 'SOCIAL_AUTH_EMAIL_FORM_URL': '/my-login-form',
        # 'SOCIAL_AUTH_EMAIL_FORM_HTML': '',
        # 'SOCIAL_AUTH_EMAIL_FORM_HTML': 'email_form.html',
        # 'SOCIAL_AUTH_EMAIL_VALIDATION_FUNCTION': '{{cookiecutter.project}}.my_social_auth.email_validation.email_validation',
        # 'SOCIAL_AUTH_EMAIL_VALIDATION_URL': '/my-login-form',
        # 'SOCIAL_AUTH_REVOKE_TOKENS_ON_DISCONNECT': True,
        # 'SOCIAL_AUTH_PIPELINE': [
        #     '{{cookiecutter.project}}.my_social_auth.hash_info.hash_info',
        #     'social_core.pipeline.social_auth.social_details',
        #     'social_core.pipeline.social_auth.social_uid',
        #     'social_core.pipeline.social_auth.auth_allowed',
        #     'social_core.pipeline.social_auth.social_user',
        #     'social_core.pipeline.user.get_username',
        #     'social_core.pipeline.mail.mail_validation',
        #     'social_core.pipeline.social_auth.associate_by_email',
        #     'social_core.pipeline.user.create_user',
        #     'social_core.pipeline.social_auth.associate_user',
        #     '{{cookiecutter.project}}.my_social_auth.user_password.user_password',
        #     'social_core.pipeline.social_auth.load_extra_data',
        #     'social_core.pipeline.user.user_details',
        # ],
        # 'SOCIAL_AUTH_DISCONNECT_PIPELINE': [
        #     'social_core.pipeline.disconnect.allowed_to_disconnect',
        #     'social_core.pipeline.disconnect.get_entries',
        #     'social_core.pipeline.disconnect.revoke_tokens',
        #     'social_core.pipeline.disconnect.disconnect',
        # ],
    })

    # XXX hack for User and Role
    util_flask._init_db(is_csrf=args.is_csrf)
    from {{cookiecutter.project}}.utils.util_flask import User

    # init_social(app, util_flask.db)
    # app.register_blueprint(social_auth.social_auth)


def _main():
    error, args = parse_args()
    cfg.init({"port": args.port, "ini_filename": args.ini, 'log_filename': args.log_filename})
    cfg._init_mongo()

    cfg.logger.info('after _init_mongo: %s', cfg.config)

    _init_app(args)

    return args


if __name__ == '__main__':
    args = _main()
    cfg.logger.info('to run server')

    http_server = WSGIServer(('127.0.0.1', args.port), app)
    http_server.serve_forever()
