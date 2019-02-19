# -*- coding: utf-8 -*-

from bson.objectid import ObjectId
import ujson as json
import re

from flask import Flask, make_response, request, current_app
from flask.json import jsonify
from mongoengine import StringField, ListField, BooleanField, DateTimeField, ReferenceField
from flask_mongoengine import MongoEngine, Document
import flask_security
from flask_security import Security, MongoEngineUserDatastore, UserMixin, RoleMixin
from flask_security import LoginForm as FlaskSecurityLoginForm
from social_flask.routes import social_auth
from social_flask_mongoengine.models import init_social
import flask_login
from functools import update_wrapper
from datetime import timedelta
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from werkzeug.contrib.fixers import ProxyFix

from {{cookiecutter.project_name}}.constants import *
from {{cookiecutter.project_name}} import cfg
from {{cookiecutter.project_name}}.utils.util_error import Error

try:
    from urlparse import urlsplit
except ImportError:  # pragma: no cover
    from urllib.parse import urlsplit

app = Flask(__name__.split('.')[0], root_path='./')
app.wsgi_app = ProxyFix(app.wsgi_app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

csrf = CSRFProtect()

db = None
user_datastore = None
security = None
User = None
Role = None


class LoginForm(FlaskSecurityLoginForm):

    def validate_next(self, field):
        cfg.logger.warning('validate_next: data: %s', field.data)
        if field.data and not validate_redirect_url(field.data):
            field.data = ''
            flash(*get_message('INVALID_REDIRECT'))
            raise ValidationError(get_message('INVALID_REDIRECT')[0])

# XXX hack for flask_security.utils.validate_redirect_url


def validate_redirect_url(url):
    cfg.logger.warning('hack validate redirect url: url: %s', url)
    if url is None or url.strip() == '':
        return False
    url_next = urlsplit(url)
    url_base = urlsplit(request.host_url)

    url_next_netloc = '' if not isinstance(url_next.netloc, str) else url_next.netloc
    url_base_netloc = '' if not isinstance(url_base.netloc, str) else url_base.netloc
    next_host = url_next.netloc.split(':')[0]
    base_host = url_next.netloc.split(':')[0]

    cfg.logger.warning('hack validate redirect url: next_host: %s base_host: %s', next_host, base_host)
    if (url_next.netloc or url_next.scheme):
        if next_host != base_host and next_host not in cfg.config.get('flask_valid_domain_set', []):
            cfg.logger.error('next_host != base_host: next_host: (%s/%s) base_host: (%s/%s)', next_host, type(next_host), base_host, type(base_host))
            return False

    return True


def crossdomain(origin=None, methods=None, headers=None,
                max_age=None, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if origin is not None and not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            request_orign = request.environ.get('HTTP_ORIGIN', '')

            request_headers = request.environ.get('HTTP_ACCESS_CONTROL_REQUEST_HEADERS', '')

            allow_headers = request_headers if headers is None and request_headers else headers

            h = resp.headers

            h['X-Frame-Options'] = 'SAMEORIGIN'
            h['Access-Control-Allow-Origin'] = request_orign
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Allow-Credentials'] = 'true'
            if max_age is not None:
                h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Headers'] = allow_headers

            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


def _process_header(resp, request, mime=None):
    if resp.status_code == 302:
        resp.headers['X-Frame-Options'] = 'SAMEORIGIN'
        return resp

    request_url = request.environ.get('HTTP_ORIGIN', '')

    if mime is not None:
        resp.headers['Content-Type'] = mime

    resp.headers['Accept'] = '*'
    resp.headers['Access-Control-Allow-Origin'] = request_url
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Methods'] = 'OPTIONS,GET,POST'

    request_headers = request.environ.get('HTTP_ACCESS_CONTROL_REQUEST_HEADERS', '')
    if request_headers:
        resp.headers['Access-Control-Allow-Headers'] = request_headers

    resp.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return resp


def _process_options_header(request):
    request_orign = request.environ.get('HTTP_ORIGIN', '')

    headers = {
        'Accept': '*',
        'Access-Control-Allow-Origin': request_orign,
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Allow-Methods': 'OPTIONS,GET,POST',
    }

    request_headers = request.environ.get('HTTP_ACCESS_CONTROL_REQUEST_HEADERS', '')
    if request_headers:
        headers['Access-Control-Allow-Headers'] = request_headers

    headers['X-Frame-Options'] = 'SAMEORIGIN'

    return headers


def _init_db(is_csrf=False):
    global db
    global user_datastore
    global security
    global mail
    global User
    global Role

    if is_csrf:
        csrf.init_app(app)

    db = MongoEngine(app)

    class Role(db.Document, RoleMixin):
        name = StringField(max_length=80, unique=True)
        description = StringField(max_length=255)

    class User(db.Document, UserMixin):
        username = StringField(max_length=100000)
        first_name = StringField(max_length=100000)
        last_name = StringField(max_length=100000)
        email = StringField(max_length=255)
        emails = ListField(StringField(max_length=255), default=[])
        password = StringField(max_length=255)
        active = BooleanField(default=True)
        confirmed_at = DateTimeField()
        roles = ListField(ReferenceField(Role), default=[])

    user_datastore = MongoEngineUserDatastore(db, User, Role)
    security = Security(app, user_datastore)
    mail = Mail(app)

    @app.login_manager.unauthorized_handler
    @crossdomain()
    def unauth_handler():
        return jsonify(success=False,
                       data={'login_required': True},
                       message='Authorize please to access this page'), 401

    @app.login_manager.user_loader
    def load_user(user_id):
        cfg.logger.warning('load_user: start: user_id: %s', user_id)
        try:
            error, db_result = util.db_find_one('user', {'_id': ObjectId(user_id)})
            if error:
                cfg.logger.error('unable to find user: e: %s', error)
                return
            if not db_result:
                cfg.logger.error('user not exist')
                return
            return User(username=user_id, first_name=db_result.get('first_name', ''), last_name=db_result.get('last_name', ''), email=db_result.get('email', ''))
        except (TypeError, ValueError) as e:
            cfg.logger.error('unable to get user_id: user_id: %s e: %s', user_id, e)

    # XXX hack for flask_security.utils.validate_redirect_url
    flask_security.forms.validate_redirect_url = validate_redirect_url
    flask_security.utils.validate_redirect_url = validate_redirect_url
