# -*- coding: utf8 -*-
__author__ = 'remy'

from Rules_Generation.Production.Umbrella.interface import Interface

class IPv4(Interface):
    """
    Specialized class for creating IPv4 Umbrella rules.
    """
    def get_match(self, match_ipv4=None, match_ipv6=None):
        """
        Forge match object.
        :param match_ipv4: IPv4 target address
        :type match_ipv4: str
        :param match_ipv6: IPv6 target address (not used)
        :type match_ipv6: str
        :return: Match object
        :raises Exception: Bad use case for this class.
        """
        if match_ipv4 is None:
            raise Exception("Bad use case for this class.")
        match = {"dl_type": 2054,
                 "arp_op": 1,
                 "arp_tpa": match_ipv4}
        return match
