# -*- coding: utf8 -*-
__author__ = 'remy'
from formtools.wizard.views import CookieWizardView
from django.views.generic.edit import UpdateView
from Members.forms import MemberForm, BillingForm, TechnicalForm, NOCForm, RouterForm, UserForm
from Authentication.LoginMixin import LoginRequiredMixin
from database.models import Membre, Hote
from django.contrib.auth.forms import PasswordChangeForm

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

class UpdateMemberView(LoginRequiredMixin, UpdateView):
    model = Membre
    form_class = MemberForm
    template_name = "update_member.html"
    success_url = "/member/update"

    def get_object(self, queryset=None):
        return Membre.objects.filter(user=self.request.user).first()

    def get_context_data(self, **kwargs):
        context = super(UpdateMemberView, self).get_context_data(**kwargs)
        membre = self.get_object()

        if membre.technical is None:
            context['technical'] = TechnicalForm(prefix="technical")
        else:
            context['technical'] = TechnicalForm(instance=membre.technical, prefix="technical")
        if membre.noc is None:
            context['noc'] = NOCForm(prefix="noc")
        else:
            context['noc'] = NOCForm(instance=membre.noc, prefix="noc")
        if membre.billing is None:
            context['billing'] = BillingForm(prefix="billing")
        else:
            context['billing'] = BillingForm(instance=membre.billing, prefix="billing")
        hosts = Hote.objects.filter(idmembre=membre)
        context['hosts'] = []
        i = 0
        for host in hosts:
            context['hosts'].append(RouterForm(instance=host, prefix="host"+str(i)))
            i += 1
        context['user'] = PasswordChangeForm(user=self.request.user, prefix="user")
        return context

    def post(self, request, *args, **kwargs):
        print("test")
        return super(UpdateMemberView, self).post(request, *args, **kwargs)
