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

from django.conf import settings
from Rules_Generation.configuration import Peer


class Interface(object):
    """
    Interface for creating Umbrella rules. It should never be used, only inherited.
    """
    def __init__(self):
        self.priority = settings.RULES_GENERATION_PRIORITIES
        self.groups = settings.RULES_GENERATION_GROUPS

    def create_umbrella(self, dpid, peer):
        """
        Create an Umbrella rule based on DPID and a Peer object
        :param dpid: Target DPID
        :type dpid: int
        :param peer: Peer object
        :type peer: Peer
        :return: Umbrella flow rule
        :raise BaseException: Not a Peer type
        """
        if isinstance(peer, Peer) is False:
            raise BaseException("Not a Peer type")
        rule = {
            "cookie": self.forge_cookie(peer.idPeer),
            "priority": self.find_priority("IPv4"),
            "table_id": 0,
            "dpid": dpid,
            "match": self.get_match(match_ipv4=peer.IPv4),

        }
        if peer.Egress is True:
            rule["actions"] = self.get_action_output("OUTPUT", port_number=peer.outputPort)
        else:
            rule["actions"] = self.get_action_output("GROUP", next_dpid=peer.nextHop)
        return rule

    def find_dst_group(self, dpid):
        """
        Convert any dpid into corresponding group_id for fast failover management.
        :param dpid: Target DPID
        :type dpid: int
        :return: group_id
        """
        return self.groups[dpid]

    def find_priority(self, type):
        """
        Find the priority for dataflow rules on the config file.
        :param type: Parameter name
        :type type: str
        :returns: priority
        """
        umbrella = self.priority["Production"].get("Umbrella")
        return umbrella[type]

    def forge_cookie(self, idmember):
        """
        Forge a cookie number based on Peer ID (the first 1024 numbers are reserved).
        :param idmember:Peer ID
        :type idmember: int
        :return: cookie
        """
        return idmember + 1024

    def get_action_output(self, type_output, port_number=1, next_dpid=1):
        """
        Create action object based on the type of output.
        :param type_output: GROUP or OUTPUT
        :type type_output: str
        :param port_number: Output Port number (optionnal when type_output=GROUP)
        :type port_number: int
        :param next_dpid: DPID of the next hop (optionnal when type_output=OUTPUT)
        :type next_dpid: int
        :return: action array
        """
        if type_output == "OUTPUT":
            action = [
                    {"type": "OUTPUT",
                     "port": port_number},
                    self.get_goto_table(1)
            ]
        elif type_output == "GROUP":
            action = [{"group_id": self.find_dst_group(next_dpid),
                                   "type": "GROUP"}
            ]
        return action

    def get_goto_table(self, tableid):
        """
        Return an GOTO_TABLE action based on table_id. Should never be used directly.
        :param tableid: TABLE ID
        :type tableid: int
        :return: action object
        """
        action = {"table_id": tableid,
                  "type": "GOTO_TABLE"}
        return action

    def get_match(self, match_ipv4=None, match_ipv6=None):
        """
        Forge match object.
        :param match_ipv4: Matching IPv4 address
        :type match_ipv4: str
        :param match_ipv6: Matching IPv6 address
        :type match_ipv6: str
        :return: match object
        :raise NotImplementedError: This method needs an implementation.
        """
        raise NotImplementedError('This method needs an implementation.')
