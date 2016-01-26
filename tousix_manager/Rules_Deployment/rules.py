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

import requests
from django.db.models import Q

from tousix_manager.Database.models import Regles


class RulesDeployment(object):
    """
    Class used for communicate depluyment rules through the Ryu REST API.
    """
    host = "http://127.0.0.1:8080"

    def send_rules(self, switches):
        """
        Send all the rules present in the Database, groups first, then flows.

        :param switches: List of switches for rules deployment
        :return: HTTP statistics
        """
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
        """
        Method for sending group rules on HTTP.
        :param rules: Queryset containing group type rules
        :return: HTTP Statistics_Manager of the operation
        """
        success = 0
        fails = 0
        for group in rules:
            try:
                request = requests.post(self.host+"/stats/groupentry/add", json=json.loads(group.regle))
                if request.status_code is not 200:
                    fails += 1
                else:
                    success += 1
            except requests.ConnectionError:
                return{"success": 0,
                       "fails": 0
                       }
        return {"success": success,
                "fails": fails}

    def send_flow_rules(self, rules):
        """
        Method for sending flow rules on HTTP.
        :param rules: Queryset containing flow type rules
        :return: HTTP Statistics_Manager of the operation
        """
        success = 0
        fails = 0
        for flow in rules:
            try:
                request = requests.post(self.host+"/stats/flowentry/add", json=json.loads(flow.regle))
                if request.status_code is not 200:
                    fails += 1
                else:
                    success += 1
            except requests.ConnectionError:
                return{"success": 0,
                       "fails": 0
                       }
        return {"success": success,
                "fails": fails}

    def remove_rules(self, rules):
        """
        Removes rules via HTTP request.
        Warning : this method use strict comparisons for deleting rules,
        it is advised to use generated rules, or those written in the Database.
        :param rules: queryset of rules
        :return:
        """
        success = 0
        fails = 0
        for rule in rules:
            try:
                # strict comparaison
                request = requests.post(self.host+"/stats/flowentry/delete_strict", json=json.loads(rule.regle))
                if request.status_code is not 200:
                    fails += 1
                else:
                    success += 1
            except requests.ConnectionError:
                return{"success": 0,
                       "fails": 0
                       }
        return {"success": success,
                "fails": fails}

    def remove_host(self, hosts):
        """
        Remove list of hosts on the topology.
        :param hosts: host list
        :return:
        """
        rules = []
        for host in hosts:
            regles = Regles.objects.filter(Q(source=host) | Q(destination=host))
            rules.extend(regles)
        self.remove_rules(rules)
