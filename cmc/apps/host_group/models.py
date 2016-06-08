# -*- coding:utf8 -*-
"""
Created on 2014年12月24日
    主机组相关数据表
@author: FMC
"""

from django.db import models
from omni.libs.django.fields import list_fields

from omni.libs.django.fields.list_fields import ListCommaSeparatedStringField


class HostGroupInfoModel(models.Model):
    name = models.CharField(max_length=20, unique=True, help_text='主机组名称')
    visible_name = models.CharField(blank=True, null=True, max_length=30, help_text='显示名称')
    env = models.SmallIntegerField(help_text='运行环境ID')
    workspace_path = models.FilePathField(blank=True, null=True, max_length=500, help_text='默认工作目录')
    tags = ListCommaSeparatedStringField(default='base', max_length=15, help_text='主机组标签,例如: app_server可用于标记本机'
                                                                                  '为部署APP应用的服务器')
    run_user = models.SmallIntegerField(blank=True, null=True, help_text='该环境中,通用的运行服务或执行指令的用户,对应user表ID')
    template_list = list_fields.ListCommaSeparatedIntegerField(default='base', max_length=15,
                                                               help_text='主机配置模板列表,对应template表id, 以","分割')
    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    class Meta:
        db_table = 'host_group_info'


class HostRelateHostGroupModel(models.Model):
    env = models.SmallIntegerField(help_text='运行环境ID')
    host = models.SmallIntegerField(help_text='主机节点ID')
    group = models.SmallIntegerField(help_text='主机组ID')

    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    class Meta:
        db_table = 'host_mix_host_group'
