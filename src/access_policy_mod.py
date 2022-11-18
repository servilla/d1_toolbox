#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: access_policy_mod

:Synopsis:
    Access policy tools to modify an objects sysmeta access policy

:Author:
    servilla

:Created:
    10/8/20
"""
from pathlib import Path

import click
import daiquiri
import d1_client.cnclient_2_0
import d1_client.mnclient_2_0
import d1_common.wrap.access_policy
import requests

from config import Config


logger = daiquiri.getLogger(__name__)


def mn_client(base_url: str, cert_key: str, cert_pem: str):
    return d1_client.mnclient_2_0.MemberNodeClient_2_0(
        base_url=base_url,
        cert_pem_path=cert_pem,
        cert_key_path=cert_key,
        verify_tls=Config.VERIFY_TLS,
    )


def resolve_doi_node(doi: str):
    node = ""
    url = "https://doi.org/" + doi
    r = requests.get(url, allow_redirects=False)
    r.raise_for_status()
    location = r.headers["Location"]
    parameter = location.split("?")[1]
    pid = parameter.split("=")[1]
    scope = pid.split(".")[0]
    if scope == "edi":
        node = "/edi/"
    return node


def set_node(pid: str, prod: bool):
    if "doi:10.6073/pasta/" in pid:
        pid = resolve_doi_node(pid)
    if "/edi/" in pid:
        if prod:
            cert_key = Config.KEYS["EDI"]
            cert_pem = Config.CRTS["EDI"]
            base_url = "https://gmn.edirepository.org/mn"
        else:
            cert_key = Config.KEYS["EDI_S"]
            cert_pem = Config.CRTS["EDI_S"]
            base_url = "https://gmn-s.edirepository.org/mn"
    else:
        if prod:
            cert_key = Config.KEYS["LTER"]
            cert_pem = Config.CRTS["LTER"]
            base_url = "https://gmn.lternet.edu/mn"
        else:
            cert_key = Config.KEYS["LTER_S"]
            cert_pem = Config.CRTS["LTER_S"]
            base_url = "https://gmn-s.lternet.edu/mn"

    if not (Path(cert_key).exists() and Path(cert_pem).exists()):
        msg = f"Either {cert_key} or {cert_pem} does not exist"
        raise IOError(msg)

    return base_url, cert_key, cert_pem


prod_help = "Perform all modifications in the PRODUCTION environment"


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("source_type", nargs=1, required=True)
@click.argument("source", nargs=1, required=True)
@click.option("-p", "--prod", is_flag=True, default=False, help=prod_help)
def main(source_type: str, source: str, prod: bool):
    """
        Update object(s) access control rule section of system metadata.

        \b
            SOURCE_TYPE: Either "PID" or "FILE"
            SOURCE: Either the PID value or the name of file containing PIDs
    """

    if source_type not in ("PID", "FILE"):
        msg = f"SOURCE_TYPE must be either 'PID' or 'FILE'"
        print(msg)
        exit(1)

    if source_type == "FILE":
        if not Path(source).is_file():
            msg = f"FILE '{source}' not found"
            print(msg)
            exit(1)
        else:
            with open(source, "r") as f:
                pids = [_.strip() for _ in f.readlines()]
    else:
        pids = [source]

    for pid in pids:
        logger.info(pid)
        base_url, cert_key, cert_pem = set_node(pid=pid, prod=prod)
        client = mn_client(base_url, cert_key, cert_pem)
        sysmeta = client.getSystemMetadata(pid=pid)
        with d1_common.wrap.access_policy.wrap_sysmeta_pyxb(sysmeta) as ap:
            ap.add_public_read()
        client.updateSystemMetadata(pid=pid, sysmeta_pyxb=sysmeta)


if __name__ == "__main__":
    main()
