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

from tousix_manager.Member_Manager.forms.forms import *
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView

from tousix_manager.Authentication.LoginMixin import LoginRequiredMixin
from tousix_manager.Database.models import Membre, Hote, UserMembre
from tousix_manager.Member_Manager.update.UpdateMixin import UpdateUrlMixin


class UpdateMemberView(LoginRequiredMixin, UpdateView, UpdateUrlMixin, SuccessMessageMixin):
    """
    This view is for testing purposes.
    It is an attempt to receive all the data posted for one url, and process only on changed values.
    A much simpler approach is currently used, on the other update views present in this module.
    """
    model = Membre
    form_class = MemberForm
    template_name = "update_member.html"
    success_message = "Changement contact facturation enregistré."

    def get_object(self, queryset=None):
        return UserMembre.objects.filter(user=self.request.user).first().membre

    def get_form(self, form_class=None):
        return MemberForm(instance=self.get_object(), prefix="member")

    def get_context_data(self, **kwargs):
        context = {"member": self.get_form()}
        context["technical"] = TechnicalForm(instance=self.get_object().technical, prefix="technical")
        if context["technical"].instance.pk is not None:
            context["technical"].empty = False
        context["noc"] = NOCForm(instance=self.get_object().noc, prefix="noc")
        if context["noc"].instance.pk is not None:
            context["noc"].empty = False
        context["billing"] = BillingForm(instance=self.get_object().billing, prefix="billing")
        if context["billing"].instance.pk is not None:
            context["billing"].empty = False

        context["router"] = []
        for hote in Hote.objects.filter(idmembre=UserMembre.objects.filter(user=self.request.user).first().membre.idmembre):
            context["router"].append(RouterForm(instance=hote, prefix="router_"+str(hote.idhote)))

        context["password"] = PasswordChangeForm(self.request.user, prefix="password")
        return context

    def post(self, request, *args, **kwargs):
        member = MemberForm(data=request.POST, instance=self.get_object(), prefix="member")

        if member.is_valid():
            member.save()

        return super(UpdateMemberView, self).post(request, *args, **kwargs)

