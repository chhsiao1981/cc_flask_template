# -*- coding: utf-8 -*-

import ujson as json
import re
from flask_security.utils import hash_password as hash_password

from rx_med_analysis.constants import *
from rx_med_analysis import cfg
from rx_med_analysis import util
from rx_med_analysis.util import Error


def hash_info(strategy, backend, user, request=None, response=None, *args, **kwargs):
    request_data = strategy.request_data()
    cfg.logger.warning('strategy: %s backend: %s user: %s request_data: %s args: %s kwargs: %s', strategy, backend, user, request_data, args, kwargs)

    if 'password' in request:
        new_password = hash_password(request['password'])
        request['password'] = new_password

    if 'password' in response:
        new_password = hash_password(response['password'])
        response['password'] = new_password

    cfg.logger.warning('after hash: strategy: %s backend: %s user: %s request_data: %s args: %s kwargs: %s', strategy, backend, user, request_data, args, kwargs)
