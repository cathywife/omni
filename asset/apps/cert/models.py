# -*- coding:utf8 -*-
"""
Created on 2015年1月23日
    SSL服务
@author: FMC
"""
from __future__ import print_function, unicode_literals, division, absolute_import

from django.db import models


class CertRepo(models.Model):
    """
    证书仓库
    """
    path = models.FilePathField(max_length=300, help_text='证书仓库路径')
    service = models.CharField(max_length=30, help_text='Rpyc服务名称')
    description = models.CharField(blank=True, null=True, max_length=100, help_text='描述、说明信息')
    env = models.SmallIntegerField(help_text='所属运行环境')
    ip = models.IPAddressField(help_text='Rpyc服务监听地址')
    port = models.IntegerField(help_text='监听端口, 1-65535')
    ca = models.SmallIntegerField(help_text="证书库")
    cert = models.SmallIntegerField(help_text="服务器证书")

    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    class Meta:
        db_table = 'ssl_cert'

print(CertRepo.__getattribute__())
