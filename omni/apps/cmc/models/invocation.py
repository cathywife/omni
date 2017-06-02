# -*- coding:utf8 -*-
"""
Created on 16/9/27 下午5:03
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

from django.db import models

from omni.libs.django.model.common import CreateUpdateDateTimeCommonModelMixin


class InvocationModel(CreateUpdateDateTimeCommonModelMixin, models.Model):
    """
    APPID及组件间调用链
    """
    appid_a = models.IntegerField(help_text='调用方AppID')
    appid_b = models.IntegerField(help_text='被调用方AppID')
    middleware = models.IntegerField(help_text='中间件')
    port_b = models.IntegerField(help_text='连接端口(当存在多端口时)')
    description = models.CharField(max_length=4096, help_text='配置描述')

    class Meta:
        db_table = 'cmc_invocation'
