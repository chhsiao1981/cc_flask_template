# -*- coding: utf-8 -*-


def _str(item, encoding='utf-8', default=''):
    """_str

    Args:
        item (Any): item
        encoding (str, optional): encoding
        default (str, optional): default

    Returns:
        str: item in str type.
    """
    if isinstance(item, bytes):
        try:
            result = item.decode(encoding)
        except Exception as e:
            result = default
        return result

    try:
        result = str(item)
    except Exception as e:
        result = default
    return result


def _unicode(item, encoding='utf-8', default=''):
    """_unicode

    Args:
        item (Any): item
        encoding (str, optional): encoding
        default (str, optional): default

    Returns:
        str: item in str type
    """
    if isinstance(item, str):
        return item

    return _str(item, encoding=encoding, default=default)


def _int(item, default=0):
    """_int

    Args:
        item (Any): item
        default (int, optional): default

    Returns:
        int: item in int type
    """
    if isinstance(item, int):
        return item

    if item == 'null':
        return 0

    if item == 'false':
        return 0

    if item == 'true':
        return 1

    result = default
    try:
        result = int(item)
    except Exception as e:
        # cfg.logger.error('unable to _int: item: %s, default: %s e: %s', item, default, e)
        result = default

    return result


def _float(item, default=0.0):
    """_float

    Args:
        item (Any): item
        default (float, optional): default

    Returns:
        float: item in float type
    """
    if isinstance(item, float):
        return item

    if item == 'null':
        return 0.0

    if item == 'false':
        return 0.0

    if item == 'true':
        return 1.0

    result = default
    try:
        result = float(item)
    except Exception as e:
        # cfg.logger.error('unable to _float: item: %s, default: %s e: %s', item, default, e)
        result = default

    return result


def _bool(item):
    """_bool

    Args:
        item (Any): item

    Returns:
        bool: item in bool type
    """
    if item == True:
        return True

    if item == False:
        return False

    if item == 'true':
        return True

    if item == 'True':
        return True

    if item == 'false':
        return False

    if item == 'False':
        return False

    return False if not item else True
