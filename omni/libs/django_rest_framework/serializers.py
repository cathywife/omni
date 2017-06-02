# -*- coding:utf8 -*-
"""
Created on 16/10/21 上午2:49
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, \
    unicode_literals

from rest_framework import serializers
from rest_framework.utils.field_mapping import get_nested_relation_kwargs
from django.core.validators import _lazy_re_compile, ValidationError
from django.db.models import Model


class CommonExtModelSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super(CommonExtModelSerializer, self).to_representation(instance)
        if hasattr(instance, 'get_absolute_url'):
            ret['__url__'] = instance.get_absolute_url()
        return ret

    def build_nested_field(self, field_name, relation_info, nested_depth):
        """
        Create nested fields for forward and reverse relationships.
        """

        class NestedSerializer(serializers.ModelSerializer):
            class Meta:
                model = relation_info.related_model
                depth = nested_depth - 1
                fields = '__all__'

            def to_representation(self, instance):
                ret = super(NestedSerializer, self).to_representation(instance)
                if hasattr(instance, 'get_absolute_url'):
                    ret['__url__'] = instance.get_absolute_url()
                return ret

        field_class = NestedSerializer
        field_kwargs = get_nested_relation_kwargs(relation_info)

        return field_class, field_kwargs

    @staticmethod
    def validate_foreign_key_field(value):
        if not isinstance(value, int) and not _lazy_re_compile('^\d+$').match(value):
            raise ValidationError('ForeignKeyField字段数据, 必须为int类型或正整数字符串. 当前值为: {0}'.format(value))
        new_value = int(value)
        return new_value

    @staticmethod
    def validate_many_to_many_field(value):
        assert isinstance(value, (tuple, list)), 'ManyToManyField字段数据, 必须为(list, tuple). 当前值为: {0}'.format(value)
        new_value = list()
        for fv in value:
            if not isinstance(value, (int, Model)) and not _lazy_re_compile('^\d+$').match(fv):
                raise ValidationError('ManyToManyField字段数据序列的值, 只能为(int, Model, 正整数字符串)类型. 当前值为: {0}'.format(value))
            new_value.append(int(fv))
        new_value.sort()
        return new_value

    def update_foreign_key_field(self, instance, field_name, peer_model, query_param_field=None, **kwargs):
        if not query_param_field:
            query_param_field = field_name
        field_id = '{0}_id'.format(field_name)
        field_obj_id = self.validate_foreign_key_field(self.initial_data.get(query_param_field))
        if field_obj_id and not field_obj_id == instance.__getattribute__(field_id):
            instance.__setattr__(field_name, peer_model.objects.get(pk=field_obj_id))

        return instance

    def update_many_to_many_field(self, instance, field_name, peer_model, query_param_field=None, append=False):
        if not query_param_field:
            query_param_field = field_name
        field_value_list = self.validate_many_to_many_field(self.initial_data.getlist(query_param_field))
        if not field_value_list:
            return instance

        instance_field_obj_id_list = [field_obj.id for field_obj in instance.__getattribute__(field_name).all()]
        instance_field_obj_id_list.sort()
        instance_field_update_list = list(set(field_value_list).difference(instance_field_obj_id_list))
        if append and instance_field_update_list:
            instance.app_id = peer_model.objects.filter(
                pk__in=set(instance_field_update_result_list).difference(instance_field_obj_id_list))

        return instance






