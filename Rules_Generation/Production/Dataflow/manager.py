# -*- coding: utf8 -*-
__author__ = 'remy'

from Rules_Generation.Production.Dataflow.interface import interface

class Manager(interface):
    """
    Manager class for creating dataflow rules.
    """
    def create_rules(self, dpid, peer):
        rule = [{"module": "Production_Dataflow",
                "rule": self.create_dataflow(dpid, peer),
                 "source": None,
                 "destination": peer.idPeer}]
        return rule
