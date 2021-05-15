#!/usr/bin/env python3

import docker
from docker.client import DockerClient

import pdns_updater.logger as logging
from pdns_updater.dns_provider import DynamicDnsProviderInterface, DynamicDnsRecord

logger = logging.getLogger(__name__)


class DockerDnsProvider(DynamicDnsProviderInterface):

    def __init__(self, host_ips: list, base_dns_label="svc.dns"):
        self.client = docker.from_env()
        self.d = "dogukan"

        self.host_ips = host_ips
        self.base_dns_label = base_dns_label
        self.search_dns_label = base_dns_label + ".name"
        self.domain_dns_label = base_dns_label + ".domain"

        self.container_filter = {
            "status": "running",
            "label": [
                self.search_dns_label
            ],
        }

    def get_dns(self):
        containers_with_label = self.client.containers.list(filters=self.container_filter)

        logger.info(f"Number of containers with label: {len(containers_with_label)}")

        res = []

        for c in containers_with_label:

            if self.domain_dns_label in c.labels:
                domain = c.labels[self.domain_dns_label]
            else:
                domain = None

            res.append(DynamicDnsRecord(
                dns_names=c.labels[self.search_dns_label].split(","),
                host_ips=self.host_ips,
                domain=domain
            ))

        return res


if __name__ == "__main__":

    provider = DockerDnsProvider(host_ips=["192.168.12.12"])

    for dns_record in provider.get_dns():
        print(dns_record)
