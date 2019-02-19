# -*- coding: utf-8 -*-
"""Collection of utility functions

Including:
    * Error
    * Result
    * mongo-op
    * type-conversion
    * timestamp
    * http
    * json / avro
    * sys
    * save_to_global / save_to_cloud
    * gen_ranomd_string
    * serialize-deserialize
    * misc

"""

from {{cookiecutter.project_name}}.constants import S_OK, S_ERR, S_ERR_ALREADY_EXIST, SESSION_EXPIRE_TIMESTAMP, HTTP_TIMEOUT

import os
import random
import math
import uuid
import base64
import time
import json as json
import pytz
import calendar
import arrow
from subprocess import Popen, PIPE
import string
import re
import itertools
import struct

from {{cookiecutter.project_name}} import cfg

##########
# Error
##########

from {{cookiecutter.project_name}}.utils.util_error import Error
from {{cookiecutter.project_name}}.utils.util_error import ERROR_EMPTY
from {{cookiecutter.project_name}}.utils.util_error import ERROR_NOT_IMPLEMENT

##########
# DB
##########

from {{cookiecutter.project_name}}.utils.util_db import db_find_one_ne
from {{cookiecutter.project_name}}.utils.util_db import db_find_one
from {{cookiecutter.project_name}}.utils.util_db import db_find_ne
from {{cookiecutter.project_name}}.utils.util_db import db_find
from {{cookiecutter.project_name}}.utils.util_db import db_find_it_ne
from {{cookiecutter.project_name}}.utils.util_db import db_find_it
from {{cookiecutter.project_name}}.utils.util_db import db_insert_ne
from {{cookiecutter.project_name}}.utils.util_db import db_insert
from {{cookiecutter.project_name}}.utils.util_db import db_bulk_update
from {{cookiecutter.project_name}}.utils.util_db import db_force_bulk_update
from {{cookiecutter.project_name}}.utils.util_db import db_update
from {{cookiecutter.project_name}}.utils.util_db import db_force_update
from {{cookiecutter.project_name}}.utils.util_db import db_save
from {{cookiecutter.project_name}}.utils.util_db import db_remove
from {{cookiecutter.project_name}}.utils.util_db import db_force_remove
from {{cookiecutter.project_name}}.utils.util_db import db_distinct
from {{cookiecutter.project_name}}.utils.util_db import db_set_if_not_exists
from {{cookiecutter.project_name}}.utils.util_db import db_find_and_modify
from {{cookiecutter.project_name}}.utils.util_db import db_aggregate_iter
from {{cookiecutter.project_name}}.utils.util_db import db_aggregate
from {{cookiecutter.project_name}}.utils.util_db import db_aggregate_parse_results
from {{cookiecutter.project_name}}.utils.util_db import db_aggregate_parse_result
from {{cookiecutter.project_name}}.utils.util_db import db_largest
from {{cookiecutter.project_name}}.utils.util_db import db_largest_list

##########
# Timestamp
##########

from {{cookiecutter.project_name}}.utils.util_timestamp import timestamp_to_datetime
from {{cookiecutter.project_name}}.utils.util_timestamp import datetime_to_timestamp
from {{cookiecutter.project_name}}.utils.util_timestamp import datetime_to_microtimestamp
from {{cookiecutter.project_name}}.utils.util_timestamp import get_timestamp
from {{cookiecutter.project_name}}.utils.util_timestamp import get_milli_timestamp
from {{cookiecutter.project_name}}.utils.util_timestamp import get_micro_timestamp
from {{cookiecutter.project_name}}.utils.util_timestamp import get_hr_timestamp
from {{cookiecutter.project_name}}.utils.util_timestamp import timestamp_to_hr_timestamp
from {{cookiecutter.project_name}}.utils.util_timestamp import timestamp_to_day_timestamp
from {{cookiecutter.project_name}}.utils.util_timestamp import micro_timestamp_to_datetime

##########
# Sys
##########

from {{cookiecutter.project_name}}.utils.util_sys import makedirs
from {{cookiecutter.project_name}}.utils.util_sys import process_cmd

##########
# JSON
##########

from {{cookiecutter.project_name}}.utils.util_json import json_dumps_ne
from {{cookiecutter.project_name}}.utils.util_json import json_dumps
from {{cookiecutter.project_name}}.utils.util_json import json_loads_ne
from {{cookiecutter.project_name}}.utils.util_json import json_loads

##########
# HTTP
##########

from {{cookiecutter.project_name}}.utils.util_http import http_multipost
from {{cookiecutter.project_name}}.utils.util_http import http_multipost_list
from {{cookiecutter.project_name}}.utils.util_http import http_multiget
from {{cookiecutter.project_name}}.utils.util_http import send_requests
from {{cookiecutter.project_name}}.utils.util_http import send_requests_with_different_params

##########
# type
##########

from {{cookiecutter.project_name}}.utils.util_type import _str
from {{cookiecutter.project_name}}.utils.util_type import _unicode
from {{cookiecutter.project_name}}.utils.util_type import _int
from {{cookiecutter.project_name}}.utils.util_type import _float
from {{cookiecutter.project_name}}.utils.util_type import _bool

##########
# misc
##########

from {{cookiecutter.project_name}}.utils.util_misc import gen_ranomd_string
from {{cookiecutter.project_name}}.utils.util_misc import flatten
from {{cookiecutter.project_name}}.utils.util_misc import flatten_results_with_error
