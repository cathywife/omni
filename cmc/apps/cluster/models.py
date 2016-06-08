# -*- coding:utf8 -*-
"""
Created on 2014年12月24日
    运行环境相关数据表
@author: FMC
"""
from __future__ import print_function, unicode_literals, division, absolute_import

from django.db import models
from omni.libs.django.fields import list_fields


class ClusterInfoModel(models.Model):
    """
    集群信息
    """
    env = models.SmallIntegerField(help_text='运行环境ID')
    name = models.CharField(max_length=100, help_text='集群名称,例如: McFrontProdNLB')
    visible_name = models.CharField(blank=True, null=True, max_length=30, help_text='显示名称,例如: McFront项目生产环境负载均衡')
    model = models.SmallIntegerField(default=0, help_text='集群模式,0: OFF,无集群; 1: NLB,网络负载均衡; 2: HA,高可用; '
                                                          '3: SP,单点,特指部署了多点,但同时仅有1个节点运行')
    host_group_list = list_fields.ListCommaSeparatedIntegerField(blank=True, null=True, max_length=300,
                                                                 help_text='包含的节点组列表,值为以","分割的id列表,对应node_group表ID')
    host_node_list = list_fields.ListCommaSeparatedIntegerField(blank=True, null=True, max_length=300,
                                                                help_text='包含的节点列表,值为以","分割的id列表,对应host_node表ID')
    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    class Meta:
        db_table = 'cluster_info'
