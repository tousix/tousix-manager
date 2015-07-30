# -*- coding: utf8 -*-
__author__ = 'remy'

import requests
import json
from database.models import Regles
from django.db.models import Q


class RulesDeployment(object):

    host = "http://127.0.0.1:8080"

    def send_rules(self, switches):
        success = 0
        fails = 0
        for switch in switches:
            rules = Regles.objects.filter(idswitch=switch)
            groups = rules.filter(typeregle="Group")
            flows = rules.exclude(typeregle="Group")
            stat_groups = self.send_group_rules(groups)
            stat_flows = self.send_flow_rules(flows)
            success += (stat_flows["success"] + stat_groups["success"])
            fails += (stat_flows["fails"] + stat_groups["fails"])
        return {"success": success,
                "fails": fails}

    def send_group_rules(self, rules):
        success = 0
        fails = 0
        for group in rules:
            request = requests.post(self.host+"/stats/groupentry/add", json=json.loads(group.regle))
            if request.status_code is not 200:
                fails += 1
            else:
                success += 1
        return {"success": success,
                "fails": fails}

    def send_flow_rules(self, rules):
        success = 0
        fails = 0
        for flow in rules:
            request = requests.post(self.host+"/stats/flowentry/add", json=json.loads(flow.regle))
            if request.status_code is not 200:
                fails += 1
            else:
                success += 1
        return {"success": success,
                "fails": fails}

    def remove_rules(self, rules):
        success = 0
        fails = 0
        for rule in rules:
            # strict comparaison
            request = requests.post(self.host+"/stats/flowentry/delete_strict", json=json.loads(rule.regle))
            if request.status_code is not 200:
                fails += 1
            else:
                success += 1
        return {"success": success,
                "fails": fails}

    def remove_host(self, hosts):
        rules = []
        for host in hosts:
            regles = Regles.objects.filter(Q(source=host) | Q(destination=host))
            rules.extend(regles)
        self.remove_rules(rules)
