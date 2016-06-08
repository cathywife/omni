# -*- coding:utf8 -*-
"""
Created on 15-10-2 上午11:21
@author: FMC
"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, \
    unicode_literals


import logging
import traceback

log = logging.getLogger(__name__)


class NotSpecifiedModelObjException(Exception):
    """
    未指定对象
    """


class NotExistModelObjException(Exception):
    """
    指定的对象不存在
    """


class QueryBaseMixin(object):
    """
    对数据库查询进行封装
    """
    model = None
    cls = None

    @classmethod
    def get_queryset(cls, manager=None):
        """
        返回queryset对象
        :return:
        """
        if manager is None:
            return cls.model._default_manager.all()
        else:
            return cls.model.__getattribute__(manager).all()

    @classmethod
    def _get_queryset_filter_context(cls, **kwargs):
        """
         获取查询数据库的参数字典
        :param kwargs:
        :return:
        """
        pk = kwargs.get('pk')
        if pk:
            context = {'pk': pk}
        else:
            context = dict()
        return context

    @classmethod
    def get_object(cls, pk=None, queryset=None):
        """
        获取单个对象并返回
        :param pk:
        :return:
        """
        if not queryset:
            queryset = cls.get_queryset()
        return queryset.get(**cls._get_queryset_filter_context(pk=pk))

    @classmethod
    def get_obj_context(cls, obj=None, pk=None):
        if obj is None:
            obj = cls.get_object(pk)
        obj_context = obj.__dict__
        obj_context.pop('_state')
        obj_context['pk'] = obj_context['id']
        return obj_context

    @classmethod
    def get_instance(cls, pk):
        """
        :param :
        :return:
        """
        return cls.cls(**cls.get_obj_context(pk))

    @classmethod
    def get_multi_obj_context(cls, pk_list, queryset=None):
        """
        接受一个pk列表,返回各个pk对应配置的列表
        :return: list
        """
        obj_context_list = []
        if not isinstance(pk_list, (list, tuple)):
            pk_list = [pk_list]

        if not queryset:
            queryset = cls.get_queryset()

        for model_obj in queryset.filter(pk_in=pk_list):
            obj_context_list.append(cls.get_obj_context(model_obj))
        return obj_context_list

    @classmethod
    def get_all_obj_context(cls, queryset=None):
        """
        返回表中所有数据
        :return:
        """
        obj_context_list = []

        if not queryset:
            queryset = cls.get_queryset()

        for model_obj in queryset.all():
            obj_context_list.append(cls.get_obj_context(model_obj))
        return obj_context_list


class ByIdentityQueryBaseMixin(QueryBaseMixin):

    @classmethod
    def _get_queryset_filter_context(cls, **kwargs):
        """
         获取查询数据库的参数字典
        :param kwargs:
        :return:
        """
        identity = kwargs.get('identity')
        value_list = kwargs.get('value_list')
        if identity:
            context = {identity: value_list}
        else:
            context = super(ByIdentityQueryBaseMixin, cls)._get_queryset_filter_context(**kwargs)
        return context

    @classmethod
    def get_object(cls, identity=None, value=None, pk=None, queryset=None, **kwargs):

        context = cls._get_queryset_filter_context(identity=identity, value=value, pk=pk, **kwargs)

        if not queryset:
            queryset = cls.get_queryset()
        if identity:
            try:
                return queryset.get(**context)
            except cls.model.DoesNotExist:
                raise NotExistModelObjException(
                    "字段{identity}的值为\"{value}\"的数据在表{table}中不存在, 错误信息: \n{except_info}".format(
                        identity=identity, value=value, table=cls.model._meta.db_table,
                        except_info=traceback.format_exc()))
        return super(ByIdentityQueryBaseMixin, cls).get_object(pk=pk, queryset=queryset)

    @classmethod
    def get_obj_context(cls, obj=None, **kwargs):
        if obj is None:
            obj = cls.get_object(**kwargs)
        return super(ByIdentityQueryBaseMixin, cls).get_obj_context(obj=obj)

    @classmethod
    def get_instance(cls, **kwargs):
        """
        依据主机标示，返回对应主机节点实例
        """
        return cls.cls(**cls.get_obj_context(**kwargs))
    
    @classmethod
    def get_multi_obj_context(cls, identity=None, value_list=list(), pk_list=list(), queryset=None, **kwargs):
        """
        获取多个对象数据并返回, 返回字典
        """
        if not queryset:
            queryset = cls.get_queryset()

        obj_context_dict = {}

        if identity:
            if not isinstance(value_list, (list, tuple)):
                value_list = [value_list]
            filter_context = {'identity': identity + '__in', 'value_list': value_list}
            filter_context.update(kwargs)
            for obj in queryset.filter(cls._get_queryset_filter_context(**filter_context)):
                obj_context = cls.get_obj_context(obj=obj)
                obj_context_dict[obj_context[identity]] = obj_context

            return obj_context_dict
        return super(ByIdentityQueryBaseMixin, cls).get_multi_obj_context(pk_list=pk_list)

    @classmethod
    def get_full_instance(cls, **kwargs):
        """
        获取包含完整配置的实例
        :param kwargs:
        :return:
        """
        return cls.cls(**cls.get_full_context(**kwargs))

    @classmethod
    def get_full_context(cls, **kwargs):
        """
        获取完整配置
        :param kwargs:
        :return:
        """
        return cls.get_obj_context(**kwargs)