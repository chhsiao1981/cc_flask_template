# -*- coding: utf-8 -*-

from {{cookiecutter.project}}.constants import S_OK, S_ERR

import uuid
import base64
import itertools


from {{cookiecutter.project}}.utils.util_error import Error


def gen_random_string():
    """Summary

    Returns:
        TYPE: Description
    """
    return base64.urlsafe_b64encode(uuid.uuid4().bytes)[:22].decode('utf-8')


def flatten(the_list_block):
    """flatten list of list to list

    Args:
        the_list_block ([[]]): list of list

    Returns:
        (list): list
    """
    return list(itertools.chain.from_iterable(the_list_block))


def flatten_results_with_error(results_with_error):
    """flatten results with error

    Args:
        results_with_error ([(Error, result)]): results with error

    Returns:
        (Error, [result]): error, results
    """
    error_msg_list = []
    results = []
    for idx, (each_error, each_result) in enumerate(results_with_error):
        if each_error:
            error_msg_list.append('(%s/%s) e: %s' % (idx, len(results_with_error), each_error))
        results.append(each_result)

    error = None if not error_msg_list else Error(S_ERR, ','.join(error_msg_list))
    if error:
        return error, results

    return None, results
