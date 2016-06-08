# -*- coding:utf8 -*-
"""
Created on 15-12-26 下午4:37
@author: FMC

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

from django.views.generic.base import View
from django.views.generic.edit import BaseFormView
from django.http.response import JsonResponse, HttpResponseRedirect
from django.core.exceptions import ImproperlyConfigured

from .base import CommonBaseExtMixin
from .edit import CommonExtFormMixin, DeletionMixin


class RestFulResponseMixin(object):
    """
    A mixin that can be response json data
    """
    response_class = JsonResponse

    def render_to_response(self, context, **response_kwargs):
        return self.response_class(context, **response_kwargs)


class CommonRestFulModelFormMixin(CommonExtFormMixin):
    """
    对ModelFormMixin类的扩展，使其更为通用，并支持Ajax
    """
    def form_invalid(self, form):
        context = self.ajax_form_invalid(form)
        return JsonResponse(context)

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        self.object = self.form_save(form)
        self.object.__dict__.pop('_state')
        context_data = {
            'model': self.object._meta.__str__(),
            'pk': self.object.pk,
            'fields': self.object.__dict__
        }
        context = self.get_response_data(context_data)
        context['pk'] = self.object.pk
        return JsonResponse(context)


class RestFulDeletionMixin(DeletionMixin):
    """
    支持Ajax的删除mixin
    """
    def delete(self, request, *args, **kwargs):
        """
        当请求是ajax时，返回json格式的数据
        """
        response = super(RestFulDeletionMixin, self).delete(request, *args, **kwargs)
        if request.is_ajax():
            return JsonResponse({})
        else:
            return response


class MultipleObjectDeletionMixin(DeletionMixin):
    """
    支持多对象删除操作
    """
    status = {
        'result': True,
        'comment': '',
        'data': {}
    }

    def delete(self, request, *args, **kwargs):
        """
        调用delete()，可批量删除多个对象，并重定向至success_url
        """

        self.object_list = self.get_queryset()
        success_url = self.get_success_url()

        comment = self.get_result_comment()

        try:
            self.object_list.delete()
        except:
            self.status['result'] = False
            self.status['comment'] = comment['failure']
        else:
            self.status['result'] = True
            self.status['comment'] = comment['success']

        if self.request.is_ajax():
            return JsonResponse(self.status)
        else:
            return HttpResponseRedirect(success_url)

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")


class CommonRestFulView(CommonBaseExtMixin, RestFulResponseMixin, View):
    """
    通用restful api视图
    """


class CommonFormRestFulView(CommonExtFormMixin, RestFulResponseMixin, BaseFormView):
    """
    通用restful api视图
    """

