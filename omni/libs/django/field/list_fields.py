# -*- coding:utf8 -*-
"""
Created on 2015年1月12日
    用户相关数据表
@author: FMC
"""
from __future__ import print_function, unicode_literals, division, absolute_import

from django.utils.translation import ugettext_lazy as _
from django.db.models.fields import CommaSeparatedIntegerField
from django.utils import six
from django.db import models
from django.utils.encoding import smart_text
from omni.libs.django.field.validators import validate_comma_separated_str_list


class ListCommaSeparatedIntegerField(six.with_metaclass(models.SubfieldBase, CommaSeparatedIntegerField)):
    def to_python(self, value):
        if isinstance(value, six.string_types):
            return tuple(value.split(','))
        elif isinstance(value, str):
            return tuple(value.split(','))
        else:
            return value

    def get_prep_value(self, value):
        value = super(ListCommaSeparatedIntegerField, self).get_prep_value(value)
        if isinstance(value, (list, tuple)):
            value = ','.join([smart_text(v) for v in value])
        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        if isinstance(value, (list, tuple)):
            return ','.join([smart_text(v) for v in value])
        value = super(ListCommaSeparatedIntegerField, self).get_db_prep_value(value, connection, prepared)
        return value

    def value_to_string(self, obj):
        value_string = super(ListCommaSeparatedIntegerField, self).value_to_string(obj)
        if value_string is None:
            return value_string
        if isinstance(value_string, (list, tuple)):
            return ','.join([smart_text(v) for v in value_string])
        return smart_text(value_string)

    def pre_save(self, model_instance, add):
        value = super(ListCommaSeparatedIntegerField, self).pre_save(model_instance, add)
        if isinstance(value, (list, tuple)):
            value = ','.join([smart_text(v) for v in value])

        return value


class ListCommaSeparatedStringField(six.with_metaclass(models.SubfieldBase, CommaSeparatedIntegerField)):
    default_validators = [validate_comma_separated_str_list]
    description = _("Comma-separated Strings")

    def formfield(self, **kwargs):
        defaults = {
            'error_messages': {
                'invalid': _('只能输入以逗号分割的字符串(字符串只能包含"0-9|A-Z|a-z|_|-").'),
            }
        }
        defaults.update(kwargs)
        return super(ListCommaSeparatedStringField, self).formfield(**defaults)
