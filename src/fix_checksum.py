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

import d1_client.mnclient_2_0


logger = logging.getLogger('fix_checksum')


def main():
    gmn_client = d1_client.mnclient_2_0.MemberNodeClient_2_0(
        base_url='https://gmn.lternet.edu/mn',
        cert_path='/home/servilla/Certs/DataONE/urn_node_LTER-1'
                  '/urn_node_LTER-1.crt',
        key_path='/home/servilla/Certs/DataONE/urn_node_LTER-1/private'
                 '/urn_node_LTER-1.key'
    )

    with open('/home/servilla/tmp/metadataChecksumRepair.txt') as f:
        lines = f.readlines()
    lines = [_.strip() for _ in lines]

    for line in lines:
        line = line.split('|')
        pid = line[0].strip()
        checksum = line[1].strip()
        print(pid,checksum)

        sysmeta = gmn_client.getSystemMetadata(pid=pid)
        print(sysmeta.checksum.value())
        sysmeta.checksum = checksum
        sysmeta.checksum.algorithm = 'SHA-1'
        gmn_client.updateSystemMetadata(pid=pid,sysmeta=sysmeta)
        sysmeta = gmn_client.getSystemMetadata(pid=pid)
        print(sysmeta.checksum.value())
        print('-' * 60)

    return 0


if __name__ == "__main__":
    main()