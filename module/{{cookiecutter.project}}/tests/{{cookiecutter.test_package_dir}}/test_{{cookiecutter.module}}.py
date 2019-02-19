# -*- coding: utf-8 -*-

from {{cookiecutter.project}}.constants import *

import unittest
import logging

from {{cookiecutter.project}} import cfg
from {{cookiecutter.project}} import util
from {{cookiecutter.project}}.util import Error
from {{cookiecutter.pkg}} import {{cookiecutter.module}}
from tests import Object


class Test{{cookiecutter.Module}}(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
