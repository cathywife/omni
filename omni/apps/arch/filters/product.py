# -*- coding:utf8 -*-
"""
Created on 16/10/4 下午9:29
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, \
    unicode_literals

from rest_framework import filters

from ..models.product import ProductModel, AppIdModel

import django_filters


class ProductFilterSet(filters.FilterSet):

    name = django_filters.CharFilter(name='name', lookup_expr='icontains')

    class Meta:
        model = ProductModel
        exclude = ('update_time', 'create_time')


class AppIdFilterSet(filters.FilterSet):

    name = django_filters.CharFilter(name='name', lookup_expr='icontains')

    class Meta:
        model = AppIdModel
        exclude = ('update_time', 'create_time')

