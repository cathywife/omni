# -*- coding:utf8 -*-
"""
Created on 16/9/26 上午11:46
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

from ..models.host import HostGroupModel, HostModelModel, HostModel
from omni.libs.django_rest_framework.serializers import CommonExtModelSerializer
from omni.libs.django_rest_framework.relations import FullObjectPrimaryKeyRelatedField


class HostModelSerializer(CommonExtModelSerializer):
    serializer_related_field = FullObjectPrimaryKeyRelatedField

    class Meta:
        model = HostModel
        depth = 1


class HostGroupModelSerializer(CommonExtModelSerializer):
    serializer_related_field = FullObjectPrimaryKeyRelatedField

    class Meta:
        model = HostGroupModel
        depth = 1


class HostModelModelSerializer(CommonExtModelSerializer):
    serializer_related_field = FullObjectPrimaryKeyRelatedField

    class Meta:
        model = HostModelModel
        depth = 1

