#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-07-26 11:04:34
import logging
import hashlib


def get_logger(name):
    """

     Returns:
            logging.RootLogger: 用户对象
    """
    logger = logging.getLogger(name)

    try:
        while logger.handlers.pop():
            continue
    except IndexError:
        pass

    handler = logging.StreamHandler()
    formater = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formater)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger


def md5encode(value):
    m = hashlib.md5()
    m.update(value)
    return m.hexdigest()