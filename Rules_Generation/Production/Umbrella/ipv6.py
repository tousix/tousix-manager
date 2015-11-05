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

from Rules_Generation.Production.Umbrella.interface import Interface
from Rules_Generation.configuration import Peer


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
        if isinstance(peer, Peer) is False:
            raise BaseException("Not a Peer type")
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