#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
Created on 2015年2月11日
    主机管理节点Mixin模块
@author: FMC
"""
from __future__ import print_function, unicode_literals, division, absolute_import


from omni.apps.arch.mixin.models import BaseHostNodeMixin
from omni.apps.arch.management import ManagementNode


class ManagementNodeMixin(BaseHostNodeMixin):
    cls = ManagementNode