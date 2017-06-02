# -*- coding:utf8 -*-
"""
Created on 16/6/11 下午1:07
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

from . import cmdb_client

channel_schema = 'channel'
channel_rl_hostgroup_schema = 'rl_channel_hosts'


def get(name):
    """
    获取泳道信息
    :param name:
    :return:
    """
    return cmdb_client.get_entity(schema=channel_schema, entity_key=name)


def mget(page=1, size=10):
    """
    获取所有泳道
    :return: list
    """
    return cmdb_client.get_entities(schema=channel_schema, page=page, size=size)


def mget_hostgroup(channel_name, page=1, size=10, **kwargs):
    """
    获取与channel_name泳道相关的所有主机组
    :param channel_name:
    :return:
    """
    return cmdb_client.search_entities(schema=channel_rl_hostgroup_schema, name=channel_name, page=page, size=size,
                                       **kwargs)



