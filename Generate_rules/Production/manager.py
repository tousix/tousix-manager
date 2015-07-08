# -*- coding: utf8 -*-
__author__ = 'remy'

from Generate_rules.Production.Dataflow.manager import Manager as Dataflow
from Generate_rules.Production.Umbrella.manager import Manager as Umbrella

class Manager(object):
    """
    Manager class for creating production rules.
    """
    def create_rules_members(self, dpid, peers):
        """
        Create all the production rules needed for the members.
        :param dpid: Target DPID
        :type dpid: int
        :param members: Peer object array
        :type members: list(Peer)
        :return: flows rules array
        """
        rules = []
        dataflow = Dataflow()
        umbrella = Umbrella()
        for peer in peers:
            rules.extend(dataflow.create_rules(dpid, peer))
            rules.extend(umbrella.create_rules(dpid, peer))
        return rules
