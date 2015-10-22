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


class groups(object):
    """
    This class has the same purpose as the configuration class.
    It is based on REST definition of groups in Ryu.
    """
    groups = {
        2221123978211977908: [
            {"dpid": 2221123978211977908,
             "type": "FF",
             "group_id": 2,
             "buckets": [{"watch_port": 51,
                          "watch_group": 4294967295,
                          "weight": 1,
                          "actions": [{"type": "OUTPUT",
                                       "port": 51}]},
                         {"watch_port": 53,
                          "watch_group": 4294967295,
                          "weight": 1,
                          "actions": [{"type": "OUTPUT",
                                       "port": 53}]}]},
            {"dpid": 2221123978211977908,
             "type": "FF",
             "group_id": 3,
             "buckets": [{"watch_port": 53,
                          "watch_group": 4294967295,
                          "weight": 1,
                          "actions": [{"type": "OUTPUT",
                                       "port": 53}]},
                         {"watch_port": 51,
                          "watch_group": 4294967295,
                          "weight": 1,
                          "actions": [{"type": "OUTPUT",
                                       "port": 51}]}]}
        ],
        16690345156023249453: [
            {"dpid": 16690345156023249453,
             "type": "FF",
             "group_id": 1,
             "buckets": [{"watch_port": 49,
                          "watch_group": 4294967295,
                          "weight": 1,
                          "actions": [{"type": "OUTPUT",
                                       "port": 49}]},
                         {"watch_port": 50,
                          "watch_group": 4294967295,
                          "weight": 1,
                          "actions": [{"type": "OUTPUT",
                                       "port": 50}]}]},
            {"dpid": 16690345156023249453,
             "type": "FF",
             "group_id": 3,
             "buckets": [{"watch_port": 49,
                          "watch_group": 4294967295,
                          "weight": 1,
                          "actions": [{"type": "OUTPUT",
                                       "port": 49}]},
                         {"watch_port": 50,
                          "watch_group": 4294967295,
                          "weight": 1,
                          "actions": [{"type": "OUTPUT",
                                       "port": 50}]}]}
        ],
        10925425496585651080: [
            {"dpid": 10925425496585651080,
             "type": "FF",
             "group_id": 1,
             "buckets": [{"watch_port": 53,
                          "watch_group": 4294967295,
                          "weight": 1,
                          "actions": [{"type": "OUTPUT",
                                       "port": 53}]},
                         {"watch_port": 51,
                          "watch_group": 4294967295,
                          "weight": 1,
                          "actions": [{"type": "OUTPUT",
                                       "port": 51}]}]},
            {"dpid": 10925425496585651080,
             "type": "FF",
             "group_id": 2,
             "buckets": [{"watch_port": 53,
                          "watch_group": 4294967295,
                          "weight": 1,
                          "actions": [{"type": "OUTPUT",
                                       "port": 53}]},
                         {"watch_port": 51,
                          "watch_group": 4294967295,
                          "weight": 1,
                          "actions": [{"type": "OUTPUT",
                                       "port": 51}]}]}
        ]
    }
