#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: chains

:Synopsis:
 
:Author:
    servilla

:Created:
    5/15/17
"""
from __future__ import print_function

import logging
import sys
import urllib

from docopt import docopt

from d1_client.mnclient_2_0 import MemberNodeClient_2_0
import properties


logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S%z',
                    #filename='$NAME' + '.log',
                    level=logging.INFO)

logger = logging.getLogger('chains')


def  successor(pid=None, mn_client=None):
    sysmeta = mn_client.getSystemMetadata(pid=pid)
    if sysmeta.obsoletedBy is not None:
        return sysmeta.obsoletedBy.value()
    else:
        return None

def predecessor(pid=None, mn_client=None):
    sysmeta = mn_client.getSystemMetadata(pid=pid)
    if sysmeta.obsoletes is not None:
        return sysmeta.obsoletes.value()
    else:
        return None


def main(argv):
    """
    Lists obsolescence chain of a DataONE object.

    Usage:
        chains.py <pid> [-n | --node <node>] [-c | --cert <cert>] [-k | --key <key>]
        chains.py (-h | --help)

    Arguments:
        pid    Persistent identifier of object

    Options:
        -h --help   This page
        -n --node   Target node (either member or coordinating)
        -c --cert   Client certificate
        -k --key    Client certificate key

    """

    args = docopt(str(main.__doc__))

    pid = args['<pid>']

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

    mn_client = MemberNodeClient_2_0(base_url=base_url,
                                     cert_pem_path=cert_pem_path,
                                     cert_key_path=cert_key_path,
                                     verify_tls=properties.VERIFY_TLS,
                                     )

    # Find oldest pid
    current_pid = None
    while pid is not None:
        current_pid = pid
        pid = predecessor(pid, mn_client)
    pid = current_pid

    # Walk obsolescence chain from oldest pid to newest pid
    pids = []
    while pid is not None:
        pids.append(pid)
        pid = successor(pid, mn_client)

    for pid in pids:
        print(pid)

    return 0


if __name__ == "__main__":
    main(sys.argv)