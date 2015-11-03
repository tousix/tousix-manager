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

from django.core.urlresolvers import reverse
from Member_Manager.forms.forms import *
from Database.models import Hote, UserMembre
from django.contrib.auth.forms import PasswordChangeForm


class UpdateUrlMixin(object):

    def get_success_url(self):
        return reverse("update member")

    def create_context_data(self, context, **kwargs):
        if self.form_class != MemberForm:
            context["member"] = MemberForm(instance=self.get_membre(), prefix="member")
        if self.form_class != TechnicalForm:
            context["technical"] = TechnicalForm(instance=self.get_membre().technical, prefix="technical")
            if context["technical"].instance.pk is not None:
                context["technical"].empty = False
        if self.form_class != NOCForm:
            context["noc"] = NOCForm(instance=self.get_membre().noc, prefix="noc")
            if context["noc"].instance.pk is not None:
                context["noc"].empty = False
        if self.form_class != BillingForm:
            context["billing"] = BillingForm(instance=self.get_membre().billing, prefix="billing")
            if context["billing"].instance.pk is not None:
                context["billing"].empty = False
        if self.form_class != RouterForm:
            context["router"] = RouterForm(instance=Hote.objects.filter(idmembre=self.get_membre().idmembre).first(), prefix="router")
        if self.form_class != PasswordChangeForm:
            context["password"] = PasswordChangeForm(self.request.user, prefix="password")
        return context

    def get_membre(self):
        return UserMembre.objects.filter(user=self.request.user).first().membre
