# -*- coding:utf8 -*-
"""
Created on 15-12-29 下午10:23
@author: FMC

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

from django import forms
from django.utils.translation import ugettext_lazy as _


class SaltStateForm(forms.Form):
    """
    saltstack state.sls From
    """
    tgt = forms.CharField(max_length=100, required=True, help_text='目标匹配表达式')
    fun = forms.CharField(max_length=20, required=True, help_text='salt state模块方法名称')
    state_name = forms.CharField(max_length=100, required=False, help_text='salt state 配置名称')
    expr_form = forms.CharField(max_length=20, required=False, help_text='目标匹配方式')
    timeout = forms.IntegerField(required=False, help_text='超时时间,单位(秒)')

    def clean_fun(self):
        salt_state_valid_fun = ['highstate', 'sls', 'single', 'low', 'show_lowstate', 'show_highstate',
                                   'show_sls']
        fun = self.cleaned_data['fun']
        if fun not in salt_state_valid_fun:
            raise forms.ValidationError(_('state方法"%(fun)"不正确!!'), params={'fun': fun})
        return fun

    def clean_expr_form(self):
        valid_expr_form_list = ['glob', 'pcre', 'list', 'grain', 'grain_pcre', 'pillar', 'pillar_pcre', 'nodegroup',
                                'range', 'compound']
        expr_form = self.cleaned_data['expr_form']
        if expr_form and expr_form not in valid_expr_form_list:
            raise forms.ValidationError(_('目标匹配方式"%(expr_form)"不正确!!'), params={'expr_form': expr_form})
        return expr_form

    def clean(self):
        cleaned_data = super(SaltStateForm, self).clean()

        fun = cleaned_data.get('fun')
        state_name = cleaned_data.get('state_name')
        if fun in ['sls', 'single', 'low', 'show_sls'] and not state_name:
            raise forms.ValidationError(_('执行"state.%(fun)"时, 参数"state_name"是必须的.'), params={'fun': fun})
