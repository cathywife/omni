# -*- coding:utf8 -*-
"""
Created on 15-10-2 下午7:20
@author: FMC
"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, \
    unicode_literals


from django.db import models


class ServerMemoryModelModel(models.Model):
    """
    Memory 型号数据模型
    """
    model = models.SmallIntegerField(help_text='型号')    # 对应asset_facilitator_manufacturer_product表
    description = models.CharField(blank=True, null=True, max_length=1024, help_text='详细描述')
    size = models.SmallIntegerField(help_text='容量大小(MB)')
    frequency = models.FloatField(help_text='内存频率(MHz)')
    type = models.CharField(max_length=10, help_text='内存类型')
    other = models.CharField(max_length=2048, help_text='其他参数描述')
    lc_aging = models.IntegerField(help_text='老龄阈值(Days)')

    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    class Meta:
        db_table = 'asset_server_memory_model'


class ServerMemoryAssetModel(models.Model):
    """
    Memory 资产
    """
    asset_id = models.CharField(max_length=30, help_text='资产ID, SERVER-Memory-000001')
    description = models.CharField(blank=True, null=True, max_length=1024, help_text='详细描述')
    sn = models.CharField(max_length=20, help_text='SN编号')
    model = models.SmallIntegerField(help_text='内存型号')
    is_standard = models.BooleanField(help_text='是否为服务器标配')
    server = models.CharField(blank=True, null=True, max_length=30, help_text='所属服务器')
    slot = models.SmallIntegerField(help_text='内存位于服务器主板中的插槽编号')
    distributor = models.SmallIntegerField(help_text='经销商')
    lc = models.SmallIntegerField(help_text='当前生命周期')

    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    def __unicode__(self):
        return self.asset_id

    class Meta:
        db_table = 'asset_server_memory'
