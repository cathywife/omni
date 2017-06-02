# -*- coding:utf8 -*-
"""
Created on 2015年1月4日
    用户相关数据表
@author: FMC
"""
from __future__ import print_function, unicode_literals, division, absolute_import

import re
from django.core import validators


from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _


def str_list_validator(sep=',', message=None, code='invalid', allow_negative=False):
    regexp = validators._lazy_re_compile('^%(neg)s\d+(?:%(sep)s%(neg)s\d+)*\Z' % {
        'neg': '(-)?' if allow_negative else '',
        'sep': re.escape(sep),
    })
    return RegexValidator(regexp, message=message, code=code)


validate_comma_separated_string_list = str_list_validator(
    message=_('Enter only strings separated by commas.'),
)
