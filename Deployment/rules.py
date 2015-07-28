# -*- coding: utf8 -*-
__author__ = 'remy'

import requests
import json
from database.models import Regles

class RulesDeployment(object):

    def send_rules(self, switches):
        host = "http://127.0.0.1:8080"
        success = 0
        fails = 0
        for switch in switches:
            rules = Regles.objects.filter(idswitch=switch)
            groups = rules.filter(typeregle="Group")
            flows = rules.exclude(typeregle="Group")
            for group in groups:
                request = requests.post(host+"/stats/groupentry/add", json=json.loads(group.regle))
                if request.status_code is not 200:
                    fails += 1
                else:
                    success += 1
            for flow in flows:
                request = requests.post(host+"/stats/flowentry/add", json=json.loads(flow.regle))
                if request.status_code is not 200:
                    fails += 1
                else:
                    success += 1
        return {"success": success,
                "fails": fails}

    def remove_rules(self, switches):
        pass