# -*- coding:utf8 -*-
"""
Created on 2015年1月4日
    用户相关数据表
@author: FMC
"""
from __future__ import print_function, unicode_literals, division, absolute_import

import re


from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

comma_separated_str_list_re = re.compile('^[\w,-]+$')
validate_comma_separated_str_list = RegexValidator(comma_separated_str_list_re,
                                                   _('只能输入以逗号分割的字符串(字符串只能包含"0-9|A-Z|a-z|_|-").'), 'invalid')