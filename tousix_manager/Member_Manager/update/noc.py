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

from tousix_manager.Member_Manager.forms.noc import NOCForm
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic.edit import UpdateView

from tousix_manager.Authentication.LoginMixin import LoginRequiredMixin
from tousix_manager.Database.models import Contact, UserMembre
from tousix_manager.Member_Manager.update.UpdateMixin import UpdateUrlMixin


class NOCUpdateView(LoginRequiredMixin, UpdateView, UpdateUrlMixin, SuccessMessageMixin):
    """
    This view updates NOC contact associated with the requesting user.
    """
    model = Contact
    form_class = NOCForm
    template_name = "update_member.html"
    success_message = "Changement contact NOC enregistré."
    context_object_name = "noc"

    def get_object(self, queryset=None):
        return UserMembre.objects.filter(user=self.request.user).first().membre.noc

    def get_form(self, form_class=None):
        return NOCForm(instance=self.get_object(), prefix="noc")

    def get(self, request, *args, **kwargs):
        return redirect(reverse("update member"))

    def form_valid(self, form):
        form.save()
        return redirect(reverse("update member"))

    def form_invalid(self, form):
        return self.render_to_response(self.create_context_data({"noc": form}))

    def post(self, request, *args, **kwargs):
        noc = NOCForm(data=request.POST, instance=self.get_object(), prefix="noc")

        if noc.is_valid():
            return self.form_valid(noc)
        else:
            return self.form_invalid(noc)