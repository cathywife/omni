# -*- coding:utf8 -*-
"""
Created on 16/10/21 下午8:58
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView

from ..models.host import HostModelModel
from ..serializers.host import HostModelModelSerializer
from rest_framework import filters
from ..filters.host import HostModelFilterSet


class HostModelListAPIView(ListAPIView):
    """
    get: 获取HostModel 列表
    """
    queryset = HostModelModel.objects.all()
    serializer_class = HostModelModelSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter,)
    filter_class = HostModelFilterSet
    ordering_fields = ('name',)


