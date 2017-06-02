# -*- coding:utf8 -*-
"""
Created on 17/3/22 上午12:52
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

from cmdblib.client import Client

CMDB_CLIENT_ID = "3fbc37d609e64b1f81b79c7240dbb063"
CMDB_SECRET = "UTWiaxGFdnywPo1CMfeHdAcq0Cqk6VzF4GfjM2P1cyWONbsvf1q11itJAoUrQbnki8fjBEdBowTFPAk5U9hoZOd6D3fFZBUYsyFhV" \
              "A0zz1ruHhoVBuxTlKqrt2W5ayrJ"
CMDB_HOST = 'cmdb.elenet.me'
CMDB_PORT = 8080

cmdb_client = Client(client_id=CMDB_CLIENT_ID,
                     secret=CMDB_SECRET,
                     host=CMDB_HOST,
                     port=CMDB_PORT)


data = cmdb_client.search_entities('rl_group_hosts', ezon_code='alta1',  size=100000, page=1)


