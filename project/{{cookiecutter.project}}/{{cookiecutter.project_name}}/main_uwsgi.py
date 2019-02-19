#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gevent.monkey
gevent.monkey.patch_all()

import ujson as json
import re
from gevent.wsgi import WSGIServer

from {{cookiecutter.project_name}}.constants import *
from {{cookiecutter.project_name}} import cfg
from {{cookiecutter.project_name}} import util
from {{cookiecutter.project_name}}.util import Error

from {{cookiecutter.project_name}} import main


if __name__ == '__main__':
    args = main._main()
    cfg.logger.warning('to run server')

    http_server = WSGIServer(('127.0.0.1', args.port), main.app)
    http_server.serve_forever()
