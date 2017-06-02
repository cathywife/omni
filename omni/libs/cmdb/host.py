# -*- coding:utf8 -*-
"""
Created on 16/8/17 上午1:05
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

from . import cmdb_client
from cmdblib.client import RequestFailException

import logging

log = logging.getLogger(__name__)


server_logic_schema = 'server_logic'
server_model_schema = 'dict_conf_model'
server_life_cycle_schema = 'dict_srv_useStatus'


def get_host(name):
    """
    获取逻辑服务器主机信息
    :param name: 主机名
    :return:
    """
    try:
        entity_obj_list = cmdb_client.search_entities(schema=server_logic_schema, hostname=name)
    except RequestFailException as e:
        if not e.message.split()[2] == '404':
            raise RequestFailException(e.message)
        entity_obj_list = None
    return entity_obj_list[0]


def mget_all_host():
    """
    获取所有服务器
    :return:
    """
    try:
        entity_obj_list = cmdb_client.search_entities(schema=server_logic_schema, page=1, size=100000000)
    except RequestFailException as e:
        if not e.message.split()[2] == '404':
            raise RequestFailException(e.message)
        entity_obj_list = []
    return entity_obj_list


def mget_all_host_model():
    """
    获取所有主机型号
    :return:
    """
    try:
        entity_obj_list = cmdb_client.search_entities(schema=server_model_schema, page=1, size=100000000)
    except RequestFailException as e:
        if not e.message.split()[2] == '404':
            raise RequestFailException(e.message)
        entity_obj_list = []
    return entity_obj_list


def mget_all_host_life_cycle_status():
    """
    获取主机所有生命周期状态
    :return:
    """
    try:
        entity_obj_list = cmdb_client.search_entities(schema=server_life_cycle_schema, page=1, size=100000000)
    except RequestFailException as e:
        if not e.message.split()[2] == '404':
            raise RequestFailException(e.message)
        entity_obj_list = []
    return entity_obj_list

