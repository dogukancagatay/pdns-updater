#!/usr/bin/env python3

import abc


class DynamicDnsProviderInterface(metaclass=abc.ABCMeta):
    """DNS Provider Meta class
    """
    @classmethod
    def __subclasscheck__(cls, subclass):
        return (
            hasattr(subclass, 'get_dns') and callable(subclass.get_dns)
        )

    @abc.abstractmethod
    def get_dns(self):
        """Provides DNS names with their host ip addresses"""
        raise NotImplementedError


class DynamicDnsRecord:

    def __init__(self, dns_names: list, host_ips: list, domain: str = None):
        self.dns_names = []

        for dns_name in dns_names:
            if dns_name:
                self.dns_names.append(dns_name)

        self.host_ips = host_ips[:]
        self.domain = domain

    def get_dns_names(self):
        return self.dns_names[:]

    def get_host_ips(self):
        return self.host_ips[:]

    def get_domain(self):
        return self.domain

    def __str__(self):
        return f"DynamicDnsRecord(dns_names={self.dns_names}, host_ips={self.host_ips}, domain={self.domain})"
