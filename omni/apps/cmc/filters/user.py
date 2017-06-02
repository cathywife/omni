# -*- coding:utf8 -*-
"""
Created on 16/10/4 下午9:29
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

from rest_framework import filters

from ..models.user import UserGroupModel, UserDepartmentModel, UserModel

import django_filters


class UserGroupFilterSet(filters.FilterSet):

    name = django_filters.CharFilter(name='name', lookup_expr='icontains')
    visible_name = django_filters.CharFilter(name='visible_name', lookup_expr='icontains')

    class Meta:
        model = UserGroupModel
        fields = ['name', 'visible_name']


class UserDepartmentFilterSet(filters.FilterSet):

    name = django_filters.CharFilter(name='name', lookup_expr='icontains')
    visible_name = django_filters.CharFilter(name='visible_name', lookup_expr='icontains')

    class Meta:
        model = UserDepartmentModel
        fields = ['name', 'visible_name']


class UserInfoFilterSet(filters.FilterSet):

    name = django_filters.CharFilter(name='name', lookup_expr='icontains')
    visible_name = django_filters.CharFilter(name='visible_name', lookup_expr='icontains')

    class Meta:
        model = UserModel
        fields = ['name', 'visible_name', 'email', 'department']
