#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: replicator

:Synopsis:
 
:Author:
    servilla

:Created:
    10/24/17
"""

import sys
import logging

from docopt import docopt
import daiquiri

import properties

daiquiri.setup(level=logging.INFO)

logger = daiquiri.getLogger('replicator.py: ' + __name__)


def get_object(pid=None, src=None):
    pass


def get_sys_meta(pid=None, src=None):
    pass


def replicate_object(pid=None, obj=None, sys_meta=None, dst=None):
    pass


def main(argv):
    """A DataONE tool to manually replicate content from one node to another

    Replicates objects, including system metadata, from one DataONE member
    node to another member node, with the option of modifying system metadata
    attributes. It is assumed that the destination member node base URL,
    certificate, and private key are specified in the properties.

    Usage:
        replicator.py   pid <pid> <src_mn> [-c | --cert <cert>]
                        [-k | --key <key>]
        replicator.py   file <file> <src_mn> [-c | --cert <cert>]
                        [-k | --key <key>]
        replicator.py   defaults
        replicator.py   -h | --help

    Arguments:
        pid             Pid of object to replicate
        file            File of pids of objects to replicate one per line
        src_mn          Base URL of the source member node (or path on local
                        file system from / where objects reside)
        defaults        Prints default properties to stdout

    Options:
        -h --help       This page
        -c --cert       Client certificate of source member node (if needed to
                        access private content)
        -k --key        Client private key of source member node (if needed to
                        access private content)


    """
    args = docopt(str(main.__doc__))

    if args['defaults']:
        properties.dump()
        return 0

    pids = []
    if args['pid']:
        pids.append(args['<pid>'])
    else:
        try:
            f = open(args['<file>'], 'r')
        except IOError as e:
            logger.error(e)
            return 1
        for pid in f:
            pids.append(pid.strip())

    src_mn = args['<src_mn>']
    if args['--cert'] and args['--key']:
        src_cert = args['<cert>']
        src_key = args['<key>']
    else:
        src_cert = None
        src_key =None

    src = {'src_mn': src_mn, 'src_cert': src_cert, 'src_key': src_key}
        
    dst_mn = properties.BASE_URL
    dst_cert = properties.CERT_PEM
    dst_key = properties.CERT_KEY

    dst = {'dst_mn': dst_mn, 'dst_cert': dst_cert, 'dst_key': dst_key}

    for pid in pids:
        obj = get_object(pid=pid, src=src)
        sys_meta = get_sys_meta(pid=pid, src=src)
        replicate_object(pid=pid, obj=obj, sys_meta=sys_meta, dst=dst)



    return 0


if __name__ == "__main__":
    main(sys.argv)