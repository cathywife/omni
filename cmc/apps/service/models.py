# -*- coding:utf8 -*-
"""
Created on 2014年12月24日
    服务相关数据表
@author: FMC
"""
from __future__ import print_function, unicode_literals, division, absolute_import

from django.db import models


class GitServerModel(models.Model):
    server_name = models.CharField(max_length=30, unique=True, help_text='服务器名')
    description = models.CharField(blank=True, null=True, max_length=1024, help_text='描述、说明信息')
    protocol_git = models.BooleanField(default=False, help_text='是否支持git连接协议')
    protocol_ssh = models.BooleanField(default=True, help_text='是否支持ssh连接协议')
    protocol_http = models.BooleanField(default=True, help_text='是否支持http连接')
    protocol_https = models.BooleanField(default=True, help_text='是否支持https连接')
    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    class Meta:
        db_table = 'service_git_server'


class GitRepositoryModel(models.Model):
    server_id = models.SmallIntegerField(help_text='Git服务器id,git_server表id')
    description = models.CharField(blank=True, null=True, max_length=1024, help_text='描述、说明信息')
    name = models.CharField(max_length=30, help_text='git仓库名称')

    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    class Meta:
        db_table = 'service_git_repository'


class GitAuthModel(models.Model):
    server_id = models.SmallIntegerField(help_text='Git服务器id,git_server表id')
    description = models.CharField(blank=True, null=True, max_length=1024, help_text='描述、说明信息')
    username = models.CharField(max_length=50, help_text='用户名')
    password = models.CharField(max_length=50, help_text='密码')
    identity = models.CharField(max_length=4096, help_text='SSH认证证书')

    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    class Meta:
        db_table = 'service_git_auth'


class SvnServerModel(models.Model):
    server_name = models.CharField(max_length=30, unique=True, help_text='服务器名')
    description = models.CharField(blank=True, null=True, max_length=1024, help_text='描述、说明信息')
    protocol_svn = models.BooleanField(default=False, help_text='是否支持svn连接协议')
    protocol_http = models.BooleanField(default=True, help_text='是否支持http连接')
    protocol_https = models.BooleanField(default=True, help_text='是否支持https连接')
    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    class Meta:
        db_table = 'service_svn_server'


class SvnRepositoryModel(models.Model):
    name = models.CharField(max_length=30, help_text='Svn仓库名称')
    server_id = models.SmallIntegerField(help_text='Svn服务器id,svn_server表id')
    description = models.CharField(blank=True, null=True, max_length=1024, help_text='描述、说明信息')
    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    class Meta:
        db_table = 'service_svn_repository'


class SvnAuthModel(models.Model):
    server_id = models.SmallIntegerField(help_text='Svn服务器id,svn_server表id')
    description = models.CharField(blank=True, null=True, max_length=1024, help_text='描述、说明信息')
    username = models.CharField(max_length=50, help_text='用户名')
    password = models.CharField(max_length=50, help_text='密码')
    is_active = models.BooleanField(default=True, help_text='用户是否激活')
    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    class Meta:
        db_table = 'service_svn_auth'
