# -*- coding: utf-8 -*-

from {{pkg}}.constants import *

import unittest
import logging

from {{pkg}} import cfg

class Object(object):
    pass


def setup():
    cfg.logger = logging
    cfg.config = {
        'mongo_server_hostname': 'localhost',
        'mongo_server': 'test',
    }

    cfg._init_mongo()
    logging.info('cfg.config: %s', cfg.config)

    pass


def teardown():
    pass


def mock_func(*args, **kwargs):
    logging.debug('mock_func: args: %s kwargs: %s', args, kwargs)
