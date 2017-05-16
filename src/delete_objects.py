#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: delete_objects

:Synopsis:
 
:Author:
    servilla

:Created:
    5/5/17
"""

import logging

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S%z', level=logging.WARN)

logger = logging.getLogger('delete_objects')

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from d1_client.mnclient_2_0 import MemberNodeClient_2_0
from d1_client.iter.objectlist import ObjectListIterator
import properties


def main():

    mn_client = MemberNodeClient_2_0(base_url=properties.BASE_URL,
                                     cert_pem_path=properties.CERT_PEM,
                                     cert_key_path=properties.CERT_KEY,
                                     verify_tls=properties.VERIFY_TLS,
                                     )

    objects = ObjectListIterator(client=mn_client)
    cnt = len(objects) - 3
    n = 0

    for obj in objects:
        if obj.identifier.value() not in ('knb.1303.1', 'knb.1305.1', 'knb.1308.1'):
            n += 1
            print('Deleting {n} of {cnt}: {pid}'.format(n=n, cnt=cnt, pid=obj.identifier.value()))
            #mn_client.delete(pid=obj.identifier.value())
        
    return 0


if __name__ == "__main__":
    main()