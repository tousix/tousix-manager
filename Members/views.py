# -*- coding: utf8 -*-
__author__ = 'remy'
from formtools.wizard.views import CookieWizardView
from Members.forms import MemberForm, BillingForm, TechnicalForm, NOCForm, RouterForm, UserForm


class CreateMemberView(CookieWizardView):

    template_name = 'inscription_membre.html'
    form_list = [MemberForm, BillingForm, NOCForm, TechnicalForm, RouterForm, UserForm]

    def done(self, form_list, form_dict, **kwargs):
        # Create object for filling missing values
        member = form_dict['0'].save(commit=False)
        if form_dict['1'].isempty is False:
            billing = form_dict['1'].save()
            member.billing_id = billing.pk
        if form_dict['2'].isempty is False:
            noc = form_dict['2'].save()
            member.noc_id = noc.pk
        if form_dict['3'].isempty is False:
            technical = form_dict['3'].save()
            member.technical_id = technical.pk

        user = form_dict['5'].save()
        member.user_id = user.pk
        member.save()

        router = form_dict['4'].save(commit=False)
        router.idmembre_id = member.pk
        router.save()
