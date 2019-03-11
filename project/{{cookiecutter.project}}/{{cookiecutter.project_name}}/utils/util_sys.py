# -*- coding: utf-8 -*-

import os
from subprocess import Popen

from {{cookiecutter.project_name}}.constants import *
from {{cookiecutter.project_name}} import cfg
from {{cookiecutter.project_name}}.utils.util_error import Error


def makedirs(dir_name):
    """Summary

    Args:
        dir_name (TYPE): Description

    Returns:
        TYPE: Description
    """
    error = None
    try:
        os.makedirs(dir_name)
    except Exception as e:
        if e.errno not in [errno.EEXIST]:  # dir already exists
            error = Error(S_ERR, 'unable to makedirs: dir_name: %s e: %s' % (dir_name, e))
            cfg.logger.error(error.message)

    return error


def process_cmd(cmd, is_stdout=True, is_stderr=True, is_wait=True):
    """Summary

    Args:
        cmd (TYPE): Description
        is_stdout (bool, optional): Description
        is_stderr (bool, optional): Description
        is_wait (bool, optional): Description

    Returns:
        TYPE: Description
    """
    error = None
    output_content = ''
    output_stderr = ''
    process = None

    the_stdout = PIPE if is_stdout else None
    the_stderr = PIPE if is_stderr else None
    try:
        process = Popen(cmd, stdout=the_stdout, stderr=the_stderr)

        if is_wait:
            (output_content, output_stderr) = process.communicate()
    except Exception as e:
        error = Error(S_ERR, 'unable to process cmd: cmd: %s e: %s' % (cmd, e))
        process = None
        output_content = ''
        output_stderr = ''

    return error, (process, output_content, output_stderr)
