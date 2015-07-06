# -*- coding: utf8 -*-
__author__ = 'remy'

from database.models import Hote, Regles

class Manager(object):

    def get_peers(self, switch):
        hotes = Hote.objects.filter(valid=True)
        peers = []
        for hote in hotes:
            peer = {"idhote": hote.idhote,
                    "nom": hote.nomhote,
                    "mac": hote.machote,
                    "ipv4": hote.ipv4hote,
                    "ipv6": hote.ipv6hote,
                    }
            if hote.idport.idswitch == switch:
                peer["egress"] = True
                peer["output"] = hote.idport.numport
            else:
                # TODO parcours chemin à étudier ?
                peer["egress"] = False
                peer["nexthop"] = hote.idport.idswitch_id

            peers.append(peer)
        return peers

    def create_rules(self, switches):

        for switch in switches:
            peers = self.get_peers(switch)
            rules = self.call_managers(peers)

            # Remove existing rules for this switch
            Regles.objects.filter(idswitch=switch.idswitch_id).delete()

            for rule in rules:
                db_rule = Regles(idswitch=switch.idswitch_id,regle=rule)
                db_rule.save()

    def call_managers(self, peers):
        return []
