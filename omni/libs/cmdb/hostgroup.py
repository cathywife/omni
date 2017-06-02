# -*- coding:utf8 -*-
"""
Created on 16/6/11 下午1:55
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

from . import cmdb_client, cmdb_result_parse
from cmdblib.client import RequestFailException
from .mapping import get_appid_for_hostgroup

import re
import logging
import time

log = logging.getLogger(__name__)


hostgroup_schema = 'rl_set_hosts'
gray_hostgroup_schema = 'rl_group_hosts'


def mget_gray_hostgroup(hostgroup):
    """
    获取灰度主机组信息
    :param hostgroup:
    :return:
    """
    try:
        entity_obj_list = cmdb_client.search_entities_by_query(query='_type: {0} AND name: {1}* AND env: prod'.format(
            gray_hostgroup_schema, hostgroup),  size=100000000000)
    except RequestFailException as e:
        if not e.message.split()[2] == '404':
            raise RequestFailException(e.message)
        entity_obj_list = []
    return [entity_obj for entity_obj in entity_obj_list if re.match(r'{0}(-\d{{1,3}})?'.format(hostgroup), entity_obj.name)]


def mget_all_hostgroup(page=1, size=10):
    """
    获取所有的主机组
    :return:
    """
    try:
        entity_obj_list = cmdb_client.search_entities(schema=hostgroup_schema, size=size, page=page)
    except RequestFailException as e:
        if not e.message.split()[2] == '404':
            raise RequestFailException(e.message)
        entity_obj_list = []
    return entity_obj_list


def get_hostgroup_by_name(name):
    """
    获取泳道主机组
    :param name: 泳道主机组名
    :return:
    """
    try:
        entity_obj = cmdb_client.get_entity(schema=hostgroup_schema, entity_key=name)
    except RequestFailException as e:
        if not e.message.split()[2] == '404':
            raise RequestFailException(e.message)
        entity_obj = None
    return entity_obj


def get_hosts_for_hostgroup(name):
    """
    获取泳道主机组主机列表
    :param name: 泳道主机组名
    :return:
    """
    hostgroup_obj = get_hostgroup_by_name(name)
    if hostgroup_obj:
        hosts = hostgroup_obj.hosts
    else:
        hosts = list()
    return hosts


def search_hostgroup_by_name(name, page=1, size=10):
    """
    搜索主机组
    :return:
    """
    try:
        entity_obj_list = cmdb_client.search_entities_by_query(query='_type: {0} AND name: {1}'.format(
            hostgroup_schema, name),  page=page, size=size)
    except RequestFailException as e:
        if not e.message.split()[2] == '404':
            raise RequestFailException(e.message)
        entity_obj_list = []
    return entity_obj_list


def add_hosts_for_hostgroup(name, hosts):
    """
    增加主机至主机组
    :param name: 主机组名
    :param hosts: 增加的主机列表
    :return:
    """

    hostgroup_obj = get_hostgroup_by_name(name)
    if not hostgroup_obj:
        return None

    hostgroup_obj.hosts.extend(hosts)
    result = cmdb_client.save_entity(hostgroup_obj)
    return cmdb_result_parse(result)


def del_hosts_for_hostgroup(name, hosts):
    """
    从主机组删除主机
    :param name: 主机组名
    :param hosts: 删除的主机列表
    :return:
    """

    hostgroup_obj = get_hostgroup_by_name(name)
    if not hostgroup_obj:
        return None

    [hostgroup_obj.hosts.remove(host) for host in hosts if host in hostgroup_obj.hosts]
    result = cmdb_client.save_entity(hostgroup_obj)
    return cmdb_result_parse(result)


def add_gray_hostgroup(name, appid_list, hosts, env):
    """
    创建灰度主机组
    :param name:
    :param appid_list:
    :param hosts:
    :param env:
    :return:
    """
    add_result = {'result': True, 'msg': '', 'task_id': list()}
    idc = name.split('-')[0]
    for appid in appid_list:
        gray_hg_info = {'name': name, 'app_id': appid, 'idc_code': idc, 'env': env,
                        'guid': '::'.join([appid, env, idc, name]), 'hosts': hosts}
        gray_hg_obj = cmdb_client.create_entity(gray_hostgroup_schema).from_json(gray_hg_info)
        result = cmdb_result_parse(cmdb_client.save_entity(gray_hg_obj))
        add_result['result'] = result['result']
        add_result['msg'] = result['msg']
        add_result['task_id'].append(result['task_id'])
        if not result['result']:
            add_result['msg'] = '创建灰度分组"{0}"失败, AppID: "{1}", hosts: "{2}"'.format(name, appid, hosts)
            return add_result
    add_result['msg'] = '灰度分组"{0}"已创建成功'.format(name)
    return add_result


def rebuild_gray_for_hostgroup(name):
    """
    对泳道主机组重新创建灰度组
    :param name:
    :return:
    """
    add_result = {'result': True, 'msg': '', 'task_id': list()}
    hostgroup_obj = get_hostgroup_by_name(name)
    if not hostgroup_obj:
        return None

    time.sleep(3)
    appid_list = get_appid_for_hostgroup(name)

    gray_hostgroup_obj_list = mget_gray_hostgroup(name)

    new_gray_host_info = dict()
    if len(hostgroup_obj.hosts) == 1:
        new_gray_host_info['{0}-1'.format(name)] = hostgroup_obj.hosts
    elif len(hostgroup_obj.hosts) <= 5:
        new_gray_host_info['{0}-1'.format(name)] = hostgroup_obj.hosts[:1]
        new_gray_host_info['{0}-2'.format(name)] = hostgroup_obj.hosts[1:]
    else:
        new_gray_host_info['{0}-1'.format(name)] = hostgroup_obj.hosts[:1]
        if hostgroup_obj.hosts[1:int(round(len(hostgroup_obj.hosts) * 0.2))]:
            new_gray_host_info['{0}-2'.format(name)] = hostgroup_obj.hosts[1:int(round(len(hostgroup_obj.hosts) * 0.2))]
            new_gray_host_info['{0}-3'.format(name)] = hostgroup_obj.hosts[int(round(len(hostgroup_obj.hosts) * 0.2)):]
        else:
            new_gray_host_info['{0}-2'.format(name)] = [hostgroup_obj.hosts[1]]
            new_gray_host_info['{0}-3'.format(name)] = hostgroup_obj.hosts[2:]

    # 删除多余的分组
    for gray_hg_obj in gray_hostgroup_obj_list:
        if gray_hg_obj.name in new_gray_host_info.keys():
            gray_hg_obj.hosts = new_gray_host_info[gray_hg_obj.name]
        else:
            gray_hg_obj.hosts = list()

        result = cmdb_result_parse(cmdb_client.save_entity(gray_hg_obj))
        add_result['result'] = result['result']
        add_result['msg'] = result['msg']
        add_result['task_id'].append(result['task_id'])
        if not result['result']:
            return add_result

    # 删除与已解除映射关系的AppId的相关灰度组
    for gray_hg_obj in gray_hostgroup_obj_list:
        if gray_hg_obj.app_id not in appid_list:
            # gray_hg_obj.app_id = '__scrap__{0}'.format(gray_hg_obj.app_id)
            gray_hg_obj.hosts = []
            gray_hg_obj.name = '__scrap__{0}'.format(gray_hg_obj.name)
            result = cmdb_result_parse(cmdb_client.save_entity(gray_hg_obj))
            add_result['result'] = result['result']
            add_result['msg'] = result['msg']
            add_result['task_id'].append(result['task_id'])
            if not result['result']:
                return add_result

    for gray_hg_name in [gray_hg_name for gray_hg_name in new_gray_host_info.keys()
                         if gray_hg_name not in [g_obj.name for g_obj in gray_hostgroup_obj_list]]:
        result = add_gray_hostgroup(gray_hg_name, appid_list, new_gray_host_info[gray_hg_name], 'prod')
        add_result['result'] = result['result']
        add_result['msg'] = result['msg']
        add_result['task_id'].extend(result['task_id'])
        if not result['result']:
            return add_result

    add_result['msg'] = '主机组"{0}"的灰度分组已重建成功!!'.format(name)
    return add_result


