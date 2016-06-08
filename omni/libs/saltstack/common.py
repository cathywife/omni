# -*- coding:utf8 -*-
"""
Created on 15-11-23 上午12:02
@author: FMC

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

import os
from salt.client import syspaths, LocalClient, Caller

syspaths.CONFIG_DIR = os.getenv('SALT_CONFIG_DIR', '/etc/salt')


def get_salt_master():
    return LocalClient()


def get_salt_caller():
    return Caller()

