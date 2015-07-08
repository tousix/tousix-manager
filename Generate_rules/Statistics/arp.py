# -*- coding: utf8 -*-
__author__ = 'remy'

from Generate_rules.Statistics.interface import Interface

class ARP(Interface):
    """
    Specialized class for creating ARP Statistics rules.
    """
    def create_stat(self, dpid, peer_src, peer_dst):
        """
        Create ARP statistic rule.
        :param dpid: Target DPID
        :type dpid: int
        :param peer_src: Source member object (not used)
        :type peer_src: Peer
        :param peer_dst: Destination member object
        :type peer_dst: Peer
        :return: statistic flow rule
        :raises BaseException: Not a Peer type
        """
        rule = {"priority": self.find_priority("ARP"),
                "cookie": self.forge_cookie(peer_dst.idPeer),
                "table_id": self.set_table_id(),
                "match": self.get_match(peer_dst.IPv4),
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
        :param ip_dst: Target Ipv4 address
        :type ip_dst: str
        :return: Match object
        """
        match = {"dl_type": 2054,
                 "arp_op": 1,
                 "arp_tpa": ip_dst}
        return match


