#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: list_objects

:Synopsis:
 
:Author:
    servilla

:Created:
    1/26/17
"""

import logging

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S%z', level=logging.WARN)

logger = logging.getLogger('list_objects')

from docopt import docopt
from urllib3.exceptions import InsecureRequestWarning
import urllib3

urllib3.disable_warnings(InsecureRequestWarning)

from d1_client.mnclient_1_1 import MemberNodeClient_1_1
from d1_client.mnclient_2_0 import MemberNodeClient_2_0
from d1_client.iter.objectlist import ObjectListIterator
import properties


def main():
    """
    List objects at a DataONE Member Node

    Usage:
        list_objects.py [--v1] [-n | --node <node>] [-c | --cert <cert>] [-k | --key <key>]
        list_objects.py defaults
        list_objects.py -h | --help

    Arguments:
        defaults Print default properties to stdout

    Options:
        -h --help   This page
        -n --node   Target node (either member or coordinating)
        -c --cert   Client certificate
        -k --key    Client certificate key

    """
    args = docopt(str(main.__doc__))

    if args['defaults']:
        properties.dump()
        return 0

    if args['--node']:
        base_url = args['<node>']
    else:
        base_url = properties.BASE_URL

    if args['--cert']:
        cert_pem_path = args['<cert>']
        if cert_pem_path == 'None':
            cert_pem_path = None
    else:
        cert_pem_path = properties.CERT_PEM

    if args['--key']:
        cert_key_path = args['<key>']
        if cert_key_path == 'None':
            cert_key_path = None
    else:
        cert_key_path = properties.CERT_KEY

    if args['--v1']:
        client = MemberNodeClient_1_1(base_url=base_url,
                                      cert_pem_path=cert_pem_path,
                                      cert_key_path=cert_key_path,
                                      verify_tls=properties.VERIFY_TLS,
                                      )
    else:
        client = MemberNodeClient_2_0(base_url=base_url,
                                         cert_pem_path=cert_pem_path,
                                         cert_key_path=cert_key_path,
                                         verify_tls=properties.VERIFY_TLS,
                                         )


    objects = ObjectListIterator(client=client)
    for obj in objects:
        print('{pid}'.format(pid=obj.identifier.value()))
        
    return 0


if __name__ == "__main__":
    main()