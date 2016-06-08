# -*- coding:utf8 -*-
"""
    FMC 创建于 2014年8月26日
    web页面的基础结构视图类
"""
import logging

from django.views.generic.base import TemplateView, ContextMixin
from django.utils.encoding import smart_text
from omni.page_config import navigation

log = logging.getLogger(__name__)


class CommonBaseExtMixin(ContextMixin):
    """
    公共扩展Mixin，主要用于扩展响应用户的数据
    """
    choice_data = {}

    @staticmethod
    def serialize_model_object(model_object):
        """
        接收1个model对象，并对model的实例化对象进行序列化，格式如下：
        {'model': 'person.employee', 'fields': {'name': 'zhangsan', 'job': 2}, pk: 0}
        """
        object_data = dict()
        object_data['pk'] = model_object.id
        object_data['model'] = smart_text(model_object._meta)
        object_data['fields'] = model_object.__dict__
        object_data['fields'].pop('_state')
        object_data['fields'].pop('id')

        return object_data

    def get_choise_data(self):
        """
        获取选择列表数据，最终格式类似如下：
        原始数据：
            'choice_data': {
                'person.employee': {
                    'job': {
                        1: 'yunwei', 2: 'manager'
                        }
                    }
                }
        返回数据：
            'choice_data': {
                'person_employee': {
                    'job': [{'value': 1, 'lable': 'yunwei'},{'value': 2, 'lable': 'manager'}]}
                }
        """
        choice_data = {}
        # 若choice_data没有值，则直接返回空字典
        if not self.choice_data:
            return choice_data

        # 生成choice_data字典
        for model_name in self.choice_data.keys():
            # 表为字典格式
            new_model_name = model_name.replace('.', '_')
            choice_data[new_model_name] = {}
            for choice_key in self.choice_data[model_name].keys():
                # 选择key为列表格式
                choice_data[new_model_name][choice_key] = []
                # 为每个子元素生成值，值为字典
                for choice_data_key in self.choice_data[model_name][choice_key].keys():
                    choice_data[new_model_name][choice_key].append(
                        {'value': choice_data_key,
                         'label': self.choice_data[model_name][choice_key][choice_data_key]})
        return choice_data

    def get_visible_data(self, row_data):
        """
        获取返回数据中某些列的显示数据，格式为：
        原始数据：
            {'model': 'person.employee', 'fields': {'name': 'zhangsan', 'job': 2}, pk: 0}
        返回数据：
            {'model': 'person_employee', 'fields': {'name': 'zhangsan', 'job': 2}, pk: 0, visibles: {'job': 'manager'}}
        """

        # 若choice_data没有值，则直接返回原始数据
        if not self.choice_data:
            return row_data
        visible = {}
        model_name = row_data['model']

        for key in row_data['fields'].keys():
            if key in self.choice_data[model_name].keys():
                if row_data['fields'][key] in self.choice_data[model_name][key].keys():
                    visible[key] = self.choice_data[model_name][key][row_data['fields'][key]]
                else:
                    log.warn('Model "%s" 的数据%s中的key "%s" 在"choice_data"中没有匹配的visible name!!' % (model_name, row_data,
                                                                                                key))
                    visible[key] = row_data['fields'][key]
                row_data['visibles'] = visible
        # 将model_name的"."替换为"_"以方便随后在模版或JS中通过"."来获取数据
        new_model_name = model_name.replace('.', '_')
        row_data['model'] = new_model_name
        return row_data

    def get_response_data(self, context=list()):
        """
        获取响应数据,基本格式如下:
        接收的列表类型context数据：
            原始数据：
            [
                {'model': 'person.employee', 'fields': {'name': 'zhangsan', 'job': 2}, pk: 0},
                {'model': 'person.employee', 'fields': {'name': 'zhangsan', 'job': 2}, pk: 1}
            ]
            返回数据：
            {'data': [
                {'model': 'person_employee', 'fields': {'name': 'zhangsan', 'job': 2}, pk: 0, visibles: {'job':
                'manager'}},
                {'model': 'person_employee', 'fields': {'name': 'zhangsan', 'job': 2}, pk: 1, visibles: {'job':
                'manager'}},
                ],
            'choice_data': {
                'person_employee': {
                    'job': [{'value': 1, 'lable': 'yunwei'},{'value': 2, 'lable': 'manager'}]}
                },
            }
        接收的字典类型context数据：
            原始数据：
            {'model': 'person.employee', 'fields': {'name': 'zhangsan', 'job': 2}, pk: 0}
            返回数据：
            {'row': {'model': 'person_employee', 'fields': {'name': 'zhangsan', 'job': 2}, pk: 0, visibles: {'job':
            'manager'}},
            'choice_data': {
                'person_employee': {
                    'job': [{'value': 1, 'lable': 'yunwei'},{'value': 2, 'lable': 'manager'}]}
                },
            }
        context为列表，则返回的为多行数据，多用于显示视图中；若context为字典，则表示返回单行数据，多用于编辑视图中
        """
        return_context = {}
        if isinstance(context, list):
            return_context['data'] = []
            for row_data in context:
                return_context['data'].append(self.get_visible_data(row_data))
        elif isinstance(context, dict):
            return_context['row'] = self.get_visible_data(context)
        # 获取选择列表数据
        return_context['choice_data'] = self.get_choise_data()
        return return_context


class CommonExtMixin(CommonBaseExtMixin):
    """
    常规视图扩展类
    """
    @staticmethod
    def get_nav_menu_data():
        """
        创建导航栏菜单实例对象,并通过request.path获取导航及菜单数据
        """
        return navigation.aside_menu_data

    def get_context_data(self, **kwargs):
        """
        获取菜单数据
        """
        kwargs['aside_menu_data'] = self.get_nav_menu_data()
        return super(CommonBaseExtMixin, self).get_context_data(**kwargs)


class CommonTemplateView(CommonExtMixin, TemplateView):
    """
    基础模版视图,无须额外动态数据，即可展示页面，适合用于静态页面
    """
