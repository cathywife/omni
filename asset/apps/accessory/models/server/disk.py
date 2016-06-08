# -*- coding:utf8 -*-
"""
Created on 15-10-2 下午8:38
@author: FMC
"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, \
    unicode_literals

from django.db import models


class ServerDiskModelModel(models.Model):
    """
    Disk 型号数据模型
    """
    model = models.SmallIntegerField(help_text='型号')
    description = models.CharField(blank=True, null=True, max_length=1024, help_text='详细描述')
    type = models.CharField(max_length=10, help_text='硬盘类型')
    size = models.SmallIntegerField(help_text='容量大小(MB)')
    rpm = models.IntegerField(help_text='转速(RPM)')
    interface_type = models.CharField(max_length=10, help_text='接口类型')
    interface_rate = models.IntegerField(help_text='接口速率(Mbps)')
    other = models.CharField(max_length=2048, help_text='其他参数描述')
    lc_aging = models.IntegerField(help_text='老龄阈值(Days)')

    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    class Meta:
        db_table = 'asset_server_disk_model'


class ServerDiskAssetModel(models.Model):
    """
    Disk 资产
    """
    asset_id = models.CharField(max_length=30, help_text='资产ID, SERVER-Disk-000001')
    description = models.CharField(blank=True, null=True, max_length=1024, help_text='详细描述')
    sn = models.CharField(max_length=30, help_text='SN编号')
    pn = models.CharField(max_length=30, help_text='零件号(Part Number)')
    model = models.SmallIntegerField(help_text='硬盘型号')
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
