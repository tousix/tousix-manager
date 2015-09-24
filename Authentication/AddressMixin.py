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


class AddressLimitationMixin(object):
    """
    Class used for verifying if the emitter of the request is in the IP address whitelist.

    It is only suitable for private addresses and/or LAN addresses (proxies can bypass that security
    if an public IP address is defined in the whitelist).

    You need to add a ADDRESS_WHITELIST list variable with string addresses in your django settings file.
    """

    def verify_address(self):
        if self.request.META["HTTP_REMOTE_ADDR"] in settings.ADDRESS_WHITELIST:
            return None
        else:
            return "Confirmed"
