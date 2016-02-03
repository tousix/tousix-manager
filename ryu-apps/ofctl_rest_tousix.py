# -*- coding: utf8 -*-
__author__ = 'remy'

import logging
import ast

from webob import Response
from ryu.ofproto import ofproto_v1_0
from ryu.ofproto import ofproto_v1_2
from ryu.ofproto import ofproto_v1_3
from ryu.lib import ofctl_v1_0
from ryu.lib import ofctl_v1_2
from ryu.lib import ofctl_v1_3
from ryu.app.ofctl_rest import StatsController, RestStatsApi
from ryu.app.wsgi import WSGIApplication
from ryu.controller import dpset

LOG = logging.getLogger('ryu.app.ofctl_rest_tousix')

class RestAPI (RestStatsApi):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION,
                    ofproto_v1_2.OFP_VERSION,
                    ofproto_v1_3.OFP_VERSION]
    _CONTEXTS = {
        'dpset': dpset.DPSet,
        'wsgi': WSGIApplication
    }

    def __init__(self, *args, **kwargs):
        super(RestStatsApi, self).__init__(*args, **kwargs)
        self.dpset = kwargs['dpset']
        wsgi = kwargs['wsgi']
        self.waiters = {}
        self.data = {}
        self.data['dpset'] = self.dpset
        self.data['waiters'] = self.waiters
        mapper = wsgi.mapper

        wsgi.registory['RestController'] = self.data
        path = '/stats'
        uri = path + '/switches'
        mapper.connect('stats', uri,
                       controller=RestController, action='get_dpids',
                       conditions=dict(method=['GET']))

        uri = path + '/desc/{dpid}'
        mapper.connect('stats', uri,
                       controller=RestController, action='get_desc_stats',
                       conditions=dict(method=['GET']))

        uri = path + '/flow/{dpid}'
        mapper.connect('stats', uri,
                       controller=RestController, action='get_flow_stats',
                       conditions=dict(method=['GET', 'POST']))

        uri = path + '/aggregateflow/{dpid}'
        mapper.connect('stats', uri,
                       controller=RestController,
                       action='get_aggregate_flow_stats',
                       conditions=dict(method=['GET', 'POST']))

        uri = path + '/port/{dpid}'
        mapper.connect('stats', uri,
                       controller=RestController, action='get_port_stats',
                       conditions=dict(method=['GET']))

        uri = path + '/queue/{dpid}'
        mapper.connect('stats', uri,
                       controller=RestController, action='get_queue_stats',
                       conditions=dict(method=['GET']))

        uri = path + '/meterfeatures/{dpid}'
        mapper.connect('stats', uri,
                       controller=RestController, action='get_meter_features',
                       conditions=dict(method=['GET']))

        uri = path + '/meterconfig/{dpid}'
        mapper.connect('stats', uri,
                       controller=RestController, action='get_meter_config',
                       conditions=dict(method=['GET']))

        uri = path + '/meter/{dpid}'
        mapper.connect('stats', uri,
                       controller=RestController, action='get_meter_stats',
                       conditions=dict(method=['GET']))

        uri = path + '/groupfeatures/{dpid}'
        mapper.connect('stats', uri,
                       controller=RestController, action='get_group_features',
                       conditions=dict(method=['GET']))

        uri = path + '/groupdesc/{dpid}'
        mapper.connect('stats', uri,
                       controller=RestController, action='get_group_desc',
                       conditions=dict(method=['GET']))

        uri = path + '/group/{dpid}'
        mapper.connect('stats', uri,
                       controller=RestController, action='get_group_stats',
                       conditions=dict(method=['GET']))

        uri = path + '/portdesc/{dpid}'
        mapper.connect('stats', uri,
                       controller=RestController, action='get_port_desc',
                       conditions=dict(method=['GET']))

        uri = path + '/flowentry/{cmd}'
        mapper.connect('stats', uri,
                       controller=RestController, action='mod_flow_entry',
                       conditions=dict(method=['POST']))

        uri = path + '/flowentry/clear/{dpid}'
        mapper.connect('stats', uri,
                       controller=RestController, action='delete_flow_entry',
                       conditions=dict(method=['DELETE']))

        uri = path + '/meterentry/{cmd}'
        mapper.connect('stats', uri,
                       controller=RestController, action='mod_meter_entry',
                       conditions=dict(method=['POST']))

        uri = path + '/groupentry/{cmd}'
        mapper.connect('stats', uri,
                       controller=RestController, action='mod_group_entry',
                       conditions=dict(method=['POST']))

        uri = path + '/portdesc/{cmd}'
        mapper.connect('stats', uri,
                       controller=RestController, action='mod_port_behavior',
                       conditions=dict(method=['POST']))

        uri = path + '/experimenter/{dpid}'
        mapper.connect('stats', uri,
                       controller=RestController, action='send_experimenter',
                       conditions=dict(method=['POST']))



class RestController(StatsController):
    def __init__(self, req, link, data, **config):
        super(RestController, self).__init__(req, link, data, **config)

    def mod_flow_entry(self, req, cmd, **_kwargs):
        if cmd == "reset" or cmd == "reset_strict":
            try:
                flow = ast.literal_eval(req.body)
            except SyntaxError:
                LOG.debug('invalid syntax %s', req.body)
                return Response(status=400)

            dpid = flow.get('dpid')
            dp = self.dpset.get(int(dpid))
            if dp is None:
                return Response(status=404)

            if cmd == 'reset':
                cmd = dp.ofproto.OFPFC_MODIFY
            elif cmd == 'reset_strict':
                cmd = dp.ofproto.OFPFC_MODIFY_STRICT
            else:
                return Response(status=404)

            flow["flags"] = int(flow.get("flags", 0) | 4)
            if dp.ofproto.OFP_VERSION == ofproto_v1_0.OFP_VERSION:
                ofctl_v1_0.mod_flow_entry(dp, flow, cmd)
            elif dp.ofproto.OFP_VERSION == ofproto_v1_2.OFP_VERSION:
                ofctl_v1_2.mod_flow_entry(dp, flow, cmd)
            elif dp.ofproto.OFP_VERSION == ofproto_v1_3.OFP_VERSION:
                ofctl_v1_3.mod_flow_entry(dp, flow, cmd)
            else:
                LOG.debug('Unsupported OF protocol')
                return Response(status=501)

            return Response(status=200)
        else:
            return super(RestController, self).mod_flow_entry(req, cmd, **_kwargs)
