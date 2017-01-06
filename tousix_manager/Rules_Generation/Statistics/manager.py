#    Copyright 2015 Rémy Lapeyrade <remy at lapeyrade dot net>
#    Copyright 2015 LAAS-CNRS
#
#
#    This file is part of TouSIX-Manager.
#
#    TouSIX-Manager is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    TouSIX-Manager is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with TouSIX-Manager.  If not, see <http://www.gnu.org/licenses/>.


from tousix_manager.Rules_Generation.Statistics.icmpv6 import ICMPv6
from tousix_manager.Rules_Generation.Statistics.ipv4 import IPv4
from tousix_manager.Rules_Generation.Statistics.ipv6 import IPv6
from django.conf import settings

from tousix_manager.Rules_Generation.Statistics.arp import ARP


class Manager(object):
    """
    Manager class for creating dataflow rules.
    """
    def create_rules_members(self, dpid, peers):
        """
        Create Statistics_Manager rules.
        :param dpid: Target DPID
        :type dpid: int
        :param peers: Peer object array
        :type peers: list(Peer)
        :return: Flow rules array
        """
        rules = []
        enabled = settings.RULES_GENERATION_ENABLED
        ipv4 = IPv4()
        ipv6 = IPv6()
        icmpv6 = ICMPv6()
        arp = ARP()

        for peer_dst in peers:
            if peer_dst.Egress is True:
                if enabled["Stats"].get('ICMPv6') is True:
                    rule = {"module": "Statistics_ICMPv6",
                            "rule": icmpv6.create_stat(dpid, None, peer_dst),
                            "source": None,
                            "destination": peer_dst.idPeer}
                    rules.append(rule)
                if enabled["Stats"].get('ARP') is True:
                    rule = {"module": "Statistics_ARP",
                            "rule": arp.create_stat(dpid, None, peer_dst),
                            "source": None,
                            "destination": peer_dst.idPeer}
                    rules.append(rule)

                for peer_src in peers:
                    if peer_src != peer_dst:
                        if enabled["Stats"].get('IPv6') is True:
                            rule = {"module": "Statistics_IPv6",
                                    "rule": ipv6.create_stat(dpid, peer_src, peer_dst),
                                    "source": peer_src.idPeer,
                                    "destination": peer_dst.idPeer}
                            rules.append(rule)
                        if enabled["Stats"].get('IPv4') is True:
                            rule = {"module": "Statistics_IPv4",
                                    "rule": ipv4.create_stat(dpid, peer_src, peer_dst),
                                    "source": peer_src.idPeer,
                                    "destination": peer_dst.idPeer}
                            rules.append(rule)
        rule = {
            "module": "Miss-table",
            "rule": ipv4.create_miss_table(dpid),
            "source": None,
            "destination": None
        }
        rules.append(rule)
        return rules

    def create_rules_member(self, dpid, peers, peer_id):
        """
        Create Statistics_Manager rules for one specific member.
        :param dpid: Target DPID
        :type dpid: int
        :param peers: Peer object array
        :type peers: list(Peer)
        :param peer_id: Peer ID on which rules will be generated
        :type peer_id: int
        :return: Flow rules array
        """
        rules = []
        enabled = settings.RULES_GENERATION_ENABLED
        ipv4 = IPv4()
        ipv6 = IPv6()
        icmpv6 = ICMPv6()
        arp = ARP()
        # forge new objects before generation
        peer_lst = []

        for peer_dst in peers:
            if peer_dst.idPeer is peer_id:
                peer_lst.append((None, peer_dst))
            for peer_src in peers:
                if peer_dst.idPeer is peer_id or peer_src.idPeer is peer_id:
                    peer_lst.append((peer_src, peer_dst))

        for peer_src, peer_dst in peer_lst:
            if peer_src is None:
                # only DST statistics
                if peer_dst.Egress is True:
                    if enabled["Stats"].get('ICMPv6') is True:
                        rule = {"module": "Statistics_ICMPv6",
                                "rule": icmpv6.create_stat(dpid, None, peer_dst),
                                "source": None,
                                "destination": peer_dst.idPeer}
                        rules.append(rule)
                    if enabled["Stats"].get('ARP') is True:
                        rule = {"module": "Statistics_ARP",
                                "rule": arp.create_stat(dpid, None, peer_dst),
                                "source": None,
                                "destination": peer_dst.idPeer}
                        rules.append(rule)
                continue
            if peer_src != peer_dst:
                if enabled["Stats"].get('IPv6') is True:
                    rule = {"module": "Statistics_IPv6",
                            "rule": ipv6.create_stat(dpid, peer_src, peer_dst),
                            "source": peer_src.idPeer,
                            "destination": peer_dst.idPeer}
                    rules.append(rule)
                if enabled["Stats"].get('IPv4') is True:
                    rule = {"module": "Statistics_IPv4",
                            "rule": ipv4.create_stat(dpid, peer_src, peer_dst),
                            "source": peer_src.idPeer,
                            "destination": peer_dst.idPeer}
                    rules.append(rule)
        rule = {
            "module": "Miss-table",
            "rule": ipv4.create_miss_table(dpid),
            "source": None,
            "destination": None
        }
        rules.append(rule)
        return rules