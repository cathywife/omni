# -*- coding:utf8 -*-
"""
Created on 16/9/26 下午2:07
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, \
    unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from omni.libs.django.model.common import CreateUpdateDateTimeCommonModelMixin

from . import environment, product
from omni.apps.cmc.models import config


class ClusterTemplateModel(CreateUpdateDateTimeCommonModelMixin, models.Model):
    """
    集群模板
    """
    name = models.CharField(unique=True, max_length=100, verbose_name='集群模板名称', help_text='模板名称, 例如: web-proxy')
    description = models.TextField(max_length=4096, verbose_name='描述', help_text='请填写相关描述信息, 最多4096字符')

    class Meta:
        db_table = 'arch_cluster_template'

    def get_absolute_url(self):
        return reverse('template-arch:cluster-template-detail', args=[str(self.pk)])


class ClusterTemplateVersionStatusModel(CreateUpdateDateTimeCommonModelMixin, models.Model):
    """
    集群模板版本状态
    """
    name = models.CharField(unique=True, max_length=20, verbose_name='集群模板版本状态', help_text='用于标识集群模板的版本状态')
    description = models.CharField(max_length=1024, verbose_name='描述', help_text='请填写相关说明信息, 最多1024字符')

    class Meta:
        db_table = 'arch_cluster_template_version_status'


class ClusterTemplateVersionModel(CreateUpdateDateTimeCommonModelMixin, models.Model):
    """
    集群模板版本
        主机组 APPID 集群配置  业务组件(反向代理,fastcgi等) 基础组件(supervisor, service, systemd, agent, crond, 日志轮转)
        基础语言(python, java) 集群内部的组件及业务间依赖关系
    """
    template = models.ForeignKey(ClusterTemplateModel, on_delete=models.SET_NULL, verbose_name='集群模板',
                                 help_text='集群模板', db_constraint=False)
    version = models.PositiveIntegerField(verbose_name='版本', help_text='版本号', default=0)
    changes = models.TextField(verbose_name='变更描述', blank=True, help_text='请列出详细的变更说明信息')
    status = models.ForeignKey(ClusterTemplateVersionStatusModel, on_delete=models.SET_NULL, db_constraint=False,
                               verbose_name='集群模板状态', help_text='选择集群模板状态')
    # name_template = models.CharField(max_length=100, verbose_name='集群命名规则',
    #                                  help_text='正则表达式, 例如: xg-hg-web-restapi-\d{1,2}')
    # hostgroup_name_template = models.CharField(max_length=100, verbose_name='主机组命名规则',
    #                                            help_text='正则表达式, 例如: xg-hg-web-restapi-1-\d{1,2}')
    # hostname_template = models.CharField(max_length=100, verbose_name='主机名命名规则',
    #                                      help_text='正则表达式, 例如: xg-web-restapi-\d{1,2}')

    # cluster_type = models.SmallIntegerField(help_text='集群类型, 1: 业务集群 2: 中间件间 3: 接入层集群')
    host_model = models.ForeignKey('arch.HostModelModel', on_delete=models.SET_NULL, db_constraint=False, null=True,
                                   verbose_name='集群默认机型', help_text='请选择集群的默认机型, 可在创建集群时覆盖这里的选择.')
    app_id = models.ManyToManyField(product.AppIdModel, db_table='arch_cluster_template_relate_app', null=True,
                                    db_constraint=False, verbose_name='App ID', help_text='请选择需在集群中部署的APPID列表')
    config = models.ManyToManyField(config.ConfigModel, db_table='arch_cluster_template_relate_config',
                                    db_constraint=False,
                                    blank=True, null=True, verbose_name='集群配置', help_text='请添加应用于集群的配置')
    # middleware_list = models.CommaSeparatedIntegerField(blank=True, max_length=1024, help_text='集群节点部署的中间件')
    # system_component_list = models.CommaSeparatedIntegerField(blank=True, max_length=1024,
    #                                                           help_text='集群节点的系统组件管理')
    # component_invocation_list = models.CommaSeparatedIntegerField(blank=True, max_length=1024,
    #                                                               help_text='集群内各组件间调用链')

    class Meta:
        db_table = 'arch_cluster_template_version'
        unique_together = ('template', 'version')

    def get_absolute_url(self):
        return reverse('template-arch:cluster-template-version-detail', args=[str(self.template_id), str(self.version)])


class ClusterModel(CreateUpdateDateTimeCommonModelMixin, models.Model):
    """
    集群表
    """
    env = models.ForeignKey(environment.EnvModel, on_delete=models.SET_NULL, help_text='运行环境', db_constraint=False)
    name = models.CharField(unique=True, max_length=100, help_text='集群名称')
    visible_name = models.CharField(blank=True, max_length=30, help_text='显示名称')
    idc = models.ForeignKey(environment.IDCModel, on_delete=models.SET_NULL, db_constraint=False, help_text='所在机房')
    template = models.ForeignKey(ClusterTemplateModel, on_delete=models.SET_NULL, help_text='集群模板', db_constraint=False)
    template_version = models.ForeignKey(ClusterTemplateVersionModel, on_delete=models.SET_NULL, help_text='版本号',
                                        db_constraint=False)
    swimlane = models.ForeignKey('SwimlaneModel', on_delete=models.SET_NULL, db_constraint=False, null=True,
                                 help_text='所属泳道')
    host_model = models.ForeignKey('HostModelModel', on_delete=models.SET_NULL, db_constraint=False,
                                   help_text='集群主机机型')

    class Meta:
        db_table = 'arch_cluster'

