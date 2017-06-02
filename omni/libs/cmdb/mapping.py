# -*- coding:utf8 -*-
"""
Created on 16/8/18 下午1:57
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

from . import cmdb_client, cmdb_result_parse
from cmdblib.client import RequestFailException


import logging

log = logging.getLogger(__name__)


hostgroup_schema = 'rl_set_hosts'
hostgroup_rl_appid_schema = 'rl_set_appid'
gray_hostgroup_schema = 'rl_group_hosts'


def get_appid_for_hostgroup(name, page=1, size=100000000000):
    """
    获取泳道主机组所关联的app_id
    :param name:
    :param page:
    :param size:
    :return:
    """
    try:
        entity_obj_list = cmdb_client.search_entities(schema=hostgroup_rl_appid_schema, hosts_set_name=name,
                                                      size=size, page=page)
        log.info('查询与主机组"{0}"关联的所有AppId'.format(name))
    except RequestFailException as e:
        if not e.message.split()[2] == '404':
            raise RequestFailException(e.message)
        entity_obj_list = []
    app_id_list = list(set([entity_obj.app_id for entity_obj in entity_obj_list]))
    return app_id_list


def add_hostgroup_rl_appid(appid, hostgroup):
    """
    增加APPID与hostgroup的映射关系
    :param appid:
    :param hostgroup:
    :return:
    """
    new_rl_obj = cmdb_client.create_entity(hostgroup_rl_appid_schema).from_json({
        'app_id': appid,
        'hosts_set_name': hostgroup,
        'guid': '::'.join([appid, hostgroup])
    })
    result_info = cmdb_client.save_entity(new_rl_obj)

    return cmdb_result_parse(result_info)


def del_hostgroup_rl_appid(appid, hostgroup):
    """
    解除APPID与hostgroup的映射关系
    :param appid:
    :param hostgroup:
    :return:
    """
    entity_obj_list = cmdb_client.search_entities(schema=hostgroup_rl_appid_schema, hosts_set_name=hostgroup,
                                                  app_id=appid)
    if len(entity_obj_list) > 0:
        entity_obj = entity_obj_list[0]
        entity_obj.app_id = ''
        entity_obj.hosts_set_name = ''
        result_info = cmdb_client.save_entity(entity_obj)
        return cmdb_result_parse(result_info)
    else:
        return {'result': True, 'msg': '主机组"{0}"与AppID "{1}" 不存在映射关系!!', 'http_status': 304, 'task_id': ''}





