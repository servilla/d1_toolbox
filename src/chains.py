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

from docopt import docopt

from d1_client.mnclient_2_0 import MemberNodeClient_2_0
import properties


logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S%z',
                    #filename='$NAME' + '.log',
                    level=logging.INFO)

logger = logging.getLogger('chains')


def  successor(pid=None):
    return None

def predecessor(pid=None):
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
        -k --key    

    """

    args = docopt(str(main.__doc__))

    pid = args['<pid>']

    if args['--node']:
        base_url = args['<node>']
    else:
        base_url = properties.BASE_URL
    if args['--cert']:
        cert_pem_path = args['<cert>']
    else:
        cert_pem_path = properties.CERT_PEM
    if args['--key']:
        cert_key_path = args['<key>']
    else:
        cert_key_path = properties.CERT_KEY

    mn_client = MemberNodeClient_2_0(base_url=properties.BASE_URL,
                                     cert_pem_path=properties.CERT_PEM,
                                     cert_key_path=properties.CERT_KEY,
                                     verify_tls=properties.VERIFY_TLS,
                                     )

    sysmeta = None
    try:
        sysmeta = mn_client.getSystemMetadata(pid=pid)
    except Exception as e:
        logger.error(e)

    if sysmeta is not None:
        obsoletes = None
        obsoletedBy = None
        if sysmeta.obsoletes is not None:
            obsoletes = sysmeta.obsoletes.value()
        if sysmeta.obsoletedBy is not None:
            obsoletedBy = sysmeta.obsoletedBy.value()
        print('obsoletes: {obs}'.format(obs=obsoletes))
        print('obsoleted by: {obs_by}'.format(obs_by=obsoletedBy))

    return 0


if __name__ == "__main__":
    main(sys.argv)