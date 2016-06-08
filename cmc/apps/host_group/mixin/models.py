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
from omni.apps.host_group.models import HostGroupInfoModel
from omni.apps.host_group.base import BaseHostGroup
from omni.apps.host_node.mixin.template import HostNodeTemplateMixin


log = logging.getLogger(__name__)


class BaseHostGroupMixin(ByIdentityResourceBaseMixin):
    """
    获取主机组配置、数据等
    """
    model = HostGroupInfoModel
    host_group_node_cls = BaseHostGroup
    pk = None

    @classmethod
    def get_multi_host_group_full_context(cls, host_pk_list):
        """
        获取多个主机组的完整数据
        """
        full_context = {}
        for host_group_context in cls.get_multi_obj_context(pk_list=host_pk_list):
            host_group_full_context = {}

            [host_group_full_context.update(template_context) for template_context in
             HostNodeTemplateMixin.get_multi_obj_context(pk_list=host_group_context['template_list'])]

            host_group_full_context.update(host_group_context)
            full_context.update(host_group_full_context)

        return full_context

    def get_template_list(self):
        """
        获取所引用的所有模板
        :return:
        """
        if not self.obj_context['template_list']:
            self.obj_context = self.get_obj_context(pk=self.pk)
        return self.obj_context['template_list']

    def get_template_context(self):
        """
        获取所有template配置数据
        :return:
        """
        return HostNodeTemplateMixin.get_multi_obj_context(pk_list=self.get_template_list())