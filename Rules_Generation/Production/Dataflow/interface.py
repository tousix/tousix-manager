# -*- coding: utf8 -*-
__author__ = 'remy'

from Rules_Generation.configuration import configuration as conf
from Rules_Generation.configuration import Peer

class interface(object):
    """
    Interface for generating productions rules. It should never be used, only inherited.
    """
    def create_dataflow(self, dpid, peer):
        """
        Create a complete flow rule based on an DPID and a member object
        :param dpid: Target DPID
        :type dpid: int
        :param peer:Peer object
        :type peer: Peer
        :return: rule
        :raises Baseexception: Not a Peer type
        """
        if isinstance(peer, Peer) is False:
            raise BaseException("Not a Peer type")
        rule = {
            "cookie": self.forge_cookie(peer.idPeer),
            "priority": self.find_priority(),
            "table_id": 0,
            "dpid": dpid,
            "match": self.get_match(peer.Mac),

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
        return conf.groups[dpid]

    def find_priority(self):
        """
        Find the priority for dataflow rules on the config file.
        :return: priority
        """
        return conf.priority["Production"].get("Dataflow")

    def forge_cookie(self, idpeer):
        """
        Forge a cookie number based on Peer ID (the first 1024 numbers are reserved).
        :param idpeer: Peer ID
        :type idpeer: int
        :return: cookie
        """
        return idpeer + 1024

    def get_action_output(self, type_output, port_number=1, next_dpid=1):
        """
        Create action object based on the type of output.
        :param type_output: GROUP or OUTPUT
        :type type_output: str
        :param port_number: Output Port number (optionnal when type_output=GROUP)
        :type port_number: int
        :param next_dpid: DPID of the next hop (optionnal when type_output=OUTPUT)
        :type next_dpid: int
        :returns: Action array
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
        :return: Action object
        """
        action = {"table_id": tableid,
                  "type": "GOTO_TABLE"}
        return action

    def get_match(self, mac):
        """
        Forge match object.
        :param mac: Destination MAC address
        :type mac: str
        :return: Match object
        """
        return {"dl_dst": mac}
