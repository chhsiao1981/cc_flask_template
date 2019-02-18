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

from rx_med_analysis.constants import *
from rx_med_analysis import cfg
from rx_med_analysis import util
from rx_med_analysis.utils import util_flask
from rx_med_analysis.utils.util_flask import app, login_manager, User, _process_options_header, _process_header, crossdomain, db, LoginForm
from rx_med_analysis.util import Error

from rx_med_analysis.my_social_auth.routes import social_auth

from rx_med_analysis.http_handlers import get_flask_user_handler

from rx_med_analysis.http_handlers import get_demo_topics_handler
from rx_med_analysis.http_handlers.get_topic_handler import get_topic_handler
from rx_med_analysis.http_handlers.get_topics_handler import get_topics_handler
from rx_med_analysis.http_handlers.get_random_handler import get_random_handler

from rx_med_analysis.http_handlers.get_study_info_list_handler import get_study_info_list_handler
from rx_med_analysis.http_handlers.get_study_info_list_from_id_handler import get_study_info_list_from_id_handler
from rx_med_analysis.http_handlers.get_group_info_list_handler import get_group_info_list_handler
from rx_med_analysis.http_handlers.get_group_info_list_from_id_handler import get_group_info_list_from_id_handler
from rx_med_analysis.http_handlers.get_subject_info_list_handler import get_subject_info_list_handler
from rx_med_analysis.http_handlers.get_subject_info_list_from_id_handler import get_subject_info_list_from_id_handler
from rx_med_analysis.http_handlers.get_session_info_list_handler import get_session_info_list_handler
from rx_med_analysis.http_handlers.get_session_info_list_from_id_handler import get_session_info_list_from_id_handler

from rx_med_analysis.http_handlers.add_study_meta_handler import add_study_meta_handler
from rx_med_analysis.http_handlers.add_meta_handler import add_meta_handler
from rx_med_analysis.http_handlers.get_meta_handler import get_meta_handler
from rx_med_analysis.http_handlers.get_display_blocks_handler import get_display_blocks_handler
from rx_med_analysis.http_handlers.get_project_blocks_handler import get_project_blocks_handler
from rx_med_analysis.http_handlers.get_dcs_info_handler import get_dcs_info_handler
from rx_med_analysis.http_handlers.get_dcs_g2_fit_handler import get_dcs_g2_fit_handler
from rx_med_analysis.http_handlers.get_ivy_data_handler import get_ivy_data_handler
from rx_med_analysis.http_handlers import get_ivy_nirs_data_handler
from rx_med_analysis.http_handlers import get_ivy_dcs_data_handler
from rx_med_analysis.http_handlers import get_ivy_single_dcs_data_handler
from rx_med_analysis.http_handlers.get_project_cal_blocks_handler import get_project_cal_blocks_handler
from rx_med_analysis.http_handlers.get_nirs_info_handler import get_nirs_info_handler
from rx_med_analysis.http_handlers.get_meta_list_handler import get_meta_list_handler

from rx_med_analysis.http_handlers.get_dcs_info2_handler import get_dcs_info2_handler
from rx_med_analysis.http_handlers.get_nirs_info2_handler import get_nirs_info2_handler

from rx_med_analysis.http_handlers.get_dcs_bfi_handler import get_dcs_bfi_handler
from rx_med_analysis.http_handlers.upload_handler import upload_handler
from rx_med_analysis.http_handlers.get_process_status_handler import get_process_status_handler

from rx_med_analysis.http_handlers.get_edit_meta_list_handler import get_edit_meta_list_handler


@app.before_request
def global_user():
    flask.g.user = flask_login.current_user


@app.route('/')
@crossdomain()
def dummy():
    params = _process_params()
    result, status, headers = _process_result(None, 1)
    cfg.logger.warning('result: %s status: %s headers: %s', result, status, headers)
    return result, status, headers


@app.route('/dummy')
@login_required
@crossdomain()
def dummy2():
    params = _process_params()
    result, status, headers = _process_result(None, "dummy")
    cfg.logger.warning('result: %s status: %s headers: %s', result, status, headers)
    return result, status, headers


