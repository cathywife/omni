# -*- coding:utf8 -*-
"""
Created on 16/10/7 上午12:51
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, \
    unicode_literals

from django.db import models
from omni.libs.django.model.common import CreateUpdateDateTimeCommonModelMixin


class EnvModel(CreateUpdateDateTimeCommonModelMixin, models.Model):
    name = models.CharField(max_length=20, unique=True, help_text='运行环境名称,例如: test; prod')
    visible_name = models.CharField(blank=True, null=True, default='', max_length=30, help_text='显示名称,例如: 测试环境; 生产环境')
    description = models.CharField(blank=True, null=True, default='', max_length=512, help_text='详细描述、说明')

    class Meta:
        db_table = 'arch_env'

    def get_absolute_url(self):
        """
        返回访问对象的URI地址
        :return:
        """
        return '/restapi/envs/{0}'.format(self.pk)


class IDCModel(CreateUpdateDateTimeCommonModelMixin, models.Model):
    idc_code = models.CharField(max_length=10, unique=True, help_text='机房唯一标识')
    name = models.CharField(max_length=10, blank=True, default='', help_text='IDC 服务商的简称')
    desc = models.CharField(max_length=50, help_text='描述', default='', blank=True)
    address = models.CharField(blank=True, null=True, max_length=100, help_text='详细地址')
    contact = models.EmailField(blank=True, null=True, help_text='联系人')
    phone = models.CharField(blank=True, null=True, max_length=15, help_text='电话')
    bandwidth_type = models.CharField(blank=True, null=True, max_length=11, help_text='带宽及类型')
    remark = models.CharField(blank=True, null=True, max_length=13, help_text='备注')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'arch_idc'


class EzoneModel(CreateUpdateDateTimeCommonModelMixin, models.Model):
    name = models.CharField(max_length=10, unique=True, help_text='Ezone唯一标识')
    ezone_id = models.CharField(max_length=10, blank=True, default='', help_text='Ezone的编号')
    desc = models.CharField(max_length=50, help_text='描述', default='', blank=True)
    idc = models.ForeignKey(IDCModel, on_delete=models.SET_NULL, db_constraint=False)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'arch_ezone'



