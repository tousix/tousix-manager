# -*- coding: utf8 -*-
__author__ = 'remy'

from Generate_rules.Statistics.interface import Interface
from Generate_rules.configuration import Peer

class IPv6(Interface):
    """
    Specialized class for creating IPv6 Statistics rules.
    """
    def create_stat(self, dpid, peer_src, peer_dst):
        """
        Create IPv6 statistic rule.
        :param dpid: Target DPID
        :type dpid: int
        :param peer_src: Source member object
        :type peer_src: Peer
        :param peer_dst: Destination member object
        :type peer_dst: Peer
        :return: statistic flow rule
        :raises BaseException: Not a Peer type
        """
        if (isinstance(peer_dst, Peer) & isinstance(peer_src, Peer)) is False:
            raise BaseException("Not a Peer type")
        rule = {"priority": self.find_priority("IPv6"),
                "cookie": self.forge_cookie(peer_src.idPeer, peer_dst.idPeer),
                "table_id": self.set_table_id(),
                "match": self.get_match(peer_src.IPv6, peer_dst.IPv6),
                "dpid": dpid}
        return rule

    def get_match(self, ip_src, ip_dst):
        """
        Create match object.
        :param ip_dst: Destination IPv6 address
        :type ip_dst: str
        :param ip_src: Source IPv6 address
        :type ip_src: str
        :return: Match object
        """
        match = {"dl_type": 34525,
                 "ipv6_src": ip_src,
                 "ipv6_dst": ip_dst}
        return match
