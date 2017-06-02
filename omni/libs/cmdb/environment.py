# -*- coding:utf8 -*-
"""
Created on 16/10/24 上午1:18
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, \
    unicode_literals

from . import cmdb_client
from cmdblib.client import RequestFailException

import logging

log = logging.getLogger(__name__)


idc_info_schema = 'idc'
env_info_scheam = 'dict_env'


def mget_all_env():
    """
    获取所有环境信息
    :return:
    """
    try:
        entity_obj_list = cmdb_client.search_entities(schema=env_info_scheam, page=1, size=100000000)
    except RequestFailException as e:
        if not e.message.split()[2] == '404':
            raise RequestFailException(e.message)
        entity_obj_list = []
    return entity_obj_list


def mget_all_idc():
    """
    获取所有IDC信息
    :return:
    """
    try:
        entity_obj_list = cmdb_client.search_entities(schema=idc_info_schema, page=1, size=100000000)
    except RequestFailException as e:
        if not e.message.split()[2] == '404':
            raise RequestFailException(e.message)
        entity_obj_list = []
    return entity_obj_list




