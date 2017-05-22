#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: peek

:Synopsis:
    Peeks at an object's system metadata.
     
:Author:
    servilla

:Created:
    5/22/17
"""
from __future__ import print_function

import logging
import sys

from d1_client.mnclient_2_0 import MemberNodeClient_2_0
from docopt import docopt

import properties

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S%z',
                    #filename='$NAME' + '.log',
                    level=logging.INFO)

logger = logging.getLogger('peek')




def main(argv):
    """
    Peeks at an object's system metadata
    
    Usage: 
        chains.py file <file> [-n | --node <node>] [-c | --cert <cert>] [-k | --key <key>] [-a | --attr <attr>] [--header]
        chains.py pid <pid> [-n | --node <node>] [-c | --cert <cert>] [-k | --key <key>] [-a | --attr <attr>] [--header]
        chains.py -h | --help

    Arguments:
        pid    Pid of object to peek
        file   File containing pid(s) (one per line) of objects to peek
                
    Options:
        -h --help   This page
        -n --node   Target node (either member or coordinating)
        -c --cert   Client certificate
        -k --key    Client certificate key
        -a --attr   Comma separated list of sysmeta attributes to display (none for all)
        --header    Add header line

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

    add_header_line = False
    if args['--header']:
        add_header_line = True

    attributes = None
    if args['--attr']:
        attributes = [ _.strip() for _ in args['<attr>'].split(',')]

    mn_client = MemberNodeClient_2_0(base_url=base_url,
                                     cert_pem_path=cert_pem_path,
                                     cert_key_path=cert_key_path,
                                     verify_tls=properties.VERIFY_TLS,
                                     )

    for pid in pids:
        sm = mn_client.getSystemMetadata(pid=pid)
        print(sm.identifier.value())
        replicas = sm.replica
        for replica in replicas:
            print(replica.replicaMemberNode.value())


    return 0


if __name__ == "__main__":
    main(sys.argv)