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

from d1_client.mnclient_1_1 import MemberNodeClient_1_1
from d1_client.mnclient_2_0 import MemberNodeClient_2_0
from docopt import docopt
import lxml.etree as etree

import properties

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S%z',
                    #filename='$NAME' + '.log',
                    level=logging.INFO)

logger = logging.getLogger('peek')


def clean_pids(pids=None, dead_pids=None):
    for pid in dead_pids:
        if pid in pids:
            pids.pop(pid)


def pretty_xml(xml=None):
    root = etree.fromstring(xml)
    return etree.tostring(root, pretty_print=True)


def replicas(replicas=None):
    """
    Return list of all replicas in the format of: target node, status, and date
    completed.
     
    :param replicas:
    :type Pyxb replica class
    :return: String of replicas
    """
    replica_list = []
    for replica in replicas:
        replicaMemberNode = replica.replicaMemberNode.value()
        replicationStatus = replica.replicationStatus
        replicaVerified = str(replica.replicaVerified)
        replica_info = '"' + replicaMemberNode + ' ' + replicationStatus + ' ' + replicaVerified + '"'
        replica_list.append(replica_info)

    r = ''
    for replica in replica_list[:-1]:
        r += '{};'.format(replica)
    replica = replica_list[-1:][0]
    r += '{}'.format(replica)

    return r


def main(argv):
    """
    Peeks at a DataONE Member Node object's system metadata
    
    Usage: 
        peek.py pid <pid> [--v1] [-n | --node <node>] [-c | --cert <cert>] [-k | --key <key>] [-a | --attr <attr>] [--header] [--to_xml]
        peek.py file <file> [--v1] [-n | --node <node>] [-c | --cert <cert>] [-k | --key <key>] [-a | --attr <attr>] [--header] [--to_xml]
        peek.py defaults
        peek.py -h | --help

    Arguments:
        pid      Pid of object to peek
        file     File containing pid(s) (one per line) of objects to peek
        defaults Print default properties to stdout
                
    Options:
        -h --help   This page
        -n --node   Target node (either member or coordinating)
        -c --cert   Client certificate
        -k --key    Client certificate key
        -a --attr   Comma separated list of sysmeta attributes to display (none for all)
        --v1        Version 1 client (defaults to version 2)
        --header    Add header line
        --to_xml    Export as XML

    """
    args = docopt(str(main.__doc__))

    if args['defaults']:
        properties.dump()
        return 0

    pids = {}
    if args['pid']:
        pids[args['<pid>']] = {'pid': args['<pid>']}
    elif args['file']:
        with open(args['<file>'], 'r') as fn:
            pid_list = [_.strip() for _ in fn.readlines()]
            for pid in pid_list:
                pids[pid] = {'pid': pid}

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

    attributes = ()
    if args['--attr']:
        attributes = [ _.strip() for _ in args['<attr>'].split(',')]
    else:
        attributes = ['checksum', 'size', 'replica', 'archived', 'rights_holder']

    to_xml = False
    if args['--to_xml']:
        to_xml = True

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

    dead_pids = []
    for pid in pids:
        try:
            sm = client.getSystemMetadata(pid=pid)
            pids[pid]['xml'] = sm.toxml()
        except Exception as e:
            logger.error('{pid}: {e}'.format(pid=pid, e=e))
            dead_pids.append(pid)

        if 'checksum' in attributes:
            pids[pid]['checksum'] = sm.checksum.algorithm + ',' + sm.checksum.value()
        if 'size' in attributes:
            pids[pid]['size'] = sm.size
        if 'replica' in attributes:
            try:
                pids[pid]['replica'] = replicas(sm.replica)
            except Exception as e:
                pids[pid]['replica'] = ''
        if 'archived' in attributes:
            try:
                pids[pid]['archived'] = sm.archived
            except Exception as e:
                pids[pid]['archived'] = ''
        if 'rights_holder' in attributes:
            pids[pid]['rights_holder'] = '\'' + sm.rightsHolder.value() + '\''

    clean_pids(pids, dead_pids)

    for pid in pids:
        if to_xml:
            xml = pretty_xml(pids[pid]['xml'])
            print('{xml}'.format(xml=xml))
        else:
            print('{pid}'.format(pid=pid), end=',')
            if 'checksum' in attributes:
                checksum = pids[pid]['checksum']
                print('{checksum}'.format(checksum=checksum), end=',')
            if 'size' in attributes:
                size = pids[pid]['size']
                print('{size}'.format(size=size), end=',')
            if 'replica' in attributes:
                replica = pids[pid]['replica']
                print('{replica}'.format(replica=replica), end=',')
            if 'archived' in attributes:
                archived = pids[pid]['archived']
                print('{archived}'.format(archived=archived), end=',')
            if 'rights_holder' in attributes:
                rights_holder = pids[pid]['rights_holder']
                print('{rights_holder}'.format(rights_holder=rights_holder), end=', ')
            print()

    return 0


if __name__ == "__main__":
    main(sys.argv)