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

from django.conf import settings


class Interface(object):
    """
    Abstract class for creating statistics rules.
    """

    def __init__(self):
        self.priority = settings.RULES_GENERATION_PRIORITIES
        self.groups = settings.RULES_GENERATION_GROUPS

    def create_stat(self, dpid, member_src, member_dst):
        """
        Create stat rule.
        :param dpid: Target DPID
        :type dpid: int
        :param member_src: Source Peer object
        :type member_src: Peer
        :param member_dst: Destination Peer object
        :type member_dst: Peer
        :return: Statistic flow rule
        :raises NotImplementedError: This method needs an implementation
        """
        raise NotImplementedError("This method needs an implementation")

    def find_priority(self, type):
        """
        Find the priority for statistics rules on the config file.
        :param type: Parameter name
        :type type: str
        :return: priority
        """

        return self.priority["Stats"].get(type)

    def forge_cookie(self, idmember_src, idmember_dst):
        """
        Create cookie based on cookie specification for statistics.
        :param idmember_src: Source member ID
        :type idmember_src: int
        :param idmember_dst: Destionation member ID
        :type idmember_dst: int
        :return: cookie ID
        """

        cookie = idmember_src + 1024
        cookie = cookie << 32
        cookie = cookie + idmember_dst + 1024
        return cookie

    def set_table_id(self):
        """
        Fix the Statistic table.
        :returns: Table ID
        """
        return 1
