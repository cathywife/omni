# -*- coding:utf8 -*-
"""
Created on 16/9/26 上午11:46
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

from rest_framework.generics import ListAPIView
from ..models.swimlane import SwimlaneModel
from ..serializers.swimlane import SwimlaneModelSerializer


class SwimlaneListAPIView(ListAPIView):

    queryset = SwimlaneModel.objects.all()
    serializer_class = SwimlaneModelSerializer
