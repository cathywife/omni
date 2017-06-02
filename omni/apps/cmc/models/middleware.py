# -*- coding:utf8 -*-
"""
Created on 16/9/27 下午5:02
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

from django.db import models

from omni.libs.django.model.common import CreateUpdateDateTimeCommonModelMixin


"""tengine goproxy """


class TengineModel(models.Model):
    """
    salt配置
    """
    name = models.CharField(CreateUpdateDateTimeCommonModelMixin, unique=True, max_length=100, help_text='SaltState名称')
    description = models.CharField(max_length=4096, help_text='配置描述')

    class Meta:
        db_table = 'cmc_config_saltstate'

