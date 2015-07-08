# -*- coding: utf8 -*-
__author__ = 'remy'

from Generate_rules.Production.Dataflow.interface import interface

class Manager(interface):
    """
    Manager class for creating dataflow rules.
    """
    def create_rules(self, dpid, peer):
        rule = [{"module": "Production_Dataflow",
                "rule": self.create_dataflow(dpid, peer)}]
        return rule
