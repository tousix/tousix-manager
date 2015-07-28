# -*- coding: utf8 -*-
__author__ = 'remy'


from Generate_rules.Statistics.arp import ARP
from Generate_rules.Statistics.icmpv6 import ICMPv6
from Generate_rules.Statistics.ipv6 import IPv6
from Generate_rules.Statistics.ipv4 import IPv4
from Generate_rules.configuration import configuration as conf
class Manager(object):
    """
    Manager class for creating dataflow rules.
    """
    def create_rules_members(self, dpid, peers):
        """
        Create Statistics rules.
        :param dpid: Target DPID
        :type dpid: int
        :param peers: Peer object array
        :type peers: list(Peer)
        :return: Flow rules array
        """
        rules = []
        ipv4 = IPv4()
        ipv6 = IPv6()
        icmpv6 = ICMPv6()
        arp = ARP()

        for peer_dst in peers:
            if peer_dst.Egress is True:
                if conf.enabled["Stats"].get('ICMPv6') is True:
                    rule = {"module": "Statistics_ICMPv6",
                            "rule": icmpv6.create_stat(dpid, None, peer_dst),
                            "source": None,
                            "destination": peer_dst.idPeer}
                    rules.append(rule)
                if conf.enabled["Stats"].get('ARP') is True:
                    rule = {"module": "Statistics_ARP",
                            "rule": arp.create_stat(dpid, None, peer_dst),
                            "source": None,
                            "destination": peer_dst.idPeer}
                    rules.append(rule)

                for peer_src in peers:
                    if peer_src != peer_dst:
                        if conf.enabled["Stats"].get('IPv6') is True:
                            rule = {"module": "Statistics_IPv6",
                                    "rule": ipv6.create_stat(dpid, peer_src, peer_dst),
                                    "source": peer_src.idPeer,
                                    "destination": peer_dst.idPeer}
                            rules.append(rule)
                        if conf.enabled["Stats"].get('IPv4') is True:
                            rule = {"module": "Statistics_IPv4",
                                    "rule": ipv4.create_stat(dpid, peer_src, peer_dst),
                                    "source": peer_src.idPeer,
                                    "destination": peer_dst.idPeer}
                            rules.append(rule)
        return rules
