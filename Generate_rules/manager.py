# -*- coding: utf8 -*-
__author__ = 'remy'

from database.models import Hote, Regles
from Generate_rules.configuration import Peer
from Generate_rules.groups import groups
from Generate_rules.Production.manager import Manager as Production
from Generate_rules.Statistics.manager import Manager as Statistics
import json

class Manager(object):

    def get_peers(self, switch):
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

        for switch in switches:
            peers = self.get_peers(switch)
            rules = self.call_managers(switch.idswitch, peers)

            # Remove existing rules for this switch
            Regles.objects.filter(idswitch=switch.idswitch).delete()
            db_rules = []
            for rule in rules:
                db_rules.append(Regles(idswitch=switch, typeregle=rule.get("module"), regle=json.dumps(rule.get("rule"))))
            Regles.objects.bulk_create(db_rules)
            # Copy raw group rules into database
            groups_switch = groups.groups[switch.idswitch]
            db_groups = []
            for group in groups_switch:
                db_groups.append(Regles(idswitch=switch, typeregle="Group", regle=json.dumps(group)).save())
            Regles.objects.bulk_create(db_groups)

    def call_managers(self, dpid, peers):
        rules = []

        production = Production()
        statistics = Statistics()
        rules.extend(production.create_rules_members(dpid, peers))
        rules.extend(statistics.create_rules_members(dpid, peers))

        return rules

