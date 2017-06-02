# -*- coding:utf8 -*-
"""
Created on 16/9/26 上午11:46
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

from omni.libs.django_rest_framework.serializers import CommonExtModelSerializer
from ..models.product import ProductModel, AppIdModel, ProjectModel
from omni.apps.cmc.models import user
from omni.libs.django_rest_framework.relations import FullObjectPrimaryKeyRelatedField


class ProductModelSerializer(CommonExtModelSerializer):
    serializer_related_field = FullObjectPrimaryKeyRelatedField

    class Meta:
        model = ProductModel
        depth = 1


class ProjectModelSerializer(CommonExtModelSerializer):
    serializer_related_field = FullObjectPrimaryKeyRelatedField

    class Meta:
        model = ProjectModel
        depth = 1


class AppIdModelSerializer(CommonExtModelSerializer):
    serializer_related_field = FullObjectPrimaryKeyRelatedField

    class Meta:
        model = AppIdModel
        depth = 1

    def update(self, instance, validated_data):
        product_id = self.validate_foreign_key_field(self.initial_data.get('product'))
        if product_id and not product_id == instance.product_id:
            instance.product = ProductModel.objects.get(pk=product_id)

        owner_id = self.validate_foreign_key_field(self.initial_data.get('owner'))
        if owner_id and not int(owner_id) == instance.owner_id:
            instance.owner = user.UserModel.objects.get(pk=owner_id)

        dev_department_id = self.validate_foreign_key_field(self.initial_data.get('dev_department'))
        if dev_department_id and not dev_department_id == instance.dev_department_id:
            instance.dev_department = user.UserDepartmentModel.objects.get(pk=dev_department_id)

        # 执行update语句更新AppIdModel
        instance = super(AppIdModelSerializer, self).update(instance, validated_data)

        # 更新关联表
        project_list = self.validate_many_to_many_field(self.initial_data.getlist('project'))
        if project_list and not project_list.sort() == [project_obj.id for project_obj in instance.project.all()].sort():
            instance.project.set(project_list)

        return instance
