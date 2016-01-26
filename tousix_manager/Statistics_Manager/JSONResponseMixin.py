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

from django.http import JsonResponse
from django.utils.timezone import datetime

class JSONResponseMixin(object):
    """
    Mixin used for render statistic data into JSON-friendly response.
    """
    def render_to_response(self, context, **response_kwargs):
        """
        Overwrites default method (calls render_to_json_response)
        :param context:
        :param response_kwargs:
        :return:
        """
        return self.render_to_json_response(context, **response_kwargs)

    def render_to_json_response(self, context, **response_kwargs):
        """
        Render a JSON HTTP Response
        :param context:
        :param response_kwargs:
        :return:
        """
        return JsonResponse(self.refactor_json(context), safe=False, **response_kwargs)

    def refactor_json(self, context):
        """
        Adapts Python objects for JSON factoring.
        :param context:
        :return:
        """
        for data in context:
            if isinstance(data.get('time'), datetime):
                # Remove microseconds & Transforms into ISO 8601 format
                data['time'] = data['time'].replace(microsecond=0).isoformat()
        return context
