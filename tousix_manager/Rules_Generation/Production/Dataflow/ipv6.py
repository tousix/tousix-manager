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
from tousix_manager.Rules_Generation.configuration import Peer
from tousix_manager.Rules_Generation.Production.Dataflow.interface import interface


class IPv6(interface):
    def create_dataflow(self, dpid):
        rules = []
        # Create rule for any member IPv6 multicast packet
        rule = {
            "cookie": 66,
            "priority": self.find_priority("incoming"),
            "table_id": 0,
            "dpid": dpid,
            "match": self.get_match_normal(),
        }
        rule["actions"] = self.get_action_output("GROUP", type_match="incoming", dpid=dpid)
        rules.append(rule)

        # Create rules for forwarded packets
        for match in self.get_match_forwarded(None): #TODO define ports links
            rule = {
                "cookie": 67,
                "priority": self.find_priority("forwarded"),
                "table_id": 0,
                "dpid": dpid,
                "match": match,
            }
            rule["actions"] = self.get_action_output("GROUP",type_match="forwarded", dpid=dpid)

            rules.append(rule)
        return rules

    def find_priority(self, type_match):
        # prioritize rule with in_port match first, then match on any incoming packet
        dataflow = self.priority["Production"].get("Dataflow")
        if type_match is "incoming":
            return dataflow.get("IPv6") + 1
        elif type_match is "forwarded":
            return dataflow.get("IPv6")
        else:
            raise NotImplementedError

    def get_match_normal(self):
        return {"dl_dst": "33:33:00:00:00:00/ff:ff:00:00:00:00"}

    def get_match_forwarded(self, group_ports):
        matches = []
        for port in group_ports:
            match = {"dl_dst": "33:33:00:00:00:00/ff:ff:00:00:00:00"}
            match["in_port"] = port
            matches.append(match)
        return matches

    def get_action_output(self, type_output, type_match, dpid=1):
        """
        Create action object based on the type of output.
        :param type_output: GROUP or OUTPUT
        :type type_output: str
        :param type_match: Type of matching rule
        :type type_match: str
        :param dpid: DPID of the current switch (optionnal when type_output=OUTPUT)
        :type dpid: int
        :returns: Action array
        """

        if type_output == "GROUP":
            actions = []
            if type_match is "incoming":
                for group in self.find_dst_group([dpid]):
                    actions.append({"group_id": group, "type": "GROUP"})
            elif type_match is "forwarded":

            else:
                raise NotImplementedError
            return actions
        else:
            raise NotImplementedError

    def find_dst_group(self, dpids):
        """
        Return all groups except the ones defined in parameter
        :param dpids: DPIDs to ignore
        :type dpids: list(int)
        :return: group_id
        """
        group_id = []
        for k, v in self.groups.items():
            if k not in dpids:
                group_id.append(v)
        return group_id