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

from django.views.generic.edit import FormView
from Authentication.LoginMixin import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect


class PasswordChangeView(LoginRequiredMixin, FormView, SuccessMessageMixin):
    """
    THis view permits an uner to change his password.
    """
    form_class = PasswordChangeForm
    success_message = "Changement mdp réussi."
    template_name = "update_member.html"

    def get_form(self, form_class=None):
        return PasswordChangeForm(self.request.user, prefix="password")

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect("/member/update")
