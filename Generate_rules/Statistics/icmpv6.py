# -*- coding: utf8 -*-
__author__ = 'remy'
from Generate_rules.Statistics.interface import Interface

class ICMPv6(Interface):
    """
    Specialized class for creating ICMPv6 Statistics rules.
    """
    def create_stat(self, dpid, peer_src, peer_dst):
        """
        Create ICMPv6 statistic rule.
        :param dpid: Target DPID
        :type dpid: int
        :param peer_src: Source member object (not used)
        :type peer_src: Peer
        :param peer_dst: Destination member object
        :type peer_dst: Peer
        :return: statistic flow rule
        :raises BaseException: Not a Peer type
        """
        rule = {"priority": self.find_priority("ICMPv6"),
                "cookie": self.forge_cookie(peer_dst.idPeer),
                "table_id": self.set_table_id(),
                "match": self.get_match(peer_dst.IPv6),
                "dpid": dpid}
        return rule

    def forge_cookie(self, idpeer):
        """
        Create cookie.
        :param idpeer: Peer ID
        :type idpeer: int
        :return: cookie ID
        """
        return idpeer + 1024

    def get_match(self, ip_dst):
        """
        Create match object.
        :param ip_dst: Target Ipv6 address
        :type ip_dst: str
        :return: Match object
        """
        match = {"dl_type": 34525,
                 "ip_proto": 58,
                 "ipv6_nd_target": ip_dst,
                 "icmpv6_type": 135}
        return match
