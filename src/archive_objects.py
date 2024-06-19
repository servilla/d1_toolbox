#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: archive_objects.py

:Synopsis:

:Author:
    servilla

:Created:
    9/6/18
"""
import logging
import sys

import daiquiri
from d1_client.mnclient_2_0 import MemberNodeClient_2_0
from d1_client.mnclient_1_2 import MemberNodeClient_1_2
from docopt import docopt

daiquiri.setup(level=logging.INFO,
               outputs=(
                   'stderr',
                   daiquiri.output.File(filename='archive_objects.log')
               ))

logger = daiquiri.getLogger(name=f'{__name__}')


def archive_pid(pid: str,
                base_url: str,
                cert_pem_path: str,
                cert_key_path: str,
                verify_tls: bool,
                mn_version: str = 'v2',
                ):
    if mn_version == 'v1':
        mn_client = MemberNodeClient_1_2(base_url=base_url,
                                         cert_pem_path=cert_pem_path,
                                         cert_key_path=cert_key_path,
                                         verify_tls=verify_tls,
                                         )
    else:  # v2
        mn_client = MemberNodeClient_2_0(base_url=base_url,
                                         cert_pem_path=cert_pem_path,
                                         cert_key_path=cert_key_path,
                                         verify_tls=verify_tls,
                                         )

    mn_client.archive(pid)


def main(argv):
    """
    Sets the object(s) in the given MN to archived.

    Usage:
        archive_objects.py pid <pid> base <base> cert <cert> key <key> [--v1] [--tls]
        archive_objects.py file <file> base <base> cert <cert> key <key> [--v1] [--tls]

    Arguments:
        pid     Pid of object to delete
        file    File containing pid(s) (one per line) of objects to delete
        base    The MN base URL
        cert    The MN client certificate
        key     The MN client certificate key

    Options:
        -h --help   This page
        --v1        Version 1 client (defaults to version 2)
        --tls       Verifies TLS connection (defaults to False)

    """
    args = docopt(str(main.__doc__))

    pids = []
    if args['pid']:
        pids.append(args['<pid>'])
    elif args['file']:
        with open(args['<file>'], 'r') as fn:
            pids = [_.strip() for _ in fn.readlines()]

    base_url = args['<base>']
    cert_pem_path = args['<cert>']
    cert_key_path = args['<key>']

    mn_version = 'v2'
    if args['--v1']:
        mn_version = 'v1'

    verify_tls = False
    if args['--tls']:
        verify_tls = True

    for pid in pids:
        try:
            archive_pid(pid, base_url, cert_pem_path, cert_key_path, verify_tls, mn_version)
            logger.info(f'Archived: "{pid}" at {base_url}')
        except Exception as e:
            logger.error(e)


if __name__ == "__main__":
    main(sys.argv)
