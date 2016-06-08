# !/usr/bin/env python
# -*- coding:utf8 -*-
"""
Created on 2015年1月30日
    产品Mixin模块
@author: FMC
"""
from __future__ import print_function, unicode_literals, division, absolute_import

import logging
import copy

log = logging.getLogger(__name__)

from omni.apps import ByIdentityResourceBaseMixin
from omni.apps.product.models import ProductInfoModel, ProjectModel, SubProjectModel, VersionSubProjectModel
from omni.apps.product.base import Project, SubProject, VersionSubProject
from omni.apps.product.manager import ProductBaseManager
from django.utils.encoding import smart_unicode


class ProductMixin(ByIdentityResourceBaseMixin):
    model = ProductInfoModel
    cls = ProductBaseManager

    @classmethod
    def get_full_context(cls, **kwargs):
        """
        获取完整的产品配置
        :param kwargs:
        :return:
        """
        env = kwargs.pop('env')
        project_name = kwargs.pop('project_name')
        subproject_name = kwargs.pop('subproject_name')
        project_version = kwargs.pop('version')

        product_context = cls.get_obj_context(**kwargs)
        product_config = copy.deepcopy(product_context)

        # 项目配置
        project_config = list()
        if project_name:
            project_config.append(ProjectMixin.get_full_context(
                identity='name', value=project_name, subproject_name=subproject_name, project_version=project_version,
                env=env))
        else:
            project_list = product_context.get('project_list', list())

            for p in project_list:
                project_config.append(ProjectMixin.get_instance(pk=p, subproject_name=subproject_name,
                                                                project_version=project_version, env=env))

        product_config['project_list'] = project_config

        return product_config

    @classmethod
    def _get_queryset_filter_context(cls, **kwargs):
        """
        获取查询数据库所需的字段数据
        :param kwargs:
        :return:
        """
        context = super(ProductMixin, cls)._get_queryset_filter_context(**kwargs)
        context['env'] = kwargs.get('env')

        return context


class ProjectMixin(ByIdentityResourceBaseMixin):
    model = ProjectModel
    cls = Project

    @classmethod
    def get_full_context(cls, **kwargs):
        env = kwargs.pop('env')
        subproject_name = kwargs.pop('subproject_name')
        project_version = kwargs.pop('project_version')

        project_context = cls.get_obj_context(**kwargs)
        project_config = copy.deepcopy(project_context)

        subproject_config = list()
        if subproject_name:
            subproject_config.append(SubProjectMixin.get_full_context(
                identity='name', value=subproject_name, project_version=project_version, env=env))
        else:
            subproject_list = project_context['subproject_list']

            for p in subproject_list:
                subproject_config.append(SubProjectMixin.get_instance(pk=p, project_version=project_version, env=env))

        project_config['subproject_list'] = subproject_config

        return project_config

    @classmethod
    def _get_queryset_filter_context(cls, **kwargs):
        """
        获取查询数据库所需的字段数据
        :param kwargs:
        :return:
        """
        context = super(ProjectMixin, cls)._get_queryset_filter_context(**kwargs)
        context['env'] = kwargs.get('env')

        return context


class SubProjectMixin(ByIdentityResourceBaseMixin):
    model = SubProjectModel
    cls = SubProject

    @classmethod
    def get_full_context(cls, **kwargs):
        env = kwargs.pop('env')
        project_version = kwargs.pop('project_version')

        subproject_context = cls.get_obj_context(**kwargs)
        subproject_config = copy.deepcopy(subproject_context)

        version_config = list()
        if project_version:
            version_config.append(VersionProjectMixin.get_full_context(identity='name', value=project_version, env=env))
        else:
            version_list = subproject_context['version_list']
            for v in version_list:
                version_config.append(VersionProjectMixin.get_instance(pk=v, env=env))

        subproject_config['version_list'] = version_config

        return subproject_config

    @classmethod
    def _get_queryset_filter_context(cls, **kwargs):
        """
        获取查询数据库所需的字段数据
        :param kwargs:
        :return:
        """
        context = super(SubProjectMixin, cls)._get_queryset_filter_context(**kwargs)
        context['env'] = kwargs.get('env')

        return context


class VersionProjectMixin(ByIdentityResourceBaseMixin):
    model = VersionSubProjectModel
    cls = VersionSubProject

    @classmethod
    def get_full_context(cls, **kwargs):
        return cls.get_obj_context(**kwargs)

    @classmethod
    def _get_queryset_filter_context(cls, **kwargs):
        """
        获取查询数据库所需的字段数据
        :param kwargs:
        :return:
        """
        context = super(VersionProjectMixin, cls)._get_queryset_filter_context(**kwargs)
        context['env'] = kwargs.get('env')

        return context