# -*- coding: utf-8 -*-

from {{cookiecutter.project_name}}.constants import S_OK, S_ERR, S_ERR_ALREADY_EXIST

from {{cookiecutter.project_name}} import cfg
from {{cookiecutter.project_name}}.utils.util_error import Error


def json_dumps_ne(json_struct, default='', indent=0, sort_keys=False):
    """Summary

    Args:
        json_struct (TYPE): Description
        default (str, optional): Description
        indent (int, optional): Description
        sort_keys (bool, optional): Description

    Returns:
        TYPE: Description
    """
    error, result = json_dumps(json_struct, default, indent, sort_keys)

    return result


def json_dumps(json_struct, default='', indent=0, sort_keys=False):
    """Summary

    Args:
        json_struct (TYPE): Description
        default (str, optional): Description
        indent (int, optional): Description
        sort_keys (bool, optional): Description

    Returns:
        TYPE: Description
    """
    error = None
    result = ''
    try:
        result = json.dumps(json_struct)
    except Exception as e:
        error = Error(S_ERR, 'unable to json_dumps: json_struct: %s e: %s' % (json_struct, e))
        result = default

    return error, result


def json_loads_ne(json_str, default=None):
    """Summary

    Args:
        json_str (TYPE): Description
        default (None, optional): Description

    Returns:
        TYPE: Description
    """
    error, result = json_loads(json_str, default)

    return result


def json_loads(json_str, default=None):
    """Summary

    Args:
        json_str (TYPE): Description
        default (None, optional): Description

    Returns:
        TYPE: Description
    """
    if default is None:
        default = {}

    error = None
    result = default

    try:
        result = json.loads(json_str)
    except Exception as e:
        error = Error(S_ERR, 'unable to json_loads: json_str: %s e: %s' % (json_str, e))
        result = default

    return error, result
