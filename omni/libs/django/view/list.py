# -*- coding:utf8 -*-
"""
    FMC 创建于 2014年10月10日
    列表视图
"""
import logging

# 导入内置库
from django.views.generic.list import ListView, MultipleObjectMixin
from django.db.models.query import QuerySet
from django.core.exceptions import ImproperlyConfigured
# 导入自定义库
from .base import CommonExtMixin

log = logging.getLogger(__name__)


class CommonListView(CommonExtMixin, ListView):
    """
    列表通用视图
    """


class MultipleObjectFilterMixin(MultipleObjectMixin):
    """
    从url中接收关键字参数pk，将pk的值转换为列表后，对数据库进行查询
    """
    pk_url_kwarg = 'pk'
    pk_delimiter = ','

    def get_queryset(self):
        pk_value = self.__getattribute__(self.pk_url_kwarg) if hasattr(self, self.pk_url_kwarg) else None
        if pk_value:
            pk_list = pk_value.split(self.pk_delimiter)
            if self.queryset is not None:
                queryset = self.queryset
                if isinstance(queryset, QuerySet):
                    queryset = queryset.filter(id__in=pk_list)
            elif self.model is not None:
                queryset = self.model._default_manager.filter(id__in=pk_list)
            else:
                raise ImproperlyConfigured(
                    "%(cls)s is missing a QuerySet. Define "
                    "%(cls)s.model, %(cls)s.queryset, or override "
                    "%(cls)s.get_queryset()." % {
                        'cls': self.__class__.__name__
                    }
                )

            return queryset
        else:
            return super(MultipleObjectFilterMixin, self).get_queryset()