@app.route('/get/demo_topics')
@login_required
@crossdomain()
def get_demo_topics():
    return Response(stream_with_context(get_demo_topics_handler.generator()), content_type='text/event-stream')


@app.route('/get/user', methods=['GET', 'POST', 'OPTIONS'])
@login_required
@crossdomain()
def get_user():
    cfg.logger.warning('remote_addr: %s host: %s', request.remote_addr, request.url)
    error, data = get_flask_user_handler.get_flask_user_handler()
    return _process_result(error, data)


@app.route('/get/study_info_list', methods=['GET', 'POST', 'OPTIONS'])
@login_required
@crossdomain()
def get_study_info_list():
    params = _process_params()
    error, results = get_study_info_list_handler(params)
    return _process_result(error, results)


@app.route('/get/study_info_list_from_id', methods=['GET', 'POST', 'OPTIONS'])
@login_required
@crossdomain()
def get_study_info_list_from_id():
    params = _process_params()
    error, results = get_study_info_list_from_id_handler(params)
    return _process_result(error, results)


@app.route('/get/group_info_list', methods=['GET', 'POST', 'OPTIONS'])
@login_required
@crossdomain()
def get_group_info_list():
    params = _process_params()
    error, results = get_group_info_list_handler(params)
    return _process_result(error, results)


@app.route('/get/group_info_list_from_id', methods=['GET', 'POST', 'OPTIONS'])
@login_required
@crossdomain()
def get_group_info_list_from_id():
    params = _process_params()
    error, results = get_group_info_list_from_id_handler(params)
    return _process_result(error, results)


@app.route('/get/subject_info_list', methods=['GET', 'POST', 'OPTIONS'])
@login_required
@crossdomain()
def get_subject_info_list():
    params = _process_params()
    error, results = get_subject_info_list_handler(params)
    return _process_result(error, results)


@app.route('/get/subject_info_list_from_id', methods=['GET', 'POST', 'OPTIONS'])
@login_required
@crossdomain()
def get_subject_info_list_from_id():
    params = _process_params()
    error, results = get_subject_info_list_from_id_handler(params)
    return _process_result(error, results)


@app.route('/get/session_info_list', methods=['GET', 'POST', 'OPTIONS'])
@login_required
@crossdomain()
def get_session_info_list():
    params = _process_params()
    error, results = get_session_info_list_handler(params)
    return _process_result(error, results)


@app.route('/get/session_info_list_from_id', methods=['GET', 'POST', 'OPTIONS'])
@login_required
@crossdomain()
def get_session_info_list_from_id():
    params = _process_params()
    error, results = get_session_info_list_from_id_handler(params)
    return _process_result(error, results)


@app.route('/add/study_meta', methods=['GET', 'POST', 'OPTIONS'])
@login_required
@crossdomain()
def add_study_meta():
    params = _process_params()

    error, results = add_study_meta_handler(params)

    return _process_result(error, results)


@app.route('/add/meta', methods=['GET', 'POST', 'OPTIONS'])
@login_required
@crossdomain()
def add_meta():
    params = _process_params()
    error, results = add_meta_handler(params)
    return _process_result(error, results)


@app.route('/get/meta', methods=['GET', 'POST', 'OPTIONS'])
@login_required
@crossdomain()
def get_meta():
    params = _process_params()
    error, results = get_meta_handler(params)
    return _process_result(error, results)


@app.route('/get/display_blocks', methods=['GET', 'POST', 'OPTIONS'])
@login_required
@crossdomain()
def get_display_blocks():
    params = _process_params()
    error, results = get_display_blocks_handler(params)
    return _process_result(error, results)


@app.route('/get/project_blocks', methods=['GET', 'POST', 'OPTIONS'])
@login_required
@crossdomain()
def get_project_blocks():
    params = _process_params()
    error, results = get_project_blocks_handler(params)
    return _process_result(error, results)


