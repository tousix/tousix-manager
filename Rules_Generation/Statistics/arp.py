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

class ARP(Interface):
    """
    Specialized class for creating ARP Statistics_Manager rules.
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
        cookie = 1024 << 32
        return  cookie + idpeer + 1024

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


