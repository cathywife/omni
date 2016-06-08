# -*- coding:utf8 -*-
"""
Created on 2014年12月24日
    产品相关数据表
@author: FMC
"""
from __future__ import print_function, unicode_literals, division, absolute_import

from django.db import models
from omni.libs.django.fields import list_fields

from omni.libs.django.fields.list_fields import ListCommaSeparatedStringField


class ProductInfoModel(models.Model):
    """
    产品
    """
    name = models.CharField(max_length=50, help_text='产品名称,英文字符/数字')
    visible_name = models.CharField(blank=True, null=True, max_length=50, help_text='产品显示名')
    description = models.CharField(blank=True, null=True, max_length=100, help_text='描述、说明信息')
    env = models.SmallIntegerField(help_text='所属运行环境')
    version = models.CharField(max_length=20, help_text=u'产品版本号', default=u'0.0.1')
    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    class Meta:
        db_table = 'product_info'


class ProjectModel(models.Model):
    """
    项目
    """
    name = models.CharField(max_length=50, help_text='项目名称,英文字符/数字')
    visible_name = models.CharField(blank=True, null=True, max_length=50, help_text='项目显示名')
    description = models.CharField(blank=True, null=True, max_length=100, help_text='描述、说明信息')
    product = models.SmallIntegerField(help_text='所属产品ID')
    env = models.SmallIntegerField(help_text='所属运行环境')
    version = models.CharField(max_length=20, help_text=u'项目版本号', default=u'0.0.1')
    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    class Meta:
        db_table = 'project_info'


class SubProjectModel(models.Model):
    """
    子项目
    """
    name = models.CharField(max_length=50, help_text='子项目名称,英文字符/数字')
    visible_name = models.CharField(blank=True, null=True, max_length=50, help_text='子项目显示名')
    description = models.CharField(blank=True, null=True, max_length=100, help_text='描述、说明信息')
    env = models.SmallIntegerField(help_text='所属运行环境')
    project = models.SmallIntegerField(help_text='所属项目ID')
    version = models.CharField(max_length=20, help_text=u'当前子项目版本号', default=u'0.0.1')
    vcs = models.SmallIntegerField(blank=True, null=True, help_text='版本控制系统类型, 0: 无,即file:///, 1: git, 2: svn')
    project_type = models.BooleanField(default=True, help_text='项目类型,分为两种: True: Dynamic; False: Static')
    project_logger = models.SmallIntegerField(blank=True, null=True, help_text='项目日志记录器,对应log_logger表ID')
    project_config_list = ListCommaSeparatedStringField(blank=True, null=True, max_length=2048, help_text='项目配置文件或目录列表')
    rollback = models.BooleanField(default=True, help_text='项目部署失败后,是否可以直接进行回滚.')
    cdn_refresh = models.BooleanField(default=False, help_text='项目重新部署后,是否需要更新CDN缓存.多用于静态项目.')
    program_language = ListCommaSeparatedStringField(max_length=50, help_text='编程语言,即项目代码由哪些语言编写')
    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    class Meta:
        db_table = 'subproject_info'


class VersionSubProjectModel(models.Model):
    """
    项目版本配置
    """
    name = models.CharField(max_length=50, help_text='版本号')
    description = models.CharField(blank=True, null=True, max_length=100, help_text='版本描述、说明信息')
    env = models.SmallIntegerField(help_text='所属运行环境')
    subproject = models.SmallIntegerField(help_text='子项目ID')
    vcs = models.SmallIntegerField(blank=True, null=True, help_text='版本控制系统类型, 0: 无,即file:///, 1: git, 2: svn')
    project_type = models.BooleanField(default=True, help_text='项目类型,这里指相对部署来说,分为两种: True: Dynamic; False: Static')
    project_logger = models.SmallIntegerField(blank=True, null=True, help_text='项目日志记录器,对应log_logger表ID')
    project_config_list = ListCommaSeparatedStringField(blank=True, null=True, max_length=2048, help_text='项目配置文件或目录列表')
    rollback = models.BooleanField(default=True, help_text='项目部署失败后,是否可以直接进行回滚.')
    cdn_refresh = models.BooleanField(default=False, help_text='项目重新部署后,是否需要更新CDN缓存.多用于静态项目.')
    program_language = ListCommaSeparatedStringField(max_length=50, help_text='编程语言,即项目代码由哪些语言编写')
    deploy_mode = models.SmallIntegerField(help_text='部署方式,对应project_deploy_mode表')
    module_list = list_fields.ListCommaSeparatedIntegerField(max_length=1024, help_text='项目模块列表, 对应与project_module表')

    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    class Meta:
        db_table = 'subproject_version_info'


class ProjectDeployModeModel(models.Model):
    """
    项目部署方式
    """
    name = models.CharField(max_length=30, help_text='部署方式名称')
    mode = models.SmallIntegerField(help_text='项目部署方式: '
                                              '0: 仅原始文件,无其他额外操作,例如:css、js、html等; '
                                              '1: 需要web容器,例如java Web项目使用Tomcat容器; '
                                              '2: 执行特定命令或脚本,例如python语言项目,执行python脚本运行项目、'
                                              'C语言项目,运行项目命令启动项目、java语言项目,运行特定jar包等')
    operate = models.CharField(max_length=1024, help_text='所执行的操作或容器名称等')
    description = models.CharField(max_length=1024, help_text='详细描述')

    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    class Meta:
        db_table = 'project_deploy_mode'


class ProjectModuleModel(models.Model):
    version_project = models.SmallIntegerField(help_text='项目版本ID,表示该模块属于哪个项目中哪个版本')
    name = models.CharField(max_length=15, help_text='模块名称')
    description = models.CharField(blank=True, null=True, max_length=100, help_text='版本描述、说明信息')
    module_type = models.IntegerField(help_text='模块类型, 0: module; 1: master; 2: parent')
    url = models.URLField(max_length=300, help_text='模块源码的仓库URL地址')
    vcs = models.SmallIntegerField(blank=True, null=True, help_text='版本控制系统类型, 0: 无,即file:///, 1: git, 2: svn')
    auth = models.SmallIntegerField(blank=True, null=True, help_text='与vcs对应的认证信息,对应与service中版本控制服务的认证信息')

    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    class Meta:
        db_table = 'project_module'
