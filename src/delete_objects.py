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

from docopt import docopt
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from d1_client.mnclient_1_1 import MemberNodeClient_1_1
from d1_client.mnclient_2_0 import MemberNodeClient_2_0
from d1_client.iter.objectlist import ObjectListIterator
import properties


def main():
    """
    Delete object(s) from a DataONE Member Node

    Usage:
        delete_objects.py pid <pid> [--v1] [-n | --node <node>] [-c | --cert <cert>] [-k | --key <key>]
        delete_objects.py file <file> [--v1] [-n | --node <node>] [-c | --cert <cert>] [-k | --key <key>]
        delete_objects.py -h | --help

    Arguments:
        pid    Pid of object to delete
        file   File containing pid(s) (one per line) of objects to delete

    Options:
        -h --help   This page
        -n --node   Target node (either member or coordinating)
        -c --cert   Client certificate
        -k --key    Client certificate key
        --v1        Version 1 client (defaults to version 2)

    """

    args = docopt(str(main.__doc__))

    pids = []
    if args['pid']:
        pids.append(args['<pid>'])
    elif args['file']:
        with open(args['<file>'], 'r') as fn:
            pids = [_.strip() for _ in fn.readlines()]

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

    for pid in pids:
        logger.warn('Deleting: {pid}'.format(pid=pid))
        try:
            client.delete(pid=pid)
        except Exception as e:
            logger.error(e)
        
    return 0


if __name__ == "__main__":
    main()