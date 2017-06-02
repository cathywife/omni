# -*- coding:utf8 -*-
"""
    FMC 创建于 2014年8月26日
    web页面的基础结构视图类
"""
import logging

from django.views.generic.base import TemplateView
from django.core.exceptions import ImproperlyConfigured
from rest_framework.generics import ListCreateAPIView, ListAPIView
from .mixin import CommonExtMixin
from posixpath import normpath

log = logging.getLogger(__name__)


class CommonTemplateView(CommonExtMixin, TemplateView):
    """
    基础模版视图,无须额外动态数据，即可展示页面，适合用于静态页面
    """


class MatchByUrlTemplateView(CommonTemplateView):
    """
    依据request.path自动获取template_name
    """

    def get_template_names(self):
        """
        调用父类方法获取，如果未获得，则捕获异常
        """
        try:
            template_list = super(MatchByUrlTemplateView, self).get_template_names()
        except ImproperlyConfigured:
            # 如果template_name没有定义,则指定为request.path
            if self.request.path == '/':
                request_url = '/index.html'
            else:
                request_url = self.request.path

            if request_url:
                abs_path = normpath(request_url)
                if abs_path.endswith('.html'):
                    template_list = [abs_path[1:]]
                else:
                    template_list = [abs_path[1:] + '.html']

                if template_list:
                    log.debug(u'通过requst.path \"%s\" 获得template_name \"%s\".' % (
                        request_url, str(template_list)))
                else:
                    template_list = []
                    log.warn(u'''没有指定template_name, 且无法通过requst.path: \"%s\"获得模版名称, 因此无法确定template_name.
                    原因可能是：1、项目bug，缺少与URL相应的视图; 2、用户访问了不存在的URL.''' % request_url)

            else:
                log.error(u'没有指定template_name, 且requst.path为空, 因此无法获得template_name值. 请定义template_name.')
                template_list = []

        return template_list

