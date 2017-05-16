#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

""":Mod: fix_checksum

:Synopsis:
 
:Author:
    servilla

:Created:
    3/22/17
"""

import logging

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S%z', level=logging.INFO)

logger = logging.getLogger('fix_checksum')

from d1_client.mnclient_2_0 import MemberNodeClient_2_0
import properties



def main():

    mn_client = MemberNodeClient_2_0(base_url=properties.BASE_URL,
                                     cert_pem_path=properties.CERT_PEM,
                                     cert_key_path=properties.CERT_KEY,
                                     verify_tls=properties.VERIFY_TLS,
                                     )

    with open('/home/servilla/tmp/metadataChecksumRepair.txt') as f:
        lines = f.readlines()
    lines = [_.strip() for _ in lines]

    for line in lines:
        line = line.split('|')
        pid = line[0].strip()
        checksum = line[1].strip()
        print(pid,checksum)

        sysmeta = mn_client.getSystemMetadata(pid=pid)
        print(sysmeta.checksum.value())
        sysmeta.checksum = checksum
        sysmeta.checksum.algorithm = 'SHA-1'
        mn_client.updateSystemMetadata(pid=pid,sysmeta=sysmeta)
        sysmeta = mn_client.getSystemMetadata(pid=pid)
        print(sysmeta.checksum.value())
        print('-' * 60)

    return 0


if __name__ == "__main__":
    main()