# -*- coding:utf8 -*-
"""
Created on 16/9/26 下午2:07
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import validate_slug
from omni.libs.django.model.common import CreateUpdateDateTimeCommonModelMixin

from omni.apps.cmc.models import user
from ..models import swimlane


class ProductModel(CreateUpdateDateTimeCommonModelMixin, models.Model):
    """
    产品信息表
    """
    name = models.CharField(unique=True, max_length=100, verbose_name='产品名称', help_text='产品的唯一标识, 仅支持"英文字符、数字、下划线和连接符"',
                            validators=[validate_slug])
    visible_name = models.CharField(blank=True, max_length=1024, verbose_name='显示名称', help_text='完整的产品名称、中文名称, 用于展示')
    description = models.TextField(blank=True, max_length=2048, verbose_name='产品描述',
                                   help_text='产品的详细描述, 包含涉及部门、业务功能、用户群体、技术架构等')

    class Meta:
        db_table = 'arch_product'

    def get_absolute_url(self):
        return reverse('template-arch:product-detail', args=[str(self.id)])


class ProjectModel(CreateUpdateDateTimeCommonModelMixin, models.Model):
    """
    项目信息表
    """
    name = models.CharField(unique=True, max_length=100, verbose_name='项目名称', validators=[validate_slug],
                            help_text='项目的唯一标识, 仅支持"英文字符、数字、下划线和连接符"')
    visible_name = models.CharField(blank=True, max_length=30, verbose_name='显示名称', help_text='完整的项目名称、中文名称, 用于展示')
    description = models.CharField(blank=True, max_length=1024, verbose_name='项目描述',
                                   help_text='项目的详细描述, 包含涉及项目功能、技术架构等')
    product = models.ForeignKey('ProductModel', on_delete=models.SET_NULL, db_constraint=False,
                                verbose_name='所属产品', help_text='选择项目所属的产品, 一个项目只能所属一个产品')
    swimlane = models.ManyToManyField(swimlane.SwimlaneModel, null=True, blank=True,
                                      db_table='arch_project_relate_swimlane', db_constraint=False,
                                      verbose_name='所在泳道', help_text='项目所属甬道, 默认继承产品所在泳道')
    dev_department = models.ForeignKey(user.UserDepartmentModel, on_delete=models.SET_NULL,
                                       db_constraint=False, verbose_name='所属部门', help_text='选择项目的owner部门')

    class Meta:
        db_table = 'arch_project'

    def get_absolute_url(self):
        return reverse('template-arch:project-detail', args=[str(self.id)])


class AppIdModel(CreateUpdateDateTimeCommonModelMixin, models.Model):
    """
    App Id信息表
    """
    name = models.CharField(unique=True, max_length=100, help_text='AppId的唯一标识名称', verbose_name='AppId名称')
    visible_name = models.CharField(blank=True, max_length=200, verbose_name='显示名称',
                                    help_text='完整的AppID名称、中文名称, 用于展示')
    product = models.ForeignKey(ProductModel, on_delete=models.SET_NULL, db_constraint=False, blank=True, null=True,
                                verbose_name='所属产品', help_text='选择AppId所属的产品')
    project = models.ManyToManyField(ProjectModel, db_constraint=False, blank=True, null=True,
                                     verbose_name='所属项目', help_text='选择AppId所属的项目',
                                     db_table='arch_appid_relate_project')
    life_cycle = models.SmallIntegerField(blank=True, null=True, verbose_name='生命周期',
                                          help_text='生命周期阶段: 申请, 初始, 服役, 转移, 废弃')
    app_arch = models.SmallIntegerField(blank=True, null=True, verbose_name='应用框架', help_text='选择应用架构类型')
    owner = models.ForeignKey(user.UserModel, on_delete=models.SET_NULL, db_constraint=False, blank=True, null=True,
                              verbose_name='项目Owner', help_text='项目责任人, 项目提议、立项、开发、维护人员')
    dev_department = models.ForeignKey(user.UserDepartmentModel, on_delete=models.SET_NULL, db_constraint=False,
                                       blank=True, null=True, verbose_name='所属部门', help_text='选择AppId的owner部门')
    thrift_port = models.PositiveIntegerField(blank=True, null=True, verbose_name='thrift端口号',
                                              help_text='用于thrift协议通信的端口号, 若不存在, 请留空')
    http_port = models.PositiveIntegerField(blank=True, null=True, verbose_name='HTTP协议端口号',
                                            help_text='用于HTTP协议通信的端口号, 若不存在, 请留空')
    monitor_port = models.PositiveIntegerField(blank=True, null=True, verbose_name='监控端口',
                                               help_text='用于监控用途的端口号, 若不存在, 请留空')
    udp_port = models.PositiveIntegerField(blank=True, null=True, verbose_name='udp端口号',
                                           help_text='用于UDP类型的端口号, 若不存在, 请留空')

    class Meta:
        db_table = 'arch_appid'

    def get_absolute_url(self):
        return reverse('template-arch:appid-detail', args=[str(self.id)])


class ProjectArchModel(CreateUpdateDateTimeCommonModelMixin, models.Model):
    """
    项目架构
    """
    project = models.ForeignKey(ProjectModel, on_delete=models.SET_NULL, db_constraint=False, help_text='项目')
    version = models.IntegerField(help_text='版本号', default=0)
    cluster_template = models.ManyToManyField('ClusterTemplateVersionModel',
                                              db_table='arch_project_arch_relate_cluster_template', help_text='集群模板',
                                              db_constraint=False)

    class Meta:
        db_table = 'arch_project_arch'
