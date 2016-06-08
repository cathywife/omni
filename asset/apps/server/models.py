# -*- coding:utf8 -*-
"""
Created on 15-10-2 下午1:30
@author: FMC
"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, \
    unicode_literals

from django.db import models
from omni.libs.django.field import list_fields


class ServerModel(models.Model):
    """
    服务器模型
    """
    asset_id = models.CharField(max_length=20, unique=True, help_text='服务器资产编号,服务器的唯一标示')
    asset_name = models.CharField(max_length=20, unique=True, help_text='资产主机名, 可变,但必须唯一')
    sn = models.CharField(max_length=20, unique=True, help_text='主机节点SN编号,用于唯一标识服务器,不可变')
    description = models.CharField(blank=True, null=True, max_length=1024, help_text='详细描述')
    model = models.SmallIntegerField(blank=True, null=True, help_text='服务器型号,为server_model表ID')
    nic_list = list_fields.ListCommaSeparatedIntegerField(blank=True, null=True, max_length=50,
                                                          help_text='网卡,为HostNodeNic表ID')
    storage_list = list_fields.ListCommaSeparatedIntegerField(blank=True, null=True, max_length=50,
                                                              help_text='存储设备,为HostNodeStorage表ID')
    os = models.SmallIntegerField(blank=True, null=True, help_text='操作系统,对应于os中的ID')
    provider = models.SmallIntegerField(blank=True, null=True, help_text='服务器硬件供应商,为provider表主键ID')
    idc = models.SmallIntegerField(blank=True, null=True, help_text='IDC供应商,为idc表主键ID')
    rack_id = models.CharField(blank=True, null=True, max_length=20, help_text='机架ID')
    slot = models.CharField(blank=True, null=True, max_length=20, help_text='机架中槽位ID')
    status = models.SmallIntegerField(help_text='主机状态,0: 下架; 1: 关机,但已上架; 2: 开机,正常; 3: 开机,未激活; 4: 未知,可能失去连接')

    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    def __unicode__(self):
        if self.asset_name:
            return self.asset_name
        else:
            return self.asset_id

    class Meta:
        db_table = 'asset_server'


class HostNodeOSModel(models.Model):
    """
    操作系统
    """
    type = models.SmallIntegerField(help_text='操作系统类型,可用值为: 0->Windows、1->Linux、2->BSD、3->MacOSX')
    name = models.CharField(max_length=10, help_text='操作系统发行版,例如: CentOS、RHEL、Windows')
    version = models.CharField(max_length=10, help_text='主版本号')
    minor_version = models.CharField(blank=True, null=True, max_length=10, help_text='次版本号')
    publisher = models.CharField(blank=True, null=True, max_length=100, help_text='发行商')
    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    def __unicode__(self):
        return u'-'.join((self.name, self.version, self.minor_version))

    class Meta:
        db_table = 'host_node_os'


class HostNodeTypeModel(models.Model):
    """
    主机类型
    """
    type = models.CharField(max_length=10, unique=True, help_text='服务器类型,可用值为: 0: 机架式; 1: 塔式; '
                                                                  '2: 卧式; 3: 云服务器; 4: 虚拟机')
    visible_name = models.CharField(blank=True, null=True, max_length=30, help_text='显示名称')
    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    def __unicode__(self):
        return self.type

    class Meta:
        db_table = 'host_node_type'


class HostNodeModelModel(models.Model):
    """
    主机硬件型号
    """
    brand = models.CharField(max_length=10, help_text='品牌名称,为英文或者中文拼音')
    alias = models.CharField(max_length=30, help_text='品牌别名、全称')
    type = models.SmallIntegerField(help_text='服务器类型ID,对应于server_tpye模型中的主键ID')
    series = models.CharField(max_length=20, help_text='系列,例如：S720')
    model = models.CharField(max_length=30, help_text='型号')
    cpu = models.CharField(blank=True, null=True, max_length=20, help_text='CPU型号')
    physical_cpu = models.SmallIntegerField(help_text='物理CPU个数')
    cpu_core = models.SmallIntegerField(help_text='单个CPU核心数')
    cpu_hz = models.FloatField(blank=True, null=True, help_text='CPU频率,单位为：GHZ')
    memory_size = models.SmallIntegerField(help_text='内存大小,单位为：GB')
    disk_num = models.SmallIntegerField(blank=True, null=True, help_text='标配磁盘个数')
    disk_size = models.SmallIntegerField(blank=True, null=True, help_text='标配单个磁盘大小,单位为：MB')
    nic_model = models.CharField(max_length=50, help_text='网卡型号,格式为：品牌-型号-子型号')
    nic_speed = models.CharField(max_length=10, help_text='网卡速率,格式为：1000Mbps')
    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    def __unicode__(self):
        return '-'.join((self.brand, self.model))

    class Meta:
        db_table = 'host_node_model'


class HostNodeNicModel(models.Model):
    """
    网卡
    """
    sn = models.CharField(max_length=30, unique=True, help_text='网卡编号,用于唯一标识网卡,不可变')
    model = models.CharField(max_length=50, help_text='网卡型号,格式为：品牌-型号-子型号')
    is_extend = models.BooleanField(default=False, help_text='网卡是否为扩展,True为扩展,False为该服务器型号自带')
    mac = models.CharField(max_length=12, unique=True, help_text='MAC地址,格式为：FFFFFFFFFFFF')
    ip = models.GenericIPAddressField(blank=True, null=True, help_text='网卡IP地址')
    speed = models.CharField(max_length=10, help_text='网卡速率,格式为：1000Mbps')
    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    def __unicode__(self):
        return '-'.join((self.ip, self.model))

    class Meta:
        db_table = 'host_node_nic'


class HostNodeStorageModel(models.Model):
    """
    存储
    """
    sn = models.CharField(max_length=30, unique=True, help_text='存储编号,用于唯一标识存储,不可变')
    model = models.CharField(max_length=50, help_text='存储型号,格式为: 品牌-型号-子型号')
    is_extend = models.BooleanField(default=False, help_text='存储是否为扩展,True为扩展,Flase为该服务器型号自带')
    type = models.CharField(max_length=10, help_text='存储类型,可用值为: disk->本地磁盘;NFS->网络文件系统;'
                                                     'HDFS->hadoop分布式文件系统;SAN->存储区域网络')
    disk_size = models.IntegerField(help_text='磁盘容量,单位为：MB')
    is_shared = models.BooleanField(default=False, help_text='该存储是否为共享方式,若为True,则表示共享,'
                                                             '那么server字段将是以","分割的服务器列表')
    share_name = models.CharField(blank=True, null=True, max_length=20, help_text='共享存储的名称,用于标识一组共享存储')
    mount_name = models.CharField(blank=True, null=True, max_length=30, help_text='存储挂载至服务器后的设备名称')
    create_time = models.DateTimeField(help_text='创建时间')
    update_time = models.DateTimeField(help_text='更新时间')

    def __unicode__(self):
        return self.sn

    class Meta:
        db_table = 'host_node_storage'
