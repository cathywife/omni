# -*- coding:utf8 -*-
"""
Created on 16/9/26 上午11:03
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, \
    unicode_literals

from django.db import models
from omni.libs.django.model.common import CreateUpdateDateTimeCommonModelMixin

from . import environment, cluster
from omni.apps.cmc.models import user


class HostGroupModel(CreateUpdateDateTimeCommonModelMixin, models.Model):
    name = models.CharField(max_length=20, unique=True, help_text='主机组名称')
    visible_name = models.CharField(blank=True, max_length=30, help_text='显示名称')
    env = models.ForeignKey(environment.EnvModel, on_delete=models.SET_NULL, db_constraint=False, help_text='运行环境')
    cluster = models.ForeignKey(cluster.ClusterModel, on_delete=models.SET_NULL, db_constraint=False,
                                help_text='所属集群')

    class Meta:
        db_table = 'arch_hostgroup'


class HostLifeCycleModel(CreateUpdateDateTimeCommonModelMixin, models.Model):
    name = models.CharField(max_length=20, unique=True, help_text='主机生命周期状态')
    desc = models.CharField(max_length=1024, help_text='描述', blank=True)

    class Meta:
        db_table = 'arch_host_life_cycle'


class HostModelModel(CreateUpdateDateTimeCommonModelMixin, models.Model):
    name = models.CharField(max_length=10, unique=True, help_text='主机型号')
    idc_limit = models.ManyToManyField(environment.IDCModel, db_table='arch_host_model_relate_idc',
                                       verbose_name='所在IDC', help_text='机房限制, 用于标识该型号仅在特定的机房存在')
    desc = models.CharField(max_length=1024, blank=True, help_text='型号描述')

    class Meta:
        db_table = 'arch_host_model'


class HostModel(CreateUpdateDateTimeCommonModelMixin, models.Model):
    hostname = models.CharField(max_length=100, unique=True, null=True, help_text='主机名')
    box_hostname = models.CharField(max_length=50, null=True, help_text='初始主机名')
    uuid = models.CharField(max_length=50, unique=True, null=True, help_text='主机UUID')
    env = models.ForeignKey(environment.EnvModel, on_delete=models.SET_NULL, null=True, db_constraint=False,
                            help_text='所属环境')
    use_status = models.ForeignKey(HostLifeCycleModel, on_delete=models.SET_NULL, db_constraint=False, null=True,
                                   help_text='主机生命周期状态')
    idc = models.ForeignKey(environment.IDCModel, on_delete=models.SET_NULL, db_constraint=False, help_text='所属机房',
                            null=True)
    cluster = models.ForeignKey(cluster.ClusterModel, on_delete=models.SET_NULL, db_constraint=False, null=True,
                                help_text='所属集群')
    hostgroup = models.ForeignKey(HostGroupModel, on_delete=models.SET_NULL, db_constraint=False, null=True,
                                  help_text='所属主机组')
    os_ver = models.CharField(max_length=100, blank=True, help_text='操作系统版本')
    core_ver = models.CharField(max_length=100, blank=True, help_text='内核版本')
    nic0_ip = models.GenericIPAddressField(blank=True, null=True, help_text='IP地址')
    nic0_mac = models.CharField(max_length=17, blank=True, help_text='MAC地址')
    cpu_num = models.SmallIntegerField(null=True, help_text='CPU核数')
    mem_size = models.PositiveIntegerField(null=True, help_text='内存容量')
    hd_size = models.PositiveIntegerField(null=True, help_text='内存容量')
    host_type = models.CharField(max_length=20, blank=True, help_text='主机类型')
    install_date = models.DateTimeField(blank=True, null=True, help_text='装机日期')
    conf_model = models.ForeignKey(HostModelModel, on_delete=models.SET_NULL, null=True, db_constraint=False,
                                   help_text='主机型号')
    ops_user_group = models.ForeignKey(user.UserGroupModel, on_delete=models.SET_NULL, db_constraint=False,
                                       null=True, help_text='运维小组')

    class Meta:
        db_table = 'arch_host'

