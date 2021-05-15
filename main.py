#!/usr/bin/env python3

import os
import asyncio
from typing import Sequence

from pdns_updater.docker_dns_provider import DockerDnsProvider
from pdns_updater.dns_provider import DynamicDnsProviderInterface

import pdns_updater.logger as logging
import pdns_updater.pdns_api as pdns_api

logging.setupLogger()
logger = logging.getLogger(__name__)


async def periodic(providers: Sequence[DynamicDnsProviderInterface], delay=60.0):
    while True:

        for i, dns_provider in enumerate(providers):

            logger.info(f"Periodic DNS provider check started for provider {i+1}")

            for dns_record in dns_provider.get_dns():

                pdns_api.add_record(
                    dns_record.get_dns_names(),
                    dns_record.get_host_ips(),
                    dns_domain=dns_record.get_domain()
                )

        await asyncio.sleep(delay)

if __name__ == "__main__":

    HOST_IP = os.getenv("HOST_IP", None)

    if HOST_IP is None:
        logger.error("Cannot start without HOST_IP environment variable")
        exit(1)

    loop = asyncio.get_event_loop()
    task = loop.create_task(periodic(providers=[
        DockerDnsProvider(host_ips=[HOST_IP])
    ], delay=3))

    try:
        loop.run_until_complete(task)
    except asyncio.CancelledError:
        pass