@app.route('/get/project_cal_blocks', methods=['GET', 'POST', 'OPTIONS'])
@login_required
@crossdomain()
def get_project_cal_blocks():
    params = _process_params()
    error, results = get_project_cal_blocks_handler(params)
    return _process_result(error, results)


@app.route('/get/dcs_info', methods=['GET', 'POST', 'OPTIONS'])
@login_required
@crossdomain()
def get_dcs_info():
    params = _process_params()
    error, results = get_dcs_info_handler(params)
    return _process_result(error, results)


@app.route('/get/dcs_g2_fit', methods=['GET', 'POST', 'OPTIONS'])
@login_required
@crossdomain()
def get_dcs_g2_fit():
    params = _process_params()
    error, results = get_dcs_g2_fit_handler(params)
    return _process_result(error, results)


@app.route('/get/nirs_info', methods=['GET', 'POST', 'OPTIONS'])
@login_required
@crossdomain()
def get_nirs_info():
    params = _process_params()
    error, results = get_nirs_info_handler(params)
    return _process_result(error, results)


@app.route('/get/ivy_data', methods=['GET', 'POST', 'OPTIONS'])
@login_required
@crossdomain()
def get_ivy_data():
    params = _process_params()
    error, results = get_ivy_data_handler(params)
    return _process_result(error, results)


@app.route('/get/ivy_nirs_data', methods=['GET', 'POST', 'OPTIONS'])
@login_required
@crossdomain()
def get_ivy_nirs_data():
    params = _process_params()
    error, results = get_ivy_nirs_data_handler.get_ivy_nirs_data_handler(params)
    return _process_result(error, results)


@app.route('/get/ivy_dcs_data', methods=['GET', 'POST', 'OPTIONS'])
@login_required
@crossdomain()
def get_ivy_dcs_data():
    params = _process_params()
    error, results = get_ivy_dcs_data_handler.get_ivy_dcs_data_handler(params)
    return _process_result(error, results)


@app.route('/get/ivy_single_dcs_data', methods=['GET', 'POST', 'OPTIONS'])
@login_required
@crossdomain()
def get_ivy_single_dcs_data():
    params = _process_params()
    error, results = get_ivy_single_dcs_data_handler.get_ivy_single_dcs_data_handler(params)
    return _process_result(error, results)


@app.route('/get/meta_list', methods=['GET', 'POST', 'OPTIONS'])
@login_required
@crossdomain()
def get_meta_list():
    params = _process_params()
    error, results = get_meta_list_handler(params)
    return _process_result(error, results)


@app.route('/get/edit_meta_list', methods=['GET', 'POST', 'OPTIONS'])
@login_required
@crossdomain()
def get_edit_meta_list():
    params = _process_params()
    error, results = get_edit_meta_list_handler(params)
    return _process_result(error, results)


@app.route('/get/dcs_info2', methods=['GET', 'POST', 'OPTIONS'])
@login_required
@crossdomain()
def get_dcs_info2():
    params = _process_params()
    error, results = get_dcs_info2_handler(params)
    return _process_result(error, results)


@app.route('/get/dcs_bfi', methods=['GET', 'POST', 'OPTIONS'])
@login_required
@crossdomain()
def get_dcs_bfi():
    params = _process_params()
    error, results = get_dcs_bfi_handler(params)
    return _process_result(error, results)


'''
@app.route('/get/dcs_g2_fit', methods=['GET', 'POST', 'OPTIONS'])
@login_required
@crossdomain()
def get_dcs_g2_fit():
    params = _process_params()
    error, results = get_dcs_g2_fit_handler(params)
    return _process_result(error, results)
'''

@app.route('/get/nirs_info2', methods=['GET', 'POST', 'OPTIONS'])
@login_required
@crossdomain()
def get_nirs_info2():
    params = _process_params()
    error, results = get_nirs_info2_handler(params)
    return _process_result(error, results)


@app.route('/upload', methods=['POST', 'OPTIONS'])
@login_required
@crossdomain()
def upload():
    params = _process_query()

    error, results = upload_handler(params, request.files)
    return _process_result(error, results)


