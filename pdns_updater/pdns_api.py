#!/usr/bin/env python3

import os
import logging
from typing import Sequence

import powerdns

import pdns_updater.logger as logging

logger = logging.getLogger(__name__)

PDNS_API_URL = os.getenv("PDNS_API_URL", "http://localhost:8081/api/v1")
PDNS_API_KEY = os.getenv("PDNS_API_KEY", "changeme")

api_client = powerdns.PDNSApiClient(api_endpoint=PDNS_API_URL, api_key=PDNS_API_KEY)
api = powerdns.PDNSEndpoint(api_client)


def get_or_create_zone(zone_domain):

    if zone_domain.endswith(".") == False:
        zone_domain += "."

    zone = api.servers[0].get_zone(zone_domain)

    if zone is None:
        logger.info(f"Will create zone: {zone_domain}")

        zone_nameservers = [
            "ns1." + zone_domain,
        ]

        zone = api.servers[0].create_zone(
            name=zone_domain,
            kind="Native",
            nameservers=zone_nameservers
        )

        logger.info(f"Zone created: {zone.name}")
        logger.info(zone.details)

    return zone


def extract_domain(dns_name):
    dns_name_split = dns_name.split(".")

    if dns_name.endswith("."):
        return dns_name_split[-3] + "." + dns_name_split[-2]
    else:
        return dns_name_split[-2] + "." + dns_name_split[-1]


def add_record(dns_names: Sequence[str], host_ips: Sequence[str], dns_domain: str = None):

    records = []

    for dns_name in dns_names:

        domain = extract_domain(dns_name) if dns_domain is None else dns_domain
        zone = get_or_create_zone(domain)

        logger.info(f"Add/update records for {dns_name} ({host_ips})")

        if dns_name.endswith(".") == False:
            dns_name += "."

        records.append(powerdns.RRSet(dns_name, 'A', host_ips))

    return zone.create_records(records)


def backup(base_dir="backups"):
    for server in api.servers:
        backup_dir = f"{base_dir}/{server.sid}"
        os.makedirs(backup_dir, exist_ok=True)

        for zone in server.zones:
            zone.backup(backup_dir)


if __name__ == "__main__":

    for zone in api.servers[0].zones:
        print(zone)
