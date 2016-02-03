# -*- coding: utf8 -*-
__author__ = 'remy'

from ryu.base import app_manager
import logging
import requests
import time, datetime
import json

from oslo_config import cfg
from ryu.controller import ofp_event
from ryu.topology import api
from ryu.controller.handler import set_ev_cls, MAIN_DISPATCHER
from ryu.lib import hub
from ryu.ofproto import ofproto_v1_3
from ryu.lib import ofctl_v1_3
LOG = logging.getLogger('ryu.app.send_stats')

class StatsSender(app_manager.RyuApp):

    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(StatsSender, self).__init__(*args, **kwargs)
        if self.load_config() is True:
            #Test servers defined
            self.datetime = None
            self.servers = []
            for server in self.CONF.send_stats.servers:
                try:
                    server = server.translate(None, '\'\"[]')
                    requests.get(server)
                    self.servers.append(server)
                except requests.ConnectionError:
                    LOG.warning("Server " + server + " not reachable, ignoring url defined")
            LOG.debug("Server verification complete")

            # Création thread routine
            self.timer = hub.spawn(self.timer_job)

    def load_config(self):
        # Extract config file
        try:
            self.CONF.register_group(cfg.OptGroup(name='send_stats',
                                     title='REST controller options'))
            self.CONF.register_opts([
                                    cfg.ListOpt('servers'),
                                    cfg.ListOpt('table_id'),
                                    cfg.IntOpt('timer'),
                                    cfg.BoolOpt('enable')
                                    ], 'send_stats')
            if self.CONF.send_stats.enable is False:
                LOG.warn("Application Envoi statistiques désactivé")
                self.stop()
                return False
        except cfg.NoSuchOptError:
            LOG.error("Fichier de configuration invalide")
            self.stop()
            return False
        return True

    def timer_job(self):
        timer = self.CONF.send_stats.timer
        while True:
            time.sleep(timer)
            if self.servers.__len__() != 0:
                switches = api.get_all_switch(self)
                # Create stats request
                self.datetime = datetime.datetime.now()
                for switch in switches:
                    dpid = switch.dp.id
                    for table_id in self.CONF.send_stats.table_id:
                        LOG.debug('Création requète table_id n° ' + table_id + ' pour ' + str(dpid))
                        parser = switch.dp.ofproto_parser
                        request = parser.OFPFlowStatsRequest(switch.dp, 0, int(table_id))
                        switch.dp.send_msg(request)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def stats_reply_handler(self, ev):
        LOG.debug("Réception de réponse aux statistiques de flow")
        flows = []
        for stats in ev.msg.body:
            actions = ofctl_v1_3.actions_to_str(stats.instructions)
            match = ofctl_v1_3.match_to_str(stats.match)

            s = {'priority': stats.priority,
                 'cookie': stats.cookie,
                 'idle_timeout': stats.idle_timeout,
                 'hard_timeout': stats.hard_timeout,
                 'actions': actions,
                 'match': match,
                 'byte_count': stats.byte_count,
                 'duration_sec': stats.duration_sec,
                 'duration_nsec': stats.duration_nsec,
                 'packet_count': stats.packet_count,
                 'table_id': stats.table_id,
                 'length': stats.length,
                 'flags': stats.flags}
            if str(s["table_id"]) in self.CONF.send_stats.table_id:
                flows.append(s)

        flows = {str(ev.msg.datapath.id): flows}
        LOG.debug("Envoi des stats sur les serveurs")
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        content = json.dumps(flows)
        for server in self.servers:
            try:
                if self.datetime is not None:
                    r = requests.post(server, data=content, headers=headers, params={"time": self.datetime.isoformat()})
                    if r.status_code != requests.codes.ok:
                        LOG.error("Erreur n° " + str(r.status_code) + " sur le serveur " + server)
            except requests.ConnectionError:
                LOG.error("Erreur de connexion au serveur " + server)
            except requests.Timeout:
                LOG.error("Timeout du serveur " + server)
