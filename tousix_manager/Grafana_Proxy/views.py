#    Copyright 2018 Rémy Lapeyrade <remy at lapeyrade dot net>
#    Copyright 2018 LAAS-CNRS
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


from revproxy.views import ProxyView


class GraphanaProxyView(ProxyView):
    upstream = 'http://127.0.0.1:3000/dashboard/'

    def get_proxy_request_headers(self, request):
        headers = super(GraphanaProxyView, self).get_proxy_request_headers(request)
        headers['X-WEBAUTH-USER'] = request.user.username
        return headers