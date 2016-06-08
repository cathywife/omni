# -*- coding:utf8 -*-
"""
Created on 15-10-3 下午2:36
@author: FMC
"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, \
    unicode_literals

from django.db import models
from omni.libs.django.field import list_fields


class ServerPowerModelModel(models.Model):
    """
    电源型号数据模型
    """
    model = models.SmallIntegerField(help_text='型号')
    description = models.CharField(blank=True, null=True, max_length=1024, help_text='详细描述')
    cpn = list_fields.ListCommaSeparatedStringField(blank=True, null=True, max_length=2048,
                                                    help_text='兼容服务器型号(Compatible Part Number)')
    version = models.CharField(max_length=20, help_text='电源版本')
    input_voltage_min = models.SmallIntegerField(help_text='最小输入电压(V)')
    input_voltage_max = models.SmallIntegerField(help_text='最大输入电压(V)')
    rated_power = models.SmallIntegerField(help_text='额定功率(W)')
    type = models.CharField(max_length=10, help_text='电源类型')
    other = models.CharField(max_length=2048, help_text='其他参数描述')
    lc_aging = models.IntegerField(help_text='老龄阈值(Days)')

    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    class Meta:
        db_table = 'asset_server_disk_model'


class ServerPowerAssetModel(models.Model):
    """
    电源资产
    """
    asset_id = models.CharField(max_length=30, help_text='资产ID, SERVER-Power-000001')
    description = models.CharField(blank=True, null=True, max_length=1024, help_text='详细描述')
    sn = models.CharField(max_length=30, help_text='SN编号')
    pn = models.CharField(blank=True, null=True, max_length=30, help_text='零件号(Part Number)')
    model = models.SmallIntegerField(help_text='电源型号')
    is_standard = models.BooleanField(help_text='是否为服务器标配')
    server = models.CharField(blank=True, null=True, max_length=30, help_text='所属服务器')
    slot = models.SmallIntegerField(help_text='位于服务器主板中的插槽编号')
    distributor = models.SmallIntegerField(help_text='经销商')
    lc = models.SmallIntegerField(help_text='当前生命周期')

    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    def __unicode__(self):
        return self.asset_id

    class Meta:
        db_table = 'asset_server_memory'
