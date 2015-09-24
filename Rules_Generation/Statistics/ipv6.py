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

from Rules_Generation.Statistics.interface import Interface
from Rules_Generation.configuration import Peer

class IPv6(Interface):
    """
    Specialized class for creating IPv6 Statistics_Manager rules.
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
        match = {"dl_type": 34525,
                 "dl_src": mac_src,
                 "dl_dst": mac_dst}
        return match
