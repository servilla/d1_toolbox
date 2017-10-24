#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: replicator

:Synopsis:
 
:Author:
    servilla

:Created:
    10/24/17
"""

import logging

from docopt import docopt
import daiquiri

import properties

daiquiri.setup(level=logging.INFO)

logger = daiquiri.getLogger(__name__)

def main():
    """A DataONE tool to manually replicate content from one node to another

    Replicates objects, including system metadata, from one DataONE member
    node to another member node, with the option of modifying system metadata
    attributes. It is assumed that the destination member node certificate and
    private key are specified in teh properties.

    Usage:
        replicator.py   pid <pid> <source_mn> <destination_mn> [-c | --cert <cert>] [-k | --key <key>]
        replicator.py   file <file> <source_mn> <destination_mn> [-c | --cert <cert>] [-k | --key <key>]
        replicator.py   defaults
        replicator.py   -h | --help

    Arguments:
        pid             Pid of object to replicate
        file            File of pids of objects to replicate
        source_mn       The source member node of the pid to replicate
        destination_mn  The destination member node of the pid to replicate
        defaults        Prints default properties to stdout

    Options:
        -h --help   This page
        -c --cert   Client certificate of source member node (if need to access private content)
        -k --key    Client private key of source member node (if need to access private content)


    """


    return 0


if __name__ == "__main__":
    main()