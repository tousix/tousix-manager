# -*- coding: utf8 -*-
__author__ = 'remy'


from Generate_rules.Production.Umbrella.ipv4 import IPv4
from Generate_rules.Production.Umbrella.ipv6 import IPv6
from Generate_rules.configuration import configuration as conf

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
        if (conf.enabled["Production"].get('Umbrella').get('IPv6')) is True:
            rule = {"module": "Production_Umbrella_IPv6",
                    "rule": ipv6.create_umbrella(dpid, peer),
                    "source": None,
                    "destination": peer.idPeer}
            rules.append(rule)
        if (conf.enabled["Production"].get('Umbrella').get('IPv4')) is True:
            rule = {"module": "Production_Umbrella_IPv4",
                    "rule": ipv4.create_umbrella(dpid, peer),
                    "source": None,
                    "destination": peer.idPeer}
            rules.append(rule)
        return rules
