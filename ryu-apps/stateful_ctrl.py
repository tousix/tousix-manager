# -*- coding: utf8 -*-

import logging
import requests
import json
import io

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller import dpset
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import ofctl_v1_3
from oslo_config import cfg

LOG = logging.getLogger('ryu.app.stateful_ctrl')


class StatefulCTRL(app_manager.RyuApp):
    def __init__(self, *args, **kwargs):
        super(StatefulCTRL, self).__init__(*args, **kwargs)
        if self.load_config() is True:
            self.is_verifying = {}

    def load_config(self):
        # Test ouverture fichier
        try:
            self.CONF.register_group(cfg.OptGroup(name='stateful',
                                     title='Stateful controller options'))
            self.CONF.register_opts([
                                    cfg.StrOpt('filepath'),
                                    cfg.StrOpt('server'),
                                    cfg.IntOpt('timeout'),
                                    cfg.BoolOpt('enable')
                                    ], 'stateful')

            if self.CONF.stateful.enable is False:
                LOG.warn("Application Contrôleur stateful désactivé")
                self.stop()
            self.filepath = self.CONF.stateful.filepath
            file_test = io.open(self.filepath, mode='r')
            file_test.close()
        except AttributeError:
            LOG.error("Erreur : Chemin de fichier invalide")
            self.stop()
            return False
        except cfg.NoSuchOptError:
            LOG.error("Erreur : Fichier de configuration invalide")
            self.stop()
            return False
        return True

    @set_ev_cls(ofp_event.EventOFPStateChange, MAIN_DISPATCHER)
    def _event_switch_hello_handler(self, ev):
        LOG.info("Le switch n° "+str(ev.datapath.id)+" a changé de statut.")
        datapath = ev.datapath
        ofp = datapath.ofproto
        ofp_parser = datapath.ofproto_parser

        cookie = cookie_mask = 0
        match = ofp_parser.OFPMatch()
        req = ofp_parser.OFPFlowStatsRequest(datapath, 0,
                                             0,
                                             ofp.OFPP_ANY, ofp.OFPG_ANY,
                                             cookie, cookie_mask,
                                             match)
        self.is_verifying[datapath.id] = True
        datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _event_switch_connection_handler(self, ev):
        if self.is_verifying.get(ev.msg.datapath.id, False) is False:
            return None
        # count flow rules on table 0
        dp = ev.msg.datapath
        count = 0
        for stats in ev.msg.body:
            if stats.table_id is 0:
                count += 1
        # Server verification
        server = self.CONF.stateful.server.translate(None, '\'\"[]')
        try:
            requests.get(server, timeout=self.CONF.stateful.timeout)
        except requests.ConnectionError:
            LOG.warning("Server " + server + " not reachable, ignoring url defined")
            server = None
        except requests.Timeout:
            LOG.warning("Server " + server + " timed out")
            server = None
        if server is not None:
            response = requests.get(server + "/deployment/rules/ask", params={"idswitch": dp.id})
            try:
                data = response.json()
            except ValueError:
                LOG.error("Erreur de récupération de l'objet JSON.")
                return None
            filtre = filter(lambda rule: rule.get("table_id", None) is 0, data)
            if filtre.__len__() is not count:
                LOG.info("Nombre de règles sur "+str(dp.id)+" différent de la base de données")
                self._restore_rules(self, dp, data)
            else:
                LOG.info("Pas de modification à apporter sur le switch n° "+str(dp.id))
        else:
            deseria = DeserializeJSON()

            rules = list()
            if deseria.verify_instuctions(self.filepath, dp.id, count, rules) is False:
                LOG.info("Nombre de règles sur "+str(dp.id)+" différent du fichier de configuration")
                self._restore_rules(self, dp, rules)
            else:
                LOG.info("Pas de modification à apporter sur le switch n° "+str(dp.id))
        self.is_verifying[dp.id] = False

    @staticmethod
    def _restore_rules(self, dp, rules):
        LOG.info("Restauration des règles de "+str(dp.id)+" en cours...")
        flows = filter(lambda rule: "buckets" not in rule, rules)
        groups = filter(lambda rule: "buckets" in rule, rules)
        for rule in groups:
            ofctl_v1_3.mod_group_entry(dp, rule, dp.ofproto.OFPGC_ADD)
        for rule in flows:
            ofctl_v1_3.mod_flow_entry(dp, rule, dp.ofproto.OFPFC_ADD)
        LOG.info("Restauration des règles de "+str(dp.id)+" terminé")


class DeserializeJSON():

    def __init__(self, *args, **kwargs):
        self.modeio = "rt"

    def _open_file(self, filepath):
        self.file_test = io.open(filepath, mode=self.modeio)

    def _clean_file(self):
        self.instruction = list()
        for line in self.file_test:
            try:
                self.instruction.append(json.loads(line))
            except ValueError:
                continue

    def verify_instuctions(self, filepath, dpid, number, rules):
        self._open_file(filepath)
        self._clean_file()
        count = 0

        for rule in self.instruction:
            if rule['dpid'] == dpid or rule['dpid'] == str(dpid):
                if ("buckets" in rule) is False:
                    if rule["table_id"] is 0:
                        count += 1
                rules.append(rule)
        if count == number:
            return True
        else:
            return False

    def _close_file(self):
        self.file_test.close()
