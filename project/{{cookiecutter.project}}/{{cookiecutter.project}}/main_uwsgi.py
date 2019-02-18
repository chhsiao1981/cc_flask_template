#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gevent.monkey
gevent.monkey.patch_all()

import ujson as json
import re
from gevent.wsgi import WSGIServer

from {{cookiecutter.project}}.constants import *
from {{cookiecutter.project}} import cfg
from {{cookiecutter.project}} import util
from {{cookiecutter.project}}.util import Error


from rx_med_analysis import main
from rx_med_analysis.main import app

main_flask._main()

if __name__ == '__main__':
    args = _main()
    cfg.logger.warning('to run server')

    http_server = WSGIServer(('127.0.0.1', args.port), main_flask.app)
    http_server.serve_forever()
