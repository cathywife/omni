#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
Created on 2015年2月9日
    环境Mixin模块
@author: FMC
"""
from __future__ import print_function, unicode_literals, division, absolute_import

import logging
from omni.apps import ByIdentityResourceBaseMixin
from omni.apps.host_node.models import HostNodeTemplateModel

log = logging.getLogger(__name__)


class HostNodeTemplateMixin(ByIdentityResourceBaseMixin):
    """
    主机节点模板配置
    """
    model = HostNodeTemplateModel