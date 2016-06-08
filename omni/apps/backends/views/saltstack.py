# -*- coding:utf8 -*-
"""
Created on 15-12-28 下午11:19
@author: FMC

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

from omni.libs.django.view.restful_api import CommonFormRestFulView
from ..forms.saltstack import SaltStateForm

from ..tasks import salt_master_async


class SaltStateView(CommonFormRestFulView):
    """
    执行saltstack state.sls
    """
    form_class = SaltStateForm
    http_method_names = ['post', 'put', 'options']

    def form_valid(self, form):
        fun = form.cleaned_data.get('fun')
        state_name = form.cleaned_data.get('state_name')
        tgt = form.cleaned_data.get('tgt')
        expr_form = form.cleaned_data.get('expr_form')
        timeout = form.cleaned_data.get('timeout')

        salt_state_task_obj = salt_master_async(tgt=tgt, fun='state.{0}'.format(fun), arg=state_name,
                                                    timeout=timeout, expr_form=expr_form)
        # context = {'id': salt_state_task_obj.id, 'status': salt_state_task_obj.status}
        return super(SaltStateView, self).render_to_response(salt_state_task_obj)

    def form_invalid(self, form):
        context = self.ajax_form_invalid(form)
        return super(SaltStateView, self).render_to_response(context)
