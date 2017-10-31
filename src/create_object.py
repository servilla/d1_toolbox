#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: list_objects

:Synopsis:
 
:Author:
    servilla

:Created:
    1/26/17
"""

import sys
import os
import hashlib
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S%z', level=logging.WARN)

logger = logging.getLogger('create_object')

import requests
from docopt import docopt


from d1_client.mnclient_2_0 import MemberNodeClient_2_0
import d1_common.types.dataoneTypes_v2_0 as dataoneTypes_v2_0
import properties


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def build_sysmeta(pid=None, obj=None, fmt=None, sid=None):

    if pid is None:
        return 1
    if obj is None:
        return 1
    if fmt is None:
        fmt = 'application/octet-stream'

    obj_size = os.path.getsize(obj)
    obj_md5 = md5(obj)

    accessPolicy = dataoneTypes_v2_0.accessPolicy()
    accessRule = dataoneTypes_v2_0.AccessRule()
    accessRule.subject.append('gmn-local')
    accessRule.permission.append('changePermission')
    accessPolicy.append(accessRule)
    accessRule = dataoneTypes_v2_0.AccessRule()
    accessRule.subject.append('public')
    accessRule.permission.append('read')
    accessPolicy.append(accessRule)

    d1_sys_meta = dataoneTypes_v2_0.systemMetadata()
    d1_sys_meta.serialVersion = 1
    d1_sys_meta.identifier = pid
    d1_sys_meta.size = obj_size
    d1_sys_meta.formatId = fmt
    d1_sys_meta.rightsHolder = 'gmn-local'
    d1_sys_meta.checksum = obj_md5
    d1_sys_meta.checksum.algorithm = 'MD5'
    d1_sys_meta.accessPolicy = accessPolicy

    if sid is not None:
        d1_sys_meta.seriesId = sid
    
    return d1_sys_meta



def main(argv):
    """
    Creates a DataONE object in GMN.

    Usage:
        create_object.py <pid> <obj> [-f | --fmt <fmt>] [-s | --sid <sid>] [-u | --update <uid>]
        create_object.py (-h | --help)

    Arguments:
        pid    Persistent identifier of object
        obj    Path to object to be created in GMN

    Options:
        -h --help              This page
        -u --update <uid>      Perform an update of the previous 'update' pid (default is create)
        -f --fmt    <fmt>      Use the provided format identifier (default is 'application/octet-stream')
        -s --sid    <sid>      Use the provided series identifier (default is no series identifier)

    """

    args = docopt(str(main.__doc__))

    pid = args['<pid>']
    obj = args['<obj>']

    fmt = None
    sid = None
    uid = None

    if args['--fmt']:
        fmt = args['<fmt>']
    if args['--sid']:
        sid = args['<sid>']
    if len(args['--update']) > 0:
        uid = args['--update'][0]

    mn_client = MemberNodeClient_2_0(base_url=properties.BASE_URL,
                                     cert_pem_path=properties.CERT_PEM,
                                     cert_key_path=properties.CERT_KEY,
                                     verify_tls=properties.VERIFY_TLS,
                                     )

    sys_meta = build_sysmeta(pid=pid, obj=obj, fmt=fmt, sid=sid)
    fo = open(obj, mode='r')

    if uid is None:
        mn_client.create(pid=pid, obj=fo, sysmeta_pyxb=sys_meta)
    else:
        mn_client.update(pid=uid, obj=fo, newPid=pid, sysmeta_pyxb=sys_meta)

    return 0


if __name__ == "__main__":
    main(sys.argv)