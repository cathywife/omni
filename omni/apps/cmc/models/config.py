# -*- coding:utf8 -*-
"""
Created on 16/9/27 下午4:59
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function


from django.db import models
from omni.libs.django.model.common import CreateUpdateDateTimeCommonModelMixin


class ConfigTypeModel(CreateUpdateDateTimeCommonModelMixin, models.Model):
    name = models.CharField(unique=True, max_length=20, verbose_name='名称', help_text='配置类型名称')
    description = models.CharField(max_length=1024, verbose_name='描述', help_text='针对配置类型的详细描述')

    class Meta:
        db_table = 'cmc_config_type'


class ConfigModel(CreateUpdateDateTimeCommonModelMixin, models.Model):
    """
    配置信息
    """
    name = models.CharField(unique=True, max_length=100, help_text='名称')
    config_type = models.ForeignKey(ConfigTypeModel, on_delete=models.SET_NULL, db_constraint=False,
                                    verbose_name='配置类型', help_text='选择配置类型')
    operation = models.CharField(max_length=2048, help_text='操作')
    description = models.CharField(max_length=4096, help_text='配置描述')
    params = models.CharField(max_length=4096, help_text='参数')

    class Meta:
        db_table = 'cmc_config_eoc'
