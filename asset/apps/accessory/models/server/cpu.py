# -*- coding:utf8 -*-
"""
Created on 15-10-2 下午4:54
@author: FMC
"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, \
    unicode_literals

from django.db import models


class ServerCPUModelModel(models.Model):
    """
    CPU 型号数据模型
    """
    model = models.SmallIntegerField(help_text='型号名称')
    description = models.CharField(blank=True, null=True, max_length=1024, help_text='详细描述')
    cores = models.SmallIntegerField(help_text='CPU 核心数')
    frequency = models.FloatField(help_text='CPU 主频(GHz)')
    cache_l1 = models.SmallIntegerField(help_text='一级缓存容量(KB)')
    cache_l2 = models.SmallIntegerField(help_text='二级缓存容量(KB)')
    cache_l3 = models.SmallIntegerField(help_text='三级缓存容量(KB)')
    mem_type = models.SmallIntegerField(help_text='最高支持内存类型')
    mem_frequency = models.SmallIntegerField(help_text='最高支持的内存频率')
    tdp = models.SmallIntegerField(help_text='散热设计功耗(Watt)')
    other = models.CharField(max_length=2048, help_text='其他参数描述')
    lc_aging = models.IntegerField(help_text='CPU 老龄阈值(Days)')

    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    class Meta:
        db_table = 'asset_server_cpu_model'


class ServerCPUAssetModel(models.Model):
    """
    CPU 资产
    """
    asset_id = models.CharField(max_length=30, help_text='CPU 资产ID, SERVER-CPU-000001')
    description = models.CharField(blank=True, null=True, max_length=1024, help_text='详细描述')
    sn = models.CharField(max_length=20, help_text='SN编号')
    model = models.SmallIntegerField(help_text='CPU型号')
    is_standard = models.BooleanField(help_text='是否为服务器标配')
    server = models.CharField(blank=True, null=True, max_length=30, help_text='所属服务器')
    slot = models.SmallIntegerField(help_text='CPU 位于服务器主板中的插槽编号')
    distributor = models.SmallIntegerField(help_text='经销商')
    lc = models.SmallIntegerField(help_text='当前生命周期')

    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    def __unicode__(self):
        return self.asset_id

    class Meta:
        db_table = 'asset_server_cpu'
