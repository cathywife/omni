# -*- coding:utf8 -*-
"""
Created on 2015年1月5日
    运行环境相关数据表
@author: FMC
"""
from __future__ import print_function, unicode_literals, division, absolute_import

from django.db import models

from omni.libs.django.fields.list_fields import ListCommaSeparatedStringField


class BaseSoftwareModel(models.Model):
    sn = models.CharField(max_length=50, unique=True, help_text='实例配置唯一编号')
    description = models.CharField(blank=True, null=True, max_length=1024, help_text='描述、说明信息')
    version = models.CharField(blank=True, null=True, max_length=15, help_text='版本号')
    common_name = models.SmallIntegerField(help_text='软件统称,例如: python2,python3统称python;且会对应到python模块的Python类')
    main_home = models.FilePathField(default='/usr/', max_length=300, help_text='安装主目录')
    bin_path_list = ListCommaSeparatedStringField(blank=True, null=True, default='bin', max_length=500,
                                                  help_text='bin目录列表,例如: bin;sbin;libexec等')
    run_user = models.SmallIntegerField(blank=True, null=True, help_text='该环境中,通用的运行服务或执行指令的用户,对应user表ID')

    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    class Meta:
        abstract = True
