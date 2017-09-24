#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: poke

:Synopsis:
    Pokes at a DataONE object's system metadata
 
:Author:
    servilla

:Created:
    9/23/17
"""

from __future__ import print_function

import sys
import logging

import daiquiri
from d1_client.mnclient_1_1 import MemberNodeClient_1_1
from d1_client.mnclient_2_0 import MemberNodeClient_2_0
from docopt import docopt
import lxml.etree as etree

import properties


daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger('poke ' + __name__)


def mod_system_metadata(sysmeta=None):
    logger.info(sysmeta.authoritativeMemberNode.value())
    sysmeta.authoritativeMemberNode = 'urn:node:GLEON'
    logger.info(sysmeta.authoritativeMemberNode.value())
    return  sysmeta


def main(argv):
    """
    Pokes at a DataONE object's system metadata

    Usage:
        poke.py pid <pid>
        poke.py file <file>
        poke.py defaults

    Arguments:
        pid      Pid of object to poke
        file     File containing pid(s) (one per line) of objects to poke
        defaults Print default properties to stdout

    """
    args = docopt(str(main.__doc__))

    if args['defaults']:
        properties.dump()
        return 0

    pids = []
    if args['pid']:
        pids.append(args['<pid>'])
    elif args['file']:
        with open(args['<file>'], 'r') as fn:
            pid_list = [_.strip() for _ in fn.readlines()]
            for pid in pid_list:
                pids.append(pid)

    base_url = properties.BASE_URL
    cert_pem_path = properties.CERT_PEM
    cert_key_path = properties.CERT_KEY

    client = MemberNodeClient_2_0(base_url=base_url,
                                  cert_pem_path=cert_pem_path,
                                  cert_key_path=cert_key_path,
                                  verify_tls=properties.VERIFY_TLS,
                                  )

    for pid in pids:
        sysmeta = client.getSystemMetadata(pid=pid)
        mod_sysmeta = mod_system_metadata(sysmeta=sysmeta)
        client.updateSystemMetadata(pid=pid, sysmeta_pyxb=mod_sysmeta)

    return 0


if __name__ == "__main__":
    main(sys.argv)