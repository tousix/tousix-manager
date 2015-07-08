# -*- coding: utf8 -*-
__author__ = 'remy'

from Generate_rules.configuration import configuration as conf

class Interface(object):
    """
    Abstract class for creating statistics rules.
    """
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

        return conf.priority["Stats"].get(type)

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
