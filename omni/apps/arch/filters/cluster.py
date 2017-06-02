# -*- coding:utf8 -*-
"""
Created on 16/11/3 上午12:46
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, \
    unicode_literals

from rest_framework import filters

from ..models.cluster import ClusterTemplateVersionModel, ClusterTemplateModel

import django_filters


class ClusterTemplateVersionFilterSet(filters.FilterSet):

    status = django_filters.NumberFilter(name='status', lookup_expr='exact')
    inherit_version = django_filters.NumberFilter(name='version', lookup_expr='exact')

    class Meta:
        model = ClusterTemplateVersionModel
        exclude = ('update_time', 'create_time')

