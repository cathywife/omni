#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
Created on 2015年2月9日
    环境Mixin模块
@author: FMC
"""
from __future__ import print_function, unicode_literals, division, absolute_import

import logging
from omni.apps.host_node.models import HostNodeModel
from omni.apps.host_node.base import BaseHostNode
from omni.apps.host_group.mixin.models import BaseHostGroupMixin


log = logging.getLogger(__name__)


class BaseHostNodeMixin(BaseHostGroupMixin):
    """
    获取主机节点配置、数据等
    """
    model = HostNodeModel
    cls = BaseHostNode


