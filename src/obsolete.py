#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: obsolete.py

:Synopsis:
    Set obsolescence information in system metadata for an DataONE object.
 
:Author:
    servilla

:Created:
    5/22/17
"""

import logging
import sys

from d1_client.mnclient_2_0 import MemberNodeClient_2_0
from docopt import docopt
import pyxb

import properties


logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S%z',
                    #filename='$NAME' + '.log',
                    level=logging.WARNING)

logger = logging.getLogger('obsolete.py')


def main(argv):
    """
    Peeks at an object's system metadata

    Usage: 
        obsolete.py <pid> [-n | --node <node>] [-c | --cert <cert>]
                    [-k | --key <key>] [-p | --pred <pred>] [-s | --succ <succ>]
                    [-v | --verbose]
        obsolete.py -h | --help

    Arguments:
        pid    PID of object to set obsolescence

    Options:
        -h --help   This page
        -n --node       Target node (either member or coordinating)
        -c --cert       Client certificate
        -k --key        Client certificate key
        -p --pred       Predecessor PID that current PID obsoletes
        -s --succ       Successor PID that current PID is obsoleted by
        -v --verbose    Display before/after system metadata

    """
    args = docopt(str(main.__doc__))

    if args['<pid>'] is not None:
        pid = args['<pid>']
    else:
        return 1

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

    pred = None
    if args['--pred']:
        pred = args['<pred>']

    succ = None
    if args['--succ']:
        succ = args['<succ>']

    verbose = False
    if args['--verbose']:
        verbose = True

    mn_client = MemberNodeClient_2_0(base_url=base_url,
                                     cert_pem_path=cert_pem_path,
                                     cert_key_path=cert_key_path,
                                     verify_tls=properties.VERIFY_TLS,
                                     )

    sm = mn_client.getSystemMetadata(pid=pid)

    if verbose:
        print('Before:')
        print(sm.toDOM().toprettyxml())

    changed = False
    if pred is not None:
        sm.obsoletes = pred
        changed = True
    if succ is not None:
        sm.obsoletedBy = succ
        changed = True

    if changed:
        mn_client.updateSystemMetadata(pid=pid,sysmeta_pyxb=sm)
        if verbose:
            sm = mn_client.getSystemMetadata(pid=pid)
            print('After:')
            print(sm.toDOM().toprettyxml())
    else:
        logger.warning('No changes detected')

    return 0


if __name__ == "__main__":
    main(sys.argv)