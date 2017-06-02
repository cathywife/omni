# -*- coding:utf8 -*-
"""
Created on 16/11/22 下午8:43
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, \
    unicode_literals

from rest_framework import filters

from ..models.host import HostModelModel

import django_filters


class HostModelFilterSet(filters.FilterSet):

    idc = django_filters.CharFilter(name='idc_limit__idc_code', lookup_expr='exact')
    name = django_filters.CharFilter(name='name', lookup_expr='icontains')

    class Meta:
        model = HostModelModel
        exclude = ('update_time', 'create_time')
