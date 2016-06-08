# -*- coding:utf8 -*-
"""
Created on 15-10-3 下午12:49
@author: FMC
"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, \
    unicode_literals

from django.db import models


class IDCModel(models.Model):
    name = models.CharField(max_length=10, unique=True, help_text='IDC 服务商的简称,或中文名称的首字母组合')
    full_name = models.CharField(max_length=50, help_text='服务商全称')
    Manufacturer = models.SmallIntegerField(help_text='所属厂商')
    province = models.CharField(max_length=15, help_text='所在省份')
    city = models.CharField(max_length=15, help_text='所在城市')
    county = models.CharField(blank=True, null=True, max_length=15, help_text='所在县')
    district = models.CharField(blank=True, null=True, max_length=15, help_text='所在区、乡、镇')
    detail_address = models.CharField(blank=True, null=True, max_length=100, help_text='详细地址，但不包括省、市、县、区级别')
    email = models.EmailField(blank=True, null=True, help_text='邮件地址')
    qq = models.CharField(blank=True, null=True, max_length=15, help_text='QQ号码')
    mobile = models.CharField(blank=True, null=True, max_length=11, help_text='手机号码')
    tel_num = models.CharField(blank=True, null=True, max_length=13, help_text='电话号码')

    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'asset_facilitator_'


class DistributorModel(models.Model):
    name = models.CharField(max_length=10, unique=True, help_text='经销商的公司简称或中文名称首字母组合')
    full_name = models.CharField(max_length=50, help_text='经销商公司全称')
    province = models.CharField(blank=True, null=True, max_length=15, help_text='公司所在省份')
    city = models.CharField(blank=True, null=True, max_length=15, help_text='公司所在province的城市')
    county = models.CharField(blank=True, null=True, max_length=15, help_text='所在县')
    district = models.CharField(blank=True, null=True, max_length=15, help_text='所在区、乡、镇')
    detail_address = models.CharField(blank=True, null=True, max_length=100, help_text='详细地址，但不包括省、市、县、区级别')
    email = models.EmailField(blank=True, null=True, help_text='邮件地址')
    qq = models.CharField(blank=True, null=True, max_length=15, help_text='QQ号码')
    mobile = models.CharField(blank=True, null=True, max_length=11, help_text='手机号码')
    tel_num = models.CharField(blank=True, null=True, max_length=13, help_text='电话号码')

    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'asset_facilitator_distributor'


class ContactModel(models.Model):
    name = models.CharField(max_length=15, help_text='姓名')
    sex = models.BooleanField(default=True, help_text='性别,True：男,False：女')
    position = models.CharField(blank=True, null=True, max_length=15, help_text='职位名称')
    belong_type = models.CharField(max_length=10, help_text='属于组织类型，例如: IDC,Distributor等表名')
    belong_to = models.SmallIntegerField(help_text='组织表主键ID')
    email = models.EmailField(blank=True, null=True, help_text='邮件地址')
    qq = models.CharField(blank=True, null=True, max_length=15, help_text='QQ号码')
    mobile = models.CharField(blank=True, null=True, max_length=11, help_text='手机号码')
    tel_num = models.CharField(blank=True, null=True, max_length=13, help_text='电话号码')

    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'asset_facilitator_contact'


class ManufacturerModel(models.Model):
    name = models.CharField(max_length=10, unique=True, help_text='生产厂商的简称或中文名称首字母组合')
    full_name = models.CharField(max_length=50, help_text='生产厂商公司全称')
    province = models.CharField(blank=True, null=True, max_length=15, help_text='公司所在省份')
    city = models.CharField(blank=True, null=True, max_length=15, help_text='公司所在province的城市')
    county = models.CharField(blank=True, null=True, max_length=15, help_text='所在县')
    district = models.CharField(blank=True, null=True, max_length=15, help_text='所在区、乡、镇')
    detail_address = models.CharField(blank=True, null=True, max_length=100, help_text='详细地址，但不包括省、市、县、区级别')
    email = models.EmailField(blank=True, null=True, help_text='邮件地址')
    qq = models.CharField(blank=True, null=True, max_length=15, help_text='QQ号码')
    mobile = models.CharField(blank=True, null=True, max_length=11, help_text='手机号码')
    tel_num = models.CharField(blank=True, null=True, max_length=13, help_text='电话号码')

    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'asset_facilitator_manufacturer'


class ManufacturerProductModel(models.Model):
    """
    厂商产品线
    """
    manufacturer = models.SmallIntegerField(help_text='厂商ID')
    product_type = models.CharField(max_length=20, help_text='产品类型')
    brand = models.CharField(max_length=20, help_text='品牌名称')
    series = models.CharField(max_length=50, help_text='系列名称')
    model_name = models.CharField(max_length=50, help_text='型号')

    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    def __unicode__(self):
        return '-'.join((self.product_type, self.brand, self.series, self.model_name))

    class Meta:
        db_table = 'asset_facilitator_manufacturer_product'
