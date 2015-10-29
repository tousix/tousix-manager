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

from django.views.generic.edit import UpdateView
from Member_Manager.forms.technical import TechnicalForm
from Authentication.LoginMixin import LoginRequiredMixin
from Database.models import Contact, UserMembre
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect


class TechnicalUpdateView(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    """
    This view updates technical contact associated with the requesting user.
    """
    model = Contact
    form_class = TechnicalForm
    template_name = "update_member.html"
    success_url = "/member/update"
    success_message = "Changement contact technique enregistré."
    context_object_name = "technical"

    def get_object(self, queryset=None):
        return UserMembre.objects.filter(user=self.request.user).first().membre.technical

    def get_form(self, form_class=None):
        return TechnicalForm(instance=self.get_object(), prefix="technical")

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect("/member/update")

    def form_valid(self, form):
        form.save()
