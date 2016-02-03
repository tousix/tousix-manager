# -*- coding: utf8 -*-
__author__ = 'remy'

import logging
import json
import requests
from ryu.base import app_manager
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER, HANDSHAKE_DISPATCHER
from ryu.ofproto import ofproto_v1_0
from ryu.ofproto import ofproto_v1_2
from ryu.ofproto import ofproto_v1_3
from ryu.controller import ofp_event
from ryu.topology import event, switches, api
from ryu.controller.handler import set_ev_cls
from oslo_config import cfg

LOG = logging.getLogger('ryu.app.send_event_async')

class AsyncEventSender(app_manager.RyuApp):

    def __init__(self, *args, **_kwargs):
        super(AsyncEventSender, self).__init__(*args, **_kwargs)
        if self.load_config() is True:
            # Test servers defined

            self.servers = []
            for server in self.CONF.send_async.servers:
                try:
                    server = server.translate(None, '\'\"[]')
                    requests.get(server)
                    self.servers.append(server)
                except requests.ConnectionError:
                    LOG.warning("Server " + server + " not reachable, ignoring url defined")
            LOG.debug("Server verification complete")

    def load_config(self):
        try:
            self.CONF.register_group(cfg.OptGroup(name='send_async',
                                     title='REST controller options'))
            self.CONF.register_opts([
                                    cfg.ListOpt('servers'),
                                    cfg.BoolOpt('enable')
                                    ], 'send_async')
            if self.CONF.send_async.enable is False:
                LOG.warn("Application Envoi évènements asynchrones désactivé")
                self.stop()
                return False
        except cfg.NoSuchOptError:
            LOG.error("Fichier de configuration invalide")
            self.stop()
            return False
        return True

    def send_event_http(self, msg, type):
        content = json.dumps(msg)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        path = "error/ryu"
        if type == "switch_enter":
            path = "/switch/enter"
        elif type == "switch_leave":
            path = "/switch/leave"
        elif type == "port_modify":
            path = "/port/modify"
        elif type == "error":
            path = "/error"
        else:
            LOG.error("Mauvais type d'envoi")
        for server in self.servers:
            try:
                r = requests.post(server+path, data=content, headers=headers)
                if r.status_code != requests.codes.ok:
                    LOG.error("Erreur n° " + str(r.status_code) + " sur le serveur " + server)
            except requests.ConnectionError:
                LOG.error("Erreur de connexion au serveur " + server)
            except requests.Timeout:
                LOG.error("Timeout du serveur " + server)

    @set_ev_cls(event.EventSwitchEnter)
    def _event_switch_enter_handler(self, ev):
        msg = ev.switch.to_dict()
        self.send_event_http(msg, "switch_enter")

    @set_ev_cls(event.EventSwitchLeave)
    def _event_switch_leave_handler(self, ev):
        msg = ev.switch.to_dict()
        self.send_event_http(msg, "switch_leave")

    @set_ev_cls(event.EventPortModify)
    def _event_switch_port_modify_handler(self, ev):
        msg = ev.port.to_dict()
        self.send_event_http(msg, "port_modify")

    @set_ev_cls(ofp_event.EventOFPErrorMsg,
                [HANDSHAKE_DISPATCHER, CONFIG_DISPATCHER, MAIN_DISPATCHER])
    def _event_error_handler(self, ev):
        LOG.debug("Erreur détecté")
        datapath = ev.msg.datapath

        msg = {"dpid": datapath.id,
               "type": ev.msg.type,
               "code": ev.msg.code,
               "data": ev.msg.data}
        self.send_event_http(msg, "error")
