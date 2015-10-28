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

from formtools.wizard.views import SessionWizardView
from Member_Manager.forms.forms import *
from Database.models import UserMembre
from Authentication.LoginMixin import LoginRequiredMixin
from django.shortcuts import render


class CreateMemberView(LoginRequiredMixin, SessionWizardView):
    """
    View for creating all the elements needed for add a member (this includes Membre, Hote, Contact model objects)
    """
    template_name = 'inscription_membre.html'
    form_list = [MemberForm, BillingForm, NOCForm, TechnicalForm, RouterForm]

    def done(self, form_list, form_dict, **kwargs):
        """
        This method insert all the forms into the datatbase following a pattern (foreign key constraints).
        :param form_list:
        :param form_dict:
        :param kwargs:
        :return:
        """
        # Create object for filling missing values
        member = form_dict['0'].save(commit=False)

        billing = form_dict['1'].save()
        member.billing_id = billing.pk

        noc = form_dict['2'].save()
        member.noc_id = noc.pk

        technical = form_dict['3'].save()
        member.technical_id = technical.pk

        member.save()
        user_membre = UserMembre(user=self.request.user, membre=member)
        user_membre.save()

        router = form_dict['4'].save(commit=False)
        router.idmembre_id = member.pk
        router.valid = False
        router.save()
        return render(self.request, "inscription_complete.html")

