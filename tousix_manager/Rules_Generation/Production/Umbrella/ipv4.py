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

from tousix_manager.Rules_Generation.Production.Umbrella.interface import Interface

class IPv4(Interface):
    """
    Specialized class for creating IPv4 Umbrella rules.
    """
    def get_match(self, match_ipv4=None, match_ipv6=None):
        """
        Forge match object.
        :param match_ipv4: IPv4 target address
        :type match_ipv4: str
        :param match_ipv6: IPv6 target address (not used)
        :type match_ipv6: str
        :return: Match object
        :raises Exception: Bad use case for this class.
        """
        if match_ipv4 is None:
            raise Exception("Bad use case for this class.")
        match = {"dl_type": 2054,
                 "arp_op": 1,
                 "arp_tpa": match_ipv4}
        return match
