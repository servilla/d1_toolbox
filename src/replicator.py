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

from d1_client.mnclient_2_0 import MemberNodeClient_2_0
import d1_common.types.exceptions
import d1_common.types.dataoneTypes_v2_0 as dataoneTypes_v2_0
import daiquiri
from docopt import docopt

import properties

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger('replicator.py: ' + __name__)


def get_local_object(pid_file=None):
    pass


def get_remote_object():
    pass


def get_object(pid=None, src=None):
    src_mn = src['src_mn']
    if src_mn[0] == '/':
        # Local directory
        pid_file = src_mn + '/' + pid
        return open(pid_file, 'rb')
    else:
        return get_remote_object()


def get_sys_meta(pid=None, src=None):
    src_mn = src['src_mn']
    if src_mn[0] == '/':
        # Local directory
        sys_meta_file = src_mn + '/' + pid + '.xml'
        with open(sys_meta_file, 'rt') as f:
            xml_text = f.read()
        return dataoneTypes_v2_0.CreateFromDocument(xml_text=xml_text)
    else:
        return get_remote_object()


def replicate_object(pid=None, obj=None, sys_meta=None):
    mn_client = MemberNodeClient_2_0(base_url=properties.BASE_URL,
                                     cert_pem_path=properties.CERT_PEM,
                                     cert_key_path=properties.CERT_KEY,
                                     verify_tls=properties.VERIFY_TLS,
                                     )
    mn_client.create(pid=pid, obj=obj, sysmeta_pyxb=sys_meta)
    return 0


def modify_sys_meta(sys_meta=None):
    sys_meta.replicationPolicy.numberReplicas = 0
    sys_meta.replicationPolicy.replicationAllowed=False
    sys_meta.replica = None
    sys_meta.authoritativeMemberNode = 'urn:node:EDI'
    sys_meta.submitter = 'CN=urn:node:EDI,DC=dataone,DC=org'
    sys_meta.dateSysMetadataModified = None
    sys_meta.obsoletes = None
    sys_meta.obsoletedBy = None


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
            with open(args['<file>'], 'rt') as f:
                for pid in f:
                    pids.append(pid.strip())
        except IOError as e:
            logger.error(e)
            return 1

    src_mn = args['<src_mn>']
    if args['--cert'] and args['--key']:
        src_cert = args['<cert>']
        src_key = args['<key>']
    else:
        src_cert = None
        src_key =None

    src = {'src_mn': src_mn, 'src_cert': src_cert, 'src_key': src_key}

    logger.info(len(pids))
    cnt = 0
    for pid in pids:
        cnt += 1
        information = '{cnt}: {pid}'.format(cnt=cnt, pid=pid)
        logger.info(information)
        obj = get_object(pid=pid, src=src)
        sys_meta = get_sys_meta(pid=pid, src=src)
        modify_sys_meta(sys_meta=sys_meta)
        try:
            replicate_object(pid=pid, obj=obj, sys_meta=sys_meta)
        except d1_common.types.exceptions.DataONEException as e:
            logger.error(e)



    return 0


if __name__ == "__main__":
    main(sys.argv)