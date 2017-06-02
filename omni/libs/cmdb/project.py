# -*- coding:utf8 -*-
"""
Created on 16/6/9 上午11:15
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

from . import cmdb_client

project_schema = 'dict_project'
server_logic_schema = 'server_logic'
app_id_schema = 'app'
project_rl_channel_schema = 'rl_project_channel'


def mget_by_userid(user_id=None):
    """
    获取有权限的项目列表
    :return:
    """
    if user_id:
        return cmdb_client.search_entities(schema=project_schema, user_id=user_id)
    else:
        return cmdb_client.search_entities(schema=project_schema)


def get(name):
    """
    查询项目信息
    """
    return cmdb_client.get_entity(schema=project_schema, name=name)


def mget_server(project_name, page=1, size=10, **kwargs):
    """
    获取属于本项目的服务器信息
    :param project_name: 项目名称
    :return:
    """
    return cmdb_client.search_entities(schema=server_logic_schema, project=project_name, page=page, size=size, **kwargs)


def mget_app_id(project_name, page=1, size=10, **kwargs):
    """
    获取属于本项目的app_id信息
    :param project_name: 项目名称
    :param page:
    :param size:
    :param kwargs: 其他filed过滤信息
    :return:
    """
    return cmdb_client.search_entities(schema=app_id_schema, prj_name=project_name, page=page, size=size, **kwargs)


def mget_channel(project_name, page=1, size=10, **kwargs):
    """
    获取项目所拥有的泳道及相关app_id
    :param project_name: 项目名称
    :return:
    """
    return cmdb_client.search_entities(schema=project_rl_channel_schema, project=project_name, page=page, size=size,
                                       **kwargs)

