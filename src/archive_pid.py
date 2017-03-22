#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: archive_pid

:Synopsis:
 
:Author:
    servilla

:Created:
    1/26/17
"""

import logging

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S%z',
                    filename='archive_pid.log',
                    level=logging.WARN)

logger = logging.getLogger('archive_pid')

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from d1_client.mnclient_2_0 import MemberNodeClient_2_0
from d1_client.objectlistiterator import ObjectListIterator


def main():

    mn_cert = '/home/servilla/Certs/DataONE/urn_node_LTER-1/urn_node_LTER-1.crt'
    mn_key = '/home/servilla/Certs/DataONE/urn_node_LTER-1/private' \
           '/urn_node_LTER-1.key'
    mn_base_url = 'https://gmn.lternet.edu/mn'

    mn_client = MemberNodeClient_2_0(base_url=mn_base_url, cert_path=mn_cert,
                                     key_path=mn_key)
    objects = ObjectListIterator(client=mn_client)
    cnt = 0

    for obj in objects:
        cnt += 1
        pid = obj.identifier.value()
        print(cnt)
        if 'doi:10.6073/AA' in pid:
            try:
                sysmeta = mn_client.getSystemMetadata(pid=pid)
                if not sysmeta.archived:
                    sysmeta.archived = True
                    mn_client.updateSystemMetadata(pid=pid, sysmeta=sysmeta)
                    logger.warn('Archived PID: {pid}'.format(pid=pid))
            except:
                logger.exception('Failed to archive PID: {pid}'.format(pid=pid))


    return 0


if __name__ == "__main__":
    main()