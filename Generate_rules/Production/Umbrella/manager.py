# -*- coding: utf8 -*-
__author__ = 'remy'


from Generate_rules.Production.Umbrella.ipv4 import IPv4
from Generate_rules.Production.Umbrella.ipv6 import IPv6

class Manager(object):
    """
    Manager class for creating Umbrella rules.
    """
    def create_rules(self, dpid, peer):
        """
        Create Umbrella rules.
        :param dpid: Target DPID
        :type dpid: int
        :param member: Peer object
        :type member: Peer
        :return: Flow rules array
        """
        ipv6 = IPv6()
        ipv4 = IPv4()
        rules = []
        rule = {"module": "Production_Umbrella_IPv6",
                "rule": ipv6.create_umbrella(dpid, peer)}
        rules.append(rule)
        rule = {"module": "Production_Umbrella_IPv4",
                "rule": ipv4.create_umbrella(dpid, peer)}
        rules.append(rule)
        return rules
