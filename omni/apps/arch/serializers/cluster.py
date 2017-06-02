# -*- coding:utf8 -*-
"""
Created on 16/9/26 上午11:46
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

import logging

from rest_framework import serializers
from ..models.cluster import ClusterModel, ClusterTemplateModel, ClusterTemplateVersionModel
from ..models.swimlane import SwimlaneModel
from ..models.host import HostModel, HostModelModel
from ..models.product import AppIdModel
from omni.libs.django_rest_framework.relations import FullObjectPrimaryKeyRelatedField
from omni.libs.django_rest_framework.serializers import CommonExtModelSerializer


log = logging.getLogger(__name__)


class ClusterModelSerializer(CommonExtModelSerializer):
    serializer_related_field = FullObjectPrimaryKeyRelatedField

    class Meta:
        model = ClusterModel
        depth = 1


class ClusterTemplateModeSerializer(CommonExtModelSerializer):
    serializer_related_field = FullObjectPrimaryKeyRelatedField

    class Meta:
        model = ClusterTemplateModel
        depth = 1


class ClusterTemplateVersionModeSerializer(CommonExtModelSerializer):
    serializer_related_field = FullObjectPrimaryKeyRelatedField

    class Meta:
        model = ClusterTemplateVersionModel
        depth = 1

    def update(self, instance, validated_data):
        host_model_id = self.validate_foreign_key_field(self.initial_data.get('host_model'))
        if host_model_id and not host_model_id == instance.host_model_id:
            instance.host_model = HostModelModel.objects.get(pk=host_model_id)

        instance = super(ClusterTemplateVersionModeSerializer, self).update(instance, validated_data)

        app_id_list = self.validate_many_to_many_field(self.initial_data.getlist('app_id'))
        instance_appid_id_list = [appid_obj.id for appid_obj in instance.app_id.all()]
        instance_appid_id_list.sort()
        if app_id_list and not app_id_list == instance_appid_id_list:
            log.error('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
            instance.app_id = ClusterTemplateVersionModel.objects.filter(pk__in=app_id_list)
        log.error('yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')
        return instance

    def create(self, validated_data):
        pass
