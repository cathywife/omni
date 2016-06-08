# -*- coding:utf8 -*-
"""
Created on 2014年12月24日
    用户相关数据表
@author: FMC
"""
from __future__ import print_function, unicode_literals, division, absolute_import

from django.db import models


class UserInfoModel(models.Model):
    username = models.CharField(max_length=50, help_text='用户名,英文字符/数字')
    visible_name = models.CharField(blank=True, null=True, max_length=50, help_text='用户显示名')
    description = models.CharField(blank=True, null=True, max_length=100, help_text='描述、说明信息')
    uid = models.IntegerField(blank=True, null=True, help_text=u'用户UID，仅posix类系统')
    group = models.IntegerField(help_text=u'用户组,对应与group表ID')
    ext_group = models.IntegerField(blank=True, null=True, help_text=u'用户附加组,对应与group表ID')
    password = models.CharField(max_length=50, blank=True, null=True, help_text=u'用户附加组,对应与group表ID')
    public_key = models.CharField(max_length=50, blank=True, null=True, help_text=u'用户公钥')
    private_key = models.CharField(max_length=50, blank=True, null=True, help_text=u'用户私钥')
    home_dir = models.CharField(blank=True, null=True, max_length=200, help_text='用户家目录路径')

    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    class Meta:
        db_table = 'user_info'


class UserGroupModel(models.Model):
    name = models.CharField(max_length=50, help_text='用户组,英文字符/数字')
    visible_name = models.CharField(blank=True, null=True, max_length=50, help_text='用户组显示名')
    description = models.CharField(blank=True, null=True, max_length=100, help_text='描述、说明信息')
    gid = models.IntegerField(blank=True, null=True, help_text=u'用户组GID,仅posix类系统')

    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    class Meta:
        db_table = 'user_group'
