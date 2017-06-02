# -*- coding:utf8 -*-
"""
Created on 16/10/2 上午3:19
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

from django.views.generic.base import ContextMixin
from rest_framework.response import Response
from omni.page_config import navigation

import logging

log = logging.getLogger(__name__)


class CommonExtMixin(ContextMixin):
    """
    常规视图扩展类
    """
    body_header_navigation = {'main': '', 'minor': '', 'page': ''}

    @staticmethod
    def get_nav_menu_data():
        """
        创建导航栏菜单实例对象,并通过request.path获取导航及菜单数据
        """
        return navigation.aside_menu_data

    def get_context_data(self, **kwargs):
        """
        获取菜单数据
        """
        kwargs['aside_menu_data'] = self.get_nav_menu_data()
        kwargs['body_header_navigation'] = self.get_body_header_navigation()
        return super(CommonExtMixin, self).get_context_data(**kwargs)

    def get_body_header_navigation(self):
        return self.body_header_navigation


class RelationModelMixin(object):

    def clean_relation_fields(self, request, response_data):

        if 'relation-fields' not in request.GET:
            return response_data

        serializer_class = self.get_serializer_class()
        if not hasattr(serializer_class, 'relation_fields'):
            log.warning('请求参数中包含参数"relation_fields", 但是"{0}"中未定义"relation_fields".')
            return response_data
        relation_fields = [field for field in request.GET['relation-fields'].split(',')
                           if field in serializer_class.relation_fields.keys()]
        for relation_field_name in relation_fields:
            relation_field_values = []
            [relation_field_values.append(obj_data[relation_field_name])
             for obj_data in response_data if obj_data[relation_field_name]]
            if not relation_field_values:
                continue

            per_serializer_class, per_field_name = serializer_class.relation_fields[relation_field_name]
            queryset = per_serializer_class.Meta.model.objects.filter(
                    **{'{0}__in'.format(per_field_name): set(relation_field_values)})
            per_model_values = per_serializer_class(queryset, many=True).data

            per_model_data = {}
            for obj_values in per_model_values:
                per_model_data[obj_values[per_field_name]] = obj_values

            for obj_data in response_data:
                obj_data[relation_field_name] = per_model_data[obj_data[relation_field_name]]
        return response_data

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response_data = self.get_response_data(request, serializer)
            return self.get_paginated_response(response_data)

        serializer = self.get_serializer(queryset, many=True)
        response_data = self.get_response_data(request, serializer)

        return Response(response_data)

    def get_response_data(self, request, serializer):

        response_data = self.clean_relation_fields(request, serializer.data)
        return response_data
