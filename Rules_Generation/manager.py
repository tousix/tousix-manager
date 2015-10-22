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

from Database.models import Hote, Regles
from Rules_Generation.configuration import Peer
from Rules_Generation.groups import groups
from Rules_Generation.Production.manager import Manager as Production
from Rules_Generation.Statistics.manager import Manager as Statistics
import json

class Manager(object):
    """
    Main class for managing the core of Generate_rues app
    """
    def get_peers(self, switch):
        """
        This method creates a list of peers seen by the given switch (only valid peers)
        :param switch: Switch model
        :return list(Peer): Peer array
        """
        hotes = Hote.objects.filter(valid=True)
        peers = []
        for hote in hotes:
            peer = Peer()

            peer.idPeer = hote.idhote
            peer.Name = hote.nomhote
            peer.Mac = hote.machote
            peer.IPv6 = hote.ipv6hote
            peer.IPv4 = hote.ipv4hote
            if hote.idport.idswitch == switch:
                peer.Egress = True
                peer.outputPort = hote.idport.numport
            else:
                # TODO parcours chemin à étudier ?
                peer.Egress = False
                peer.nextHop = hote.idport.idswitch_id

            peers.append(peer)
        return peers

    def create_rules(self, switches):
        """
        Insert into the database a new set of rules generated .
        :param switches: list(Switch)
        :return:
        """
        for switch in switches:
            peers = self.get_peers(switch)
            rules = self.call_managers(switch.idswitch, peers)

            # Remove existing rules for this switch
            Regles.objects.filter(idswitch=switch.idswitch).filter(etat="Production").delete()
            db_rules = []
            for rule in rules:
                db_rules.append(Regles(idswitch=switch, typeregle=rule.get("module"), regle=json.dumps(rule.get("rule")),
                                       source_id=rule.get("source"), destination_id=rule.get("destination")))
            Regles.objects.bulk_create(db_rules)
            # Copy raw group rules into database
            groups_switch = groups.groups[switch.idswitch]
            db_groups = []
            for group in groups_switch:
                db_groups.append(Regles(idswitch=switch, typeregle="Group", regle=json.dumps(group)))
            Regles.objects.bulk_create(db_groups)

    def call_managers(self, dpid, peers):
        """
        Method for calling managgers of other modules.
        :param dpid: Target DPID
        :param peers: LIst Peer
        :return:
        """
        rules = []

        production = Production()
        statistics = Statistics()
        rules.extend(production.create_rules_members(dpid, peers))
        rules.extend(statistics.create_rules_members(dpid, peers))

        return rules

