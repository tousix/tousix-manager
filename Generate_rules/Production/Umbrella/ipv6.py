# -*- coding: utf8 -*-
__author__ = 'remy'

from Generate_rules.Production.Umbrella.interface import Interface

class IPv6(Interface):
    """
    Specialized class for creating IPv6 Umbrella rules.
    """
    def create_umbrella(self, dpid, peer):
        """
        Create an Umbrella rule based on DPID and a Peer object
        :param dpid: Target DPID
        :type dpid: int
        :param peer: Peer object
        :type peer: Peer
        :return: Umbrella flow rule
        :raises BaseException: Not a Peer type
        """
        rule = {
            "cookie": self.forge_cookie(peer.idPeer),
            "priority": self.find_priority("IPv6"),
            "table_id": 0,
            "dpid": dpid,
            "match": self.get_match(match_ipv6=peer.IPv6),

        }
        if peer.Egress is True:
            rule["actions"] = self.get_action_output("OUTPUT", port_number=peer.outputPort)
        else:
            rule["actions"] = self.get_action_output("GROUP", next_dpid=peer.nextHop)
        return rule

    def get_match(self, match_ipv4=None, match_ipv6=None):
        """
        Forge match object.
        :param match_ipv4: IPv4 target address (not used)
        :type match_ipv4: str
        :param match_ipv6: IPv6 target address
        :type match_ipv6: str
        :return: Match object
        :raises Exception: Bad use case for this class.
        """
        if match_ipv6 is None:
            raise Exception("Bad use case for this class.")
        match = {"dl_type": 34525,
                 "ip_proto": 58,
                 "ipv6_nd_target": match_ipv6,
                 "icmpv6_type": 135}

        return match