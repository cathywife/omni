# -*- coding:utf8 -*-
"""
    FMC 创建于 2014年10月10日
    自定义编辑视图
"""
import logging

# 导入内置库
from django.views.generic.edit import FormMixin, ModelFormMixin, DeletionMixin, CreateView, UpdateView, FormView
from django.http import HttpResponseRedirect
from django.views.generic.detail import BaseDetailView
from django.core.exceptions import ImproperlyConfigured
# 导入自定义模块
from .base import CommonExtMixin, CommonBaseExtMixin
from .list import MultipleObjectFilterMixin
from omni.libs.django.form.bootstrap import BootstrapErrorList

log = logging.getLogger(__name__)


class CommonExtFormMixin(CommonBaseExtMixin):
    """
    FormMixin的通用扩展
    """
    fields_default = {}

    def get_fields_default(self):
        """
        设置Form中未包含字段的默认值
        """
        return self.fields_default

    def ajax_form_invalid(self, form):
        """
        ajax对不合法请求参数的处理
        """
        context = {}
        context['fieldErrors'] = form.errors
        return context

    def form_save(self, form):
        """
        保存form数据，并写入数据库
        """
        return form.save(commit=True)

    def get_result_comment(self):
        """
        返回视图的执行结果描述信息
        """
        comment = {
            'success': '执行成功!! 注: 该信息为默认描述信息,可能不够清晰,请自行扩展更为详细的描述信息!!',
            'failure': '执行失败!! 注: 该信息为默认描述信息,可能不够清晰,请自行扩展更为详细的描述信息!!'
        }
        return comment

    def get_form_kwargs(self):
        """
        为form指定ErrorList类,用于格式化错误错误输出
        """
        kwargs = super(CommonExtFormMixin, self).get_form_kwargs()
        kwargs.update({'error_class': BootstrapErrorList})
        return kwargs


class CommonModelFormMixin(CommonExtFormMixin, ModelFormMixin):
    """
    对ModelFormMixin类的扩展，使其更为通用，并支持Ajax
    """

    def get_model_instance(self):
        """
        创建用于实例化Form的model实例的object变量
        """
        if self.fields_default:
            form_class = self.get_form_class()
            model_class = form_class._meta.model
            self.object = model_class(**self.get_fields_default())

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        # 创建model实例
        self.get_model_instance()
        kwargs = super(CommonModelFormMixin, self).get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs


class CommonCreateView(CommonModelFormMixin, CreateView):
    """
    新增数据的通用视图
    """


class CommonUpdateView(CommonModelFormMixin, UpdateView):
    """
    View for updating an object,
    with a response rendered by template.
    """

    def get_fields_default(self, **kwargs):
        """
        赋予默认值，当值为'__default__'时,则不更改字段
        """
        for key in self.fields_default.keys():
            if self.fields_default[key] == '__default__':
                kwargs[key] = self.object.__getattribute__(key)
                continue
            if key in kwargs.keys() and kwargs[key]:
                continue
            kwargs[key] = self.fields_default[key]
        return kwargs


class MultipleObjectDeletionMixin(DeletionMixin):
    """
    支持多对象删除操作
    """
    def delete(self, request, *args, **kwargs):
        """
        调用delete()，可批量删除多个对象，并重定向至success_url
        """
        self.object_list = self.get_queryset()
        success_url = self.get_success_url()

        comment = self.get_result_comment()
        self.object_list.delete()
        return HttpResponseRedirect(success_url)


class CommonDeleteView(CommonExtFormMixin, MultipleObjectFilterMixin, MultipleObjectDeletionMixin, BaseDetailView):
    """
    接收来自url的pk关键字参数，并通过self.get_queryset()方法获取相应的数据列表，最后调用self.delete批量删除相关记录
    """
    template_name_suffix = '_confirm_delete'


class CommonFormView(CommonExtFormMixin, FormView):
    """
    A view for displaying a form, and rendering a template response.
    """