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

import json

from tousix_manager.Rules_Generation.Production.manager import Manager as Production
from tousix_manager.Rules_Generation.configuration import Peer
from django.conf import settings

from tousix_manager.Database.models import Hote, Regles
from tousix_manager.Rules_Generation.Statistics.manager import Manager as Statistics


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
        hotes = Hote.objects.filter(valid=True).exclude(etat="Inactive")
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
        Insert into the database a new set of rules generated (groups included).
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
            groups_switch = settings.RULES_GENERATION_GROUPS_DEFINITION[switch.idswitch]
            db_groups = []
            for group in groups_switch:
                db_groups.append(Regles(idswitch=switch, typeregle="Group", regle=json.dumps(group)))
            Regles.objects.bulk_create(db_groups)

    def create_rules_single(self, switches, host):
        """
        Insert into the database a new set of rules generated for one host.
        :param switches: list(Switch)
        :param host: Host on which rules will be generated
        :return:
        """
        for switch in switches:
            peers = self.get_peers(switch)
            rules = self.call_managers_single(switch.idswitch, peers, host.idhote)

            # Remove existing rules for this switch
            Regles.objects.filter(idswitch=switch.idswitch).filter(etat="Production").exclude(typeregle="Group").delete()
            db_rules = []
            for rule in rules:
                db_rules.append(Regles(idswitch=switch, typeregle=rule.get("module"), regle=json.dumps(rule.get("rule")),
                                       source_id=rule.get("source"), destination_id=rule.get("destination")))
            Regles.objects.bulk_create(db_rules)

    def call_managers(self, dpid, peers):
        """
        Method for calling managers of other modules.
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

    def call_managers_single(self, dpid, peers, peer_id):
        """

        Method for calling managers of other modules.
        :param dpid: Target DPID
        :param peers: LIst Peer
        :param peer_id: Peer ID on which rules will be generated
        :return:
        """
        rules = []

        production = Production()
        statistics = Statistics()
        rules.extend(production.create_rules_member(dpid, peers, peer_id))
        rules.extend(statistics.create_rules_member(dpid, peers, peer_id))

        return rules