@app.route('/get/process_status', methods=['GET', 'POST', 'OPTIONS'])
@login_required
@crossdomain()
def get_process_status():
    params = _process_params()

    error, results = get_process_status_handler(params)
    return _process_result(error, results)


@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('images', path)


@app.route('/static/js/<path:path>')
def send_js(path):
    return render_template('security/static/js/' + path)

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
    parser = argparse.ArgumentParser(description='rx_med_analysis')
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
        'MAIL_DEFAULT_SENDER': 'noreply@cloud.babynirs.org',
        'MAIL_PORT': cfg.config.get('mail_port', 465),
        'MAIL_USE_SSL': cfg.config.get('mail_use_ssl', True),
        'MAIL_USER_NAME': cfg.config.get('mail_username', ''),
        'MAIL_PASSWORD': cfg.config.get('mail_password', ''),
        # 'SOCIAL_AUTH_USER_MODEL': 'rx_med_analysis.utils.util_flask.User',
        # 'SOCIAL_AUTH_FIELDS_STORED_IN_SESSION': ['keep'],
        # 'SOCIAL_AUTH_AUTHENTICATION_BACKENDS': [
        #     'social_core.backends.email.EmailAuth',
        # ],
        # 'SOCIAL_AUTH_EMAIL_FORM_URL': '/my-login-form',
        # 'SOCIAL_AUTH_EMAIL_FORM_HTML': '',
        # 'SOCIAL_AUTH_EMAIL_FORM_HTML': 'email_form.html',
        # 'SOCIAL_AUTH_EMAIL_VALIDATION_FUNCTION': 'rx_med_analysis.my_social_auth.email_validation.email_validation',
        # 'SOCIAL_AUTH_EMAIL_VALIDATION_URL': '/my-login-form',
        # 'SOCIAL_AUTH_REVOKE_TOKENS_ON_DISCONNECT': True,
        # 'SOCIAL_AUTH_PIPELINE': [
        #     'rx_med_analysis.my_social_auth.hash_info.hash_info',
        #     'social_core.pipeline.social_auth.social_details',
        #     'social_core.pipeline.social_auth.social_uid',
        #    'social_core.pipeline.social_auth.auth_allowed',
        #    'social_core.pipeline.social_auth.social_user',
        #    'social_core.pipeline.user.get_username',
        #    'social_core.pipeline.mail.mail_validation',
        #    'social_core.pipeline.social_auth.associate_by_email',
        #    'social_core.pipeline.user.create_user',
        #    'social_core.pipeline.social_auth.associate_user',
        #    'rx_med_analysis.my_social_auth.user_password.user_password',
        #    'social_core.pipeline.social_auth.load_extra_data',
        #    'social_core.pipeline.user.user_details',
        #],
        #'SOCIAL_AUTH_DISCONNECT_PIPELINE': [
        #    'social_core.pipeline.disconnect.allowed_to_disconnect',
        #    'social_core.pipeline.disconnect.get_entries',
        #    'social_core.pipeline.disconnect.revoke_tokens',
        #    'social_core.pipeline.disconnect.disconnect',
        #],
    })

    # XXX hack for User and Role
    util_flask._init_db(is_csrf=args.is_csrf)
    from rx_med_analysis.utils.util_flask import User

    # init_social(app, util_flask.db)
    # app.register_blueprint(social_auth.social_auth)


def _main():
    error, args = parse_args()
    cfg.init({"port": args.port, "ini_filename": args.ini, 'log_filename': args.log_filename})
    cfg._init_mongo()
    cfg._init_redis()
    get_demo_topics_handler.init()
    get_ivy_nirs_data_handler.init()
    get_ivy_dcs_data_handler.init()
    get_ivy_single_dcs_data_handler.init()

    cfg.logger.warning('after _init_mongo: %s', cfg.config)

    _init_app(args)

    return args


if __name__ == '__main__':
    args = _main()
    cfg.logger.warning('to run server')

    http_server = WSGIServer(('127.0.0.1', args.port), app)
    http_server.serve_forever()
