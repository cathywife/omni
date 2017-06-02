# -*- coding:utf8 -*-
"""
Created on 16/10/24 上午12:30
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, \
    unicode_literals

from celery import task

from omni.apps.arch.models import host as host_models
from omni.apps.arch.models import environment as environment_models
from omni.libs.cmdb import host as host_cmdb
from omni.libs.cmdb import environment as environment_cmdb

from django.db.models import ObjectDoesNotExist

import datetime
import logging

log = logging.getLogger(__name__)


def update_on_change_or_create(model, defaults=dict(), **kwargs):
    obj, created = model.objects.get_or_create(defaults=defaults, **kwargs)
    if not created and not {field: obj.__getattribute__(field) for field in defaults.keys()} == defaults:
        [obj.__setattr__(field, defaults[field]) for field in defaults.keys()]
        obj.save()
    return obj


@task.task(ignore_result=True)
def sync_host_life_cycle():
    """
    同步主机生命周期列表
    :return:
    """
    life_cycle_list = host_cmdb.mget_all_host_life_cycle_status()
    if not life_cycle_list:
        log.warning('获取的cmdb主机生命周期列表为空, 无法更新"{0}".'.format(host_models.HostLifeCycleModel.name))
        return
    for cmdb_obj_info in life_cycle_list:
        cmdb_obj_dict = {'name': cmdb_obj_info.name, 'desc': cmdb_obj_info.desc if cmdb_obj_info.desc else ''}
        update_on_change_or_create(host_models.HostLifeCycleModel, defaults=cmdb_obj_dict, **cmdb_obj_dict)


@task.task(ignore_result=True)
def sync_idc():
    """
    同步IDC
    :return:
    """
    idc_list = environment_cmdb.mget_all_idc()
    if not idc_list:
        log.warning('获取的cmdb IDC 列表为空, 无法更新"{0}".'.format(environment_models.IDCModel.name))
        return
    for cmdb_obj_info in idc_list:
        cmdb_obj_dict = {'idc_code': cmdb_obj_info.idc_code, 'desc': cmdb_obj_info.desc if cmdb_obj_info.desc else ''}
        update_on_change_or_create(environment_models.IDCModel, defaults=cmdb_obj_dict, **cmdb_obj_dict)


@task.task(ignore_result=True)
def sync_host_model():
    """
    同步主机型号
    :return:
    """
    host_model_list = host_cmdb.mget_all_host_model()
    if not host_model_list:
        log.warning('获取的cmdb主机型号列表为空, 无法更新"{0}".'.format(host_models.HostModelModel.name))
        return

    for cmdb_obj_info in host_model_list:
        cmdb_obj_dict = {'name': cmdb_obj_info.name, 'desc': cmdb_obj_info.desc if cmdb_obj_info.desc else ''}

        if cmdb_obj_info.name.startswith('t'):
            limit_idc_list = environment_models.IDCModel.objects.filter(idc_code__startswith='qc')
        elif cmdb_obj_info.name.startswith('a'):
            limit_idc_list = environment_models.IDCModel.objects.filter(idc_code__startswith='al')
        else:
            limit_idc_list = environment_models.IDCModel.objects.exclude(idc_code__startswith='qc').\
                exclude(idc_code__startswith='al')
        obj = update_on_change_or_create(host_models.HostModelModel, defaults=cmdb_obj_dict, **cmdb_obj_dict)
        obj.idc_limit.set(limit_idc_list)


@task.task(ignore_result=True)
def sync_host():
    """
    同步主机
    :return:
    """
    def get_cmdb_host_obj_values(cmdb_obj_info):
        values = {}
        try:
            values['env'] = environment_models.EnvModel.objects.get(name__exact=cmdb_obj_info.env)
        except ObjectDoesNotExist:
            values['env'] = None

        try:
            values['use_status'] = host_models.HostLifeCycleModel.objects.get(name=cmdb_obj_info.use_status)
        except ObjectDoesNotExist:
            values['use_status'] = None

        try:
            values['idc'] = environment_models.IDCModel.objects.get(idc_code__exact=cmdb_obj_info.idc)
        except ObjectDoesNotExist:
            values['idc'] = None

        try:
            values['install_date'] = datetime.datetime.strptime(cmdb_obj_info.install_date, '%a %d %b %Y %H:%M:%S %p CST') \
                if cmdb_obj_info.install_date else None
        except ValueError:
            values['install_date'] = None

        try:
            values['conf_model'] = host_models.HostModelModel.objects.get(name__exact=cmdb_obj_info.conf_model)
        except ObjectDoesNotExist:
            values['conf_model'] = None

        return values

    host_list = host_cmdb.mget_all_host()
    if not host_list:
        log.warning('获取的cmdb主机列表为空, 无法更新"{0}".'.format(host_models.HostModel.name))
        return

    for cmdb_obj_info in host_list:
        created = False
        updated = False
        try:
            obj = host_models.HostModel.objects.get(uuid__exact=cmdb_obj_info.uuid)
            cmdb_obj_values = get_cmdb_host_obj_values(cmdb_obj_info)
            obj_validator_list = [obj.hostname, obj.box_hostname,
                                  obj.env.name if obj.env else None,
                                  obj.use_status.name if obj.use_status else None,
                                  obj.idc.name if obj.idc else None,
                                  obj.os_ver, obj.core_ver,
                                  obj.nic0_ip.split(',') if obj.nic0_ip else [],
                                  obj.nic0_mac,
                                  unicode(obj.cpu_num) if obj.cpu_num else None,
                                  unicode(obj.mem_size) if obj.mem_size is not None else None,
                                  obj.host_type if obj.host_type else '',
                                  obj.conf_model.name if obj.conf_model else None]
            cmdb_obj_validator_list = [cmdb_obj_info.hostname, cmdb_obj_info.box_hostname,
                                       cmdb_obj_values['env'].name if cmdb_obj_values['env'] else None,
                                       cmdb_obj_values['use_status'].name if cmdb_obj_values['use_status'] else None,
                                       cmdb_obj_values['idc'].idc_code if cmdb_obj_values['idc'] else None,
                                       cmdb_obj_info.os_ver if cmdb_obj_info.os_ver else '',
                                       cmdb_obj_info.core_ver if cmdb_obj_info.core_ver else '',
                                       cmdb_obj_info.nic0_ip if cmdb_obj_info.nic0_ip else [],
                                       cmdb_obj_info.nic0_mac if cmdb_obj_info.nic0_mac else '',
                                       cmdb_obj_info.cpu, cmdb_obj_info.mem,
                                       cmdb_obj_info.host_type if cmdb_obj_info.host_type else '',
                                       cmdb_obj_values['conf_model'].name if cmdb_obj_values['conf_model'] else None]
            if not obj_validator_list == cmdb_obj_validator_list:
                updated = True

        except ObjectDoesNotExist:
            cmdb_obj_values = get_cmdb_host_obj_values(cmdb_obj_info)
            obj = host_models.HostModel(uuid=cmdb_obj_info.uuid)
            created = True

        if updated or created:
            obj.hostname = cmdb_obj_info.hostname
            obj.box_hostname = cmdb_obj_info.box_hostname

            obj.env = cmdb_obj_values['env']

            obj.use_status = cmdb_obj_values['use_status']

            obj.idc = cmdb_obj_values['idc']

            obj.os_ver = cmdb_obj_info.os_ver if cmdb_obj_info.os_ver else ''
            obj.core_ver = cmdb_obj_info.core_ver if cmdb_obj_info.core_ver else ''
            obj.nic0_ip = ','.join(cmdb_obj_info.nic0_ip) if cmdb_obj_info.nic0_ip else ''
            obj.nic0_mac = cmdb_obj_info.nic0_mac if cmdb_obj_info.nic0_mac else ''
            obj.cpu_num = cmdb_obj_info.cpu
            obj.mem_size = cmdb_obj_info.mem
            obj.host_type = cmdb_obj_info.host_type if cmdb_obj_info.host_type else ''

            obj.install_date = cmdb_obj_values['install_date']

            obj.conf_model = cmdb_obj_values['conf_model']

            obj.save()

