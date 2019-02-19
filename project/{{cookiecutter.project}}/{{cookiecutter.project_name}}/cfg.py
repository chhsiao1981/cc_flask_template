# -*- coding: utf-8 -*-

from configparser import SafeConfigParser
import logging
import logging.config
import random
import math
import base64
import time
import pymongo
from pymongo import MongoClient
import ujson as json
import copy
import re

_LOGGER_NAME = "{{cookiecutter.project_name}}"
logger = None
config = {
}

_mongo_map = {
    'test': 'test',
}

_flask_mongo_map = {
    'user': 'user',
}

_ensure_index = {
}

_ensure_unique_index = {
}

IS_INIT = False


def init(params):
    '''
    params: log_ini_filename
            ini_filename
    '''
    global IS_INIT
    if IS_INIT:
        return

    IS_INIT = True

    _init_logger(params)
    _init_ini_file(params)
    _post_init_config(params)

    _init_process_list()

    # _init_mongo()

    # _init_redis()

    logger.warning('config: %s', config)


def _init_logger(params):
    '''logger'''
    global logger
    logger = logging.getLogger(_LOGGER_NAME)

    log_ini_filename = params.get('log_ini_filename', '')
    if not log_ini_filename:
        log_ini_filename = params.get('ini_filename', '')

    if not log_ini_filename:
        return

    logging.config.fileConfig(log_ini_filename, disable_existing_loggers=False)


def _init_ini_file(params):
    '''
    setup {{cookiecutter.project_name}}:main config
    '''
    global config

    ini_filename = params.get('ini_filename', '')

    section = '{{cookiecutter.project_name}}:main'

    config = init_ini_file(ini_filename, section)


def init_ini_file(ini_filename, section):
    '''
    get ini conf from section
    return: config: {key: val} val: json_loaded
    '''
    config_parser = SafeConfigParser()
    config_parser.read(ini_filename)
    options = config_parser.options(section)
    config = {option: _init_ini_file_parse_option(option, section, config_parser) for option in options}
    _post_json_config(config)

    return config


def _init_ini_file_parse_option(option, section, config_parser):
    try:
        val = config_parser.get(section, option)
    except Exception as e:
        logger.exception('unable to get option: section: %s option: %s e: %s', section, option, e)
        val = ''
    return val


def _post_json_config(config):
    '''
    try to do json load on value
    '''
    for k, v in config.items():
        if v.__class__.__name__ != 'str':
            continue

        orig_v = v
        try:
            config[k] = json.loads(v)
        except:
            config[k] = orig_v

        if re.search(r'_set$', k) and type(v) == list:
            config[k] = set(v)


def _post_init_config(params):
    '''
    add additional parameters into config
    '''
    logger.info('params: %s', params)

    for (k, v) in params.items():
        if k in config:
            logger.warning('params will be overwrite: key: %s origin: %s new: %s', k, config[k], v)

    config.update(params)

    config['data'] = {}


def _init_mongo(db_name=None):
    '''
    initialize mongo
    '''

    _init_mongo_map_core(
        'mongo',
        config.get('mongo_server_hostname', 'localhost'),
        config.get('mongo_server', 'test'),
        _mongo_map,
        _ensure_index,
        _ensure_unique_index,
        db_name=db_name)

    _init_mongo_map_core(
        'flask_mongoengine',
        config.get('flask_mongoengine_host', 'localhost'),
        config.get('flask_mongoengine_server', 'flask_mongoengine'),
        _flask_mongo_map,
        None,
        None,
        db_name=db_name)


def _init_mongo_map_core(mongo_prefix, mongo_server_hostname, mongo_server, mongo_map, ensure_index_map=None, ensure_unique_index_map=None, db_name=None):
    if db_name is not None and db_name not in mongo_map:
        return

    if ensure_index_map is None:
        ensure_index_map = {}

    if ensure_unique_index_map is None:
        ensure_unique_index_map = {}

    mongo_server_url = mongo_prefix + '_MONGO_SERVER_URL'
    mongo_server_idx = mongo_prefix + '_MONGO_SERVER'

    # mongo_server_url
    if mongo_server_url not in config:
        config[mongo_server_url] = "mongodb://" + mongo_server_hostname + "/" + mongo_server

    try:
        if mongo_server_idx not in config:
            config[mongo_server_idx] = MongoClient(config.get(mongo_server_url))[mongo_server]

        for (key, val) in mongo_map.items():
            if key in config:
                logger.warning('key already in config: key: %s config: %s', key, config[key])
                continue

            logger.info('mongo: %s => %s', key, val)
            config[key] = config.get(mongo_server_idx)[val]
    except Exception as e:
        logger.error('unable to init mongo: mongo_prefix: %s mongo_server_hostname: %s mongo_server: %s e: %s', mongo_prefix, mongo_server_hostname, mongo_server, e)

        for key, val in mongo_map.items():
            config[key] = None

    for key, val in ensure_index_map.items():
        logger.info('to ensure_index: key: %s', key)
        try:
            config[key].ensure_index(val, background=True)
        except Exception as e:
            logging.error('unable to ensure_index: key: %s e: %s', key, e)

    for key, val in ensure_unique_index_map.items():
        logger.info('to ensure_unique_index: key: %s', key)
        try:
            config[key].ensure_index(val, background=True, unique=True)
        except Exception as e:
            logging.error('unable to ensure unique index: key: %s e: %s', key, e)
