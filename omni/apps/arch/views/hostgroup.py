# -*- coding:utf8 -*-
"""
Created on 16/8/15 下午9:51
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

from omni.libs.django.view.common import CommonTemplateView
from omni.libs.cmdb import hostgroup as cmdb_hostgroup
from omni.libs.cmdb import host as cmdb_host
from omni.libs.cmdb import mapping as cmdb_mapping
from ..forms.hostgroup import HostGroupRlAppidForm, HostGroupRlHostsForm
from django.http import JsonResponse

import logging

log = logging.getLogger(__name__)


def rebuild_gray_hostgroup_for_view(msg, hostgroup):
    """
    用于view的上层封装
    :param msg:
    :param hostgroup:
    :return:
    """
    # 重建灰度主机组
    result = cmdb_hostgroup.rebuild_gray_for_hostgroup(hostgroup)
    if not result['result']:
        result['msg'] = '{0}成功!!, 但重建灰度分组时失败, 信息: {1}'.format(msg, result['msg'])

    result['msg'] = '{0}成功!!, 灰度分组也已重建成功, 信息: {1}'.format(msg, result['msg'])

    return result


class HostGroupView(CommonTemplateView):
    """
    主机组列表视图
    """
    template_name = 'arch/hostgroup/index.html'

    def get_context_data(self, **kwargs):
        page_num = self.request.GET.get('page', 1)
        page_size = self.request.GET.get('size', 10)

        context = {
            'page_num': page_num,
            'page_size': page_size
        }

        kwargs.update(context)
        return super(HostGroupView, self).get_context_data(**kwargs)


class HostGroupSearchView(CommonTemplateView):
    """
    主机组搜索, 用于load
    """
    template_name = 'arch/hostgroup/hostgroup_table.html'

    def get_context_data(self, **kwargs):
        hostgroup_name = self.request.GET.get('name', '')
        page_num = self.request.GET.get('page', 1)
        page_size = self.request.GET.get('size', 10)

        if hostgroup_name:
            hostgroup_obj_list = cmdb_hostgroup.search_hostgroup_by_name(name=hostgroup_name, page=page_num, size=page_size)
        else:
            hostgroup_obj_list = cmdb_hostgroup.mget_all_hostgroup(page=page_num, size=page_size)

        context = {'hostgroup_list': hostgroup_obj_list}

        kwargs.update(context)
        return super(HostGroupSearchView, self).get_context_data(**kwargs)


class HostGroupInfoAppIdView(CommonTemplateView):
    """
    主机组相关的appid信息, 返回json数据
    """
    template_name = 'arch/hostgroup/appid_table.html'

    def get_context_data(self, **kwargs):
        hostgroup_name = self.request.GET.get('name', '')

        if hostgroup_name:
            appid_list = cmdb_hostgroup.get_appid_for_hostgroup(hostgroup_name)
        else:
            appid_list = []

        context = {'appid_list': appid_list}

        kwargs.update(context)
        return super(HostGroupInfoAppIdView, self).get_context_data(**kwargs)


class HostGroupInfoHostsView(CommonTemplateView):
    """
    主机组相关的主机列表, 返回json数据
    """
    template_name = 'arch/hostgroup/host_table.html'

    def get_context_data(self, **kwargs):
        hostgroup_name = self.request.GET.get('name', '')

        if hostgroup_name:
            host_list = cmdb_hostgroup.get_hosts_for_hostgroup(hostgroup_name)
            host_list.sort()
        else:
            host_list = []

        host_obj_list = list()
        for hostname in host_list:
            host_obj = cmdb_host.get_host_info(hostname)
            if host_obj:
                host_obj_list.append({
                    'name': hostname,
                    'nic0_ip': host_obj.nic0_ip,
                    'use_status': host_obj.use_status
                })
            else:
                host_obj_list.append({'name': hostname})

        context = {'host_obj_list': host_obj_list}

        kwargs.update(context)
        return super(HostGroupInfoHostsView, self).get_context_data(**kwargs)


class HostGroupAddAppidView(CommonTemplateView):
    """
    为主机组添加Appid
    """
    form_class = HostGroupRlAppidForm

    def form_valid(self, form):

        hostgroup_name = form.cleaned_data.get('hostgroup_name')
        app_id = form.cleaned_data.get('app_id')
        # 添加Appid与主机组映射关系
        result = cmdb_mapping.add_hostgroup_rl_appid(app_id, hostgroup_name)
        if not result['result']:
            result['msg'] = 'AppId "{0}" 绑定至主机组"{1}"失败!! 信息: {2}'.format(
                app_id, hostgroup_name, result['msg'])
            if result.get('http_status'):
                return JsonResponse(result, status=result.get('http_status'))
            return JsonResponse(result, status=500)

        # 重建灰度主机组
        result = rebuild_gray_hostgroup_for_view('AppId "{0}" 绑定至主机组"{1}"'.format(
            app_id, hostgroup_name), hostgroup_name)
        return JsonResponse(result)


class HostGroupAddHostsView(CommonTemplateView):
    """
    为主机组扩容服务器
    """
    form_class = HostGroupRlHostsForm

    def form_valid(self, form):

        hostgroup_name = form.cleaned_data.get('hostgroup_name')
        hosts = list(set(form.cleaned_data.get('hosts', '').split(',')))

        # 扩容主机组
        result = cmdb_hostgroup.add_hosts_for_hostgroup(hostgroup_name, hosts)
        if not result['result']:
            result['msg'] = '为主机组"{0}"扩容服务器"{1}"失败!! 信息: {2}'.format(
                hostgroup_name, hosts, result['msg'])
            if result.get('http_status'):
                return JsonResponse(result, status=result.get('http_status'))
            else:
                return JsonResponse(result, status=500)

        # 重建灰度主机组
        result = rebuild_gray_hostgroup_for_view('为主机组"{0}"扩容服务器"{1}"'.format(
            hostgroup_name, hosts), hostgroup_name)
        return JsonResponse(result)


class HostGroupDelAppidView(CommonTemplateView):
    """
    为主机组解除Appid映射
    """
    form_class = HostGroupRlAppidForm

    def form_valid(self, form):

        hostgroup_name = form.cleaned_data.get('hostgroup_name')
        app_id = form.cleaned_data.get('app_id')
        # 删除Appid与主机组映射关系
        result = cmdb_mapping.del_hostgroup_rl_appid(app_id, hostgroup_name)
        if not result['result']:
            result['msg'] = '删除AppId "{0}" 与主机组"{1}"的映射关系失败!! 信息: {2}'.format(
                app_id, hostgroup_name, result['msg'])
            if result.get('http_status'):
                return JsonResponse(result, status=result.get('http_status'))
            return JsonResponse(result, status=500)

        # 重建灰度主机组
        result = rebuild_gray_hostgroup_for_view(
            'AppId "{0}" 与主机组"{1}"的映射关系已删除'.format(app_id, hostgroup_name), hostgroup_name)
        return JsonResponse(result)


class HostGroupDelHostsView(CommonTemplateView):
    """
    主机组缩容服务器
    """
    form_class = HostGroupRlHostsForm

    def form_valid(self, form):

        hostgroup_name = form.cleaned_data.get('hostgroup_name')
        hosts = list(set(form.cleaned_data.get('hosts', '').splist(',')))

        # 缩容主机组
        result = cmdb_hostgroup.del_hosts_for_hostgroup(hostgroup_name, hosts)
        if not result['result']:
            result['msg'] = '从主机组"{0}"删除服务器"{1}"失败!! 信息: {2}'.format(
                hostgroup_name, hosts, result['msg'])
            if result.get('http_status'):
                return JsonResponse(result, status=result.get('http_status'))
            else:
                return JsonResponse(result, status=500)

        # 重建灰度主机组
        result = rebuild_gray_hostgroup_for_view('从主机组"{0}"删除服务器"{1}"'.format(hostgroup_name, hosts), hostgroup_name)
        return JsonResponse(result)

