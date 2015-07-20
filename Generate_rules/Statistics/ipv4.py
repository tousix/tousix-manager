# -*- coding: utf8 -*-
__author__ = 'remy'


from Generate_rules.Statistics.interface import Interface
from Generate_rules.configuration import Peer

class IPv4(Interface):
    """
    Specialized class for creating IPv4 Statistics rules.
    """
    def create_stat(self, dpid, peer_src, peer_dst):
        """
        Create IPv4 statistic rule.
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
        rule = {"priority": self.find_priority("IPv4"),
                "cookie": self.forge_cookie(peer_src.idPeer, peer_dst.idPeer),
                "table_id": self.set_table_id(),
                "match": self.get_match(peer_src.Mac, peer_dst.Mac),
                "dpid": dpid}
        return rule

    def get_match(self, mac_src, mac_dst):
        """
        Create match object.
        :param mac_dst: Destination Mac address
        :type mac_dst: str
        :param mac_src: Source Mac address
        :type mac_src: str
        :return: Match object
        """
        match = {"dl_type": 2048,
                 "dl_dst": mac_dst,
                 "dl_src": mac_src}
        return match
