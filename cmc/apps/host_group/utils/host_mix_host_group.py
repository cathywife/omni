# !/usr/bin/env python
# -*- coding:utf8 -*-
"""
Created on 2015年1月21日
    节点组基本模块
@author: FMC
"""
from __future__ import print_function, unicode_literals, division, absolute_import

import logging
from omni.apps.host_group.models import HostRelateHostGroupModel

log = logging.getLogger(__name__)


def get_host_group_by_host(env_pk, host_pk):
    """
    依据指定run_env和主机节点pk,返回所有相关主机组
    :param host_pk:
    :return: list
    """
    host_group_list = []
    for m in HostRelateHostGroupModel.objects.filter(env=env_pk, host=host_pk):
        host_group_list.append(m.group)

    return host_group_list


def get_host_by_host_group(run_env, host_group_pk):
    """
    依据指定run_env和主机组pk,返回所有相关主机节点
    :param host_group_pk:
    :return: list
    """
    host_list = []
    for m in HostRelateHostGroupModel.objects.filter(env=run_env, group=host_group_pk):
        host_list.append(m.host)

    return host_list
