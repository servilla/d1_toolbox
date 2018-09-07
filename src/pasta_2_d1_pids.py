#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: pasta_2_d1_pids

:Synopsis:

:Author:
    servilla

:Created:
    9/6/18
"""
import logging
import sys

import daiquiri
from docopt import docopt
import requests

daiquiri.setup(level=logging.INFO,
               outputs=(
                   'stderr',
                   daiquiri.output.File(filename='pasta_2_d1_pids.log')
                ))

logger = daiquiri.getLogger(name=f'{__name__}')


def get_pasta_scopes(base_url: str) -> list:
    r = requests.get(f'{base_url}/eml')
    if r.status_code == requests.codes.OK:
        return [_.strip() for _ in r.text.split('\n')]


def get_pasta_identifiers(base_url: str, packages: list) -> list:
    _package = list()
    for scope in packages:
        r = requests.get(f'{base_url}/eml/{scope}')
        if r.status_code == requests.codes.OK:
            identifiers = [_.strip() for _ in r.text.split('\n')]
            for identifier in identifiers:
                _package.append(f'{scope}/{identifier}')
    return _package


def get_pasta_revisions(base_url: str, packages: list) -> list:
    _package = list()
    for scope_identifer in packages:
        r = requests.get(f'{base_url}/eml/{scope_identifer}')
        if r.status_code == requests.codes.OK:
            revisions = [_.strip() for _ in r.text.split('\n')]
            for revision in revisions:
                _package.append(f'{scope_identifer}/{revision}')
    return _package


def main(argv):
    """
    Lists all DataONE object pids for a given PASTA data package pid. PASTA
    package identifiers can be full or partial or none (all).

    Usage:
        pasta_2_d1_pids.py [-s | --scope <scope>] [-i | --identifier <identifier>] [-r | --revision <revision>] [-e | --env <env>]

    Options:
        -h --help        This page
        -s --scope       The scope of the PASTA package identifier
        -i --identifier  The identifier of the PASTA identifier
        -r --revision    The revision of the PASTA identifier
        -e --env         The PASTA environment being targeted (p, s, d)

    """
    args = docopt(str(main.__doc__))

    scope = None
    if args['--scope']:
        scope = args['<scope>']

    identifier = None
    if args['--identifier']:
        if scope is None:
            msg = 'Scope must not be None if identifier set'
            raise ValueError(msg)
        identifier = args['<identifier>']

    revision = None
    if args['--revision']:
        if scope is None or identifier is None:
            msg = 'Scope and identifier must not be None if revision set'
            raise ValueError(msg)
        revision = args['<revision>']

    env = 'p'
    base_url = 'https://pasta.lternet.edu/package/'
    if args['--env']:
        env = args['<env>']
        if env not in ('p', 's', 'd'):
            msg = 'PASTA environment must be one of p, s, or d'
            raise ValueError(msg)

    if env == 's':
        base_url = 'https://pasta-s.lternet.edu/package/'
    elif env == 'd':
        base_url = 'https://pasta-d.lternet.edu/package/'

    if scope is None:
        packages = get_pasta_scopes(base_url)
    else:
        packages = [scope]

    if identifier is None:
        packages = get_pasta_identifiers(base_url, packages)
    else:
        packages = [f'{scope}/{identifier}']

    if revision is None:
        packages = get_pasta_revisions(base_url, packages)
    else:
        packages = [f'{scope}/{identifier}/{revision}']

    for package in packages:
        r = requests.get(f'{base_url}/doi/eml/{package}')
        if r.status_code == requests.codes.ok:
            doi = r.text.strip()
            print(doi)
        r = requests.get(f'{base_url}/eml/{package}')
        if r.status_code == requests.codes.OK:
            pids = [_.strip() for _ in r.text.strip().split('\n')]
            for pid in pids[:-1]:
                print(pid)

    return 0


if __name__ == "__main__":
    main(sys.argv)
