# -*- coding:utf8 -*-
"""
    FMC 创建于 2014年10月10日
    详情视图
"""
import logging


from django.views.generic.detail import DetailView
from django.core import serializers
from django.db.models.query import QuerySet
from django.db.models.base import Model
from .base import CommonExtMixin, CommonBaseExtMixin

log = logging.getLogger(__name__)


class CommonDetailView(CommonExtMixin, DetailView):
    """
    通用常规详情视图
    """
    def get_context_data(self, **kwargs):
        """
        获取详情数据
        """
        context = super(CommonDetailView, self).get_context_data(**kwargs)
        for key in context.keys():
            if isinstance(context[key], QuerySet) and not key == 'object':
                context[key] = self.get_response_data(serializers.serialize('python', context[key]))
            elif isinstance(context[key], Model) and not key == 'object':
                context[key] = self.get_response_data(self.serialize_model_object(context[key]))
            else:
                context[key] = self.get_response_data(context[key])

        if hasattr(self, 'help_texts'):
            context['help_texts'] = self.help_texts
        if hasattr(self, 'labels'):
            context['labels'] = self.labels
        if hasattr(self, 'fields'):
            context['fields'] = self.fields
        return context


class CommonRestFulDetailView(CommonBaseExtMixin, DetailView):
    """
    通用RestFul API 详情视图
    """
    def get_context_data(self, **kwargs):
        if self.object:

            if isinstance(self.object, QuerySet):
                return self.get_response_data(serializers.serialize('python', self.object))
            elif isinstance(self.object, Model):
                return self.get_response_data(self.serialize_model_object(self.object))
            else:
                return self.get_response_data(self.object)
        else:
            return {}