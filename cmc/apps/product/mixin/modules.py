# !/usr/bin/env python
# -*- coding:utf8 -*-
"""
Created on 2015年2月11日
    项目模块Mixin模块
@author: FMC
"""
from __future__ import print_function, unicode_literals, division, absolute_import

import logging
import copy

log = logging.getLogger(__name__)

from omni.apps import ByIdentityResourceBaseMixin
from omni.apps.product.models import ProjectModel
from django.utils.encoding import smart_unicode


class ProjectModuleDuplicateException(ValueError):
    """
    项目模块名称重复
    """


class ProjectModuleMixin(ByIdentityResourceBaseMixin):
    model = ProjectModel
    cls = None

    @classmethod
    def _get_queryset_filter_context(cls, **kwargs):
        context = super(ProjectModuleMixin, cls)._get_queryset_filter_context(**kwargs)
        context['version_project'] = kwargs.get('version_project')
        return context

    @classmethod
    def get_project_module_by_version(cls, version_pk, queryset=None, **kwargs):
        """
        获取指定项目版本的所有模块信息
        :param version_pk:
        :return:
        """
        if not queryset:
            queryset = cls.get_queryset()

        obj_context_dict = {}

        if version_pk:
            if not isinstance(version_pk, int):
                try:
                    version_pk = int(version_pk)
                except ValueError:
                    raise TypeError('指定的项目版本PK值,必须为int类型,而不是{0}'.format(type(version_pk)))
            filter_context = {'version_project': version_pk}
            filter_context.update(kwargs)
            for obj in queryset.filter(cls._get_queryset_filter_context(**filter_context)):
                obj_context = cls.get_obj_context(obj=obj)
                if obj_context_dict.get(obj_context['name']):
                    raise ProjectModuleDuplicateException('PK值为{version_pk}的项目版本,其模块{module_list}名称重复!!'.format(
                        version_pk=version_pk,
                        module_list=smart_unicode([obj_context_dict[obj_context['name']]['pk'], obj_context['pk']])
                    ))
                obj_context_dict[obj_context['name']] = obj_context

        else:
            obj_context_dict = dict()

        return obj_context_dict
