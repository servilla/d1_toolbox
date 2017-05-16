#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: reset_rightsholder

:Synopsis:
 
:Author:
    servilla

:Created:
    1/26/17
"""

import logging

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S%z', level=logging.WARN)

logger = logging.getLogger('reset_rightsholder')

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
    cnt = 0

    for obj in objects:
        cnt += 1
        pid = obj.identifier.value()
        print(cnt)
        if 'doi:' in pid or 'pasta' in pid:
            try:
                sysmeta = mn_client.getSystemMetadata(pid=pid)
                sysmeta.rightsHolder = 'CN=urn:node:mnTestEDI,DC=dataone,DC=org'
                mn_client.updateSystemMetadata(pid=pid, sysmeta=sysmeta)
                logger.warn('PID rights holder reset: {pid}'.format(pid=pid))
            except:
                logger.exception('PID reset failed: {pid}'.format(pid=pid))
    return 0


if __name__ == "__main__":
    main()