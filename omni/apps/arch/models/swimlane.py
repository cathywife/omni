# -*- coding:utf8 -*-
"""
Created on 16/9/26 下午2:07
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

from django.db import models
from omni.libs.django.model.common import CreateUpdateDateTimeCommonModelMixin

from . import environment


class SwimlaneModel(CreateUpdateDateTimeCommonModelMixin, models.Model):
    """
    泳道信息表
    """
    env = models.ForeignKey(environment.EnvModel, on_delete=models.SET_NULL, db_constraint=False, help_text='运行环境ID')
    name = models.CharField(unique=True, max_length=100, help_text='泳道名称')
    visible_name = models.CharField(blank=True, max_length=30, help_text='显示名称')

    class Meta:
        db_table = 'arch_swimlane'

