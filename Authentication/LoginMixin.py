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

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Thanks to : http://stackoverflow.com/questions/6069070/how-to-use-permission-required-decorators-on-django-class-based-views
# For clean implementation of this decorator

class LoginRequiredMixin(object):
    """
    This a Mixin created for simplifying the code present in the other views.
    It only adds the decorator in the subclass.
    Warning: You need to inherit this class first among the others, otherwise it will be redefined by other views,
    thus nullify the modification of the method.
    """
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

