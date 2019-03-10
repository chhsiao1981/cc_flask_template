# -*- coding: utf-8 -*-

import ujson as json
import re

from rx_med_analysis.constants import *
from rx_med_analysis import cfg
from rx_med_analysis import util
from rx_med_analysis.util import Error


def user_password(strategy, backend, user, is_new=False, request=None, response=None, *args, **kwargs):
    if backend.name != 'email':
        return

    if request is None:
        request = {}

    if response is None:
        response = {}

    if 'verification_code' not in request:
        return

    request_data = strategy.request_data()

    password = response['password']
    if isinstance(password, list):
        password = password[0]
    cfg.logger.warning('user: (%s/%s/%s) request_data: %s is_new: %s request: %s response: %s password: %s args: %s kwargs: %s validate: (%s/%s/%s/%s/%s)', user, type(user), dir(user), request_data, is_new, request, response, password, args, kwargs, type(user.validate), dir(user.validate), user.validate.__call__, user.validate.__func__, user.validate.__self__)

    if is_new:
        user.password = password
        user.save()
    elif not user.validate(password):
        # return {'user': None, 'social': None}
        raise AuthForbidden(backend)
