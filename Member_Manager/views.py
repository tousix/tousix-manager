# -*- coding: utf8 -*-
__author__ = 'remy'
from formtools.wizard.views import SessionWizardView
from django.views.generic.edit import UpdateView, FormView
from Member_Manager.forms import MemberForm, BillingForm, TechnicalForm, NOCForm, RouterForm
from Authentication.LoginMixin import LoginRequiredMixin
from Database.models import Membre, Hote, Contact
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
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

        member.user = self.request.user
        member.approved = False
        member.save()

        router = form_dict['4'].save(commit=False)
        router.idmembre_id = member.pk
        router.valid = False
        router.save()
        return render(self.request, "inscription_complete.html")


class UpdateMemberView(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    """
    This view is for testing purposes.
    It is an attempt to receive all the data posted for one url, and process only on changed values.
    A much simpler approach is currently used, on the other update views present in this module.
    """
    model = Membre
    form_class = MemberForm
    template_name = "update_member.html"
    success_url = "/member/update"
    success_message = "Changement contact facturation enregistré."

    def get_object(self, queryset=None):
        return Membre.objects.filter(user=self.request.user).first()

    def get_form(self, form_class=None):
        return MemberForm(instance=self.get_object(), prefix="member")

    def get_context_data(self, **kwargs):
        context = super(UpdateMemberView, self).get_context_data(**kwargs)
        context["technical"] = TechnicalForm(instance=self.get_object().technical, prefix="technical")
        if context["technical"].instance.pk is not None:
            context["technical"].empty = False
        context["noc"] = NOCForm(instance=self.get_object().noc, prefix="noc")
        if context["noc"].instance.pk is not None:
            context["noc"].empty = False
        context["billing"] = BillingForm(instance=self.get_object().billing, prefix="billing")
        if context["billing"].instance.pk is not None:
            context["billing"].empty = False
        context["router"] = RouterForm(instance=Hote.objects.filter(idmembre=self.get_object()).first(), prefix="router")
        context["password"] = PasswordChangeForm(self.request.user, prefix="password")
        return context

    def post(self, request, *args, **kwargs):
        member = MemberForm(data=request.POST, instance=self.get_object(), prefix="member")

        if member.is_valid():
            member.save()

        return super(UpdateMemberView, self).post(request, *args, **kwargs)


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
        return Membre.objects.filter(user=self.request.user).first().technical

    def get_form(self, form_class=None):
        return TechnicalForm(instance=self.get_object(), prefix="technical")

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect("/member/update")

    def form_valid(self, form):
        form.save()


class NOCUpdateView(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    """
    This view updates NOC contact associated with the requesting user.
    """
    model = Contact
    form_class = NOCForm
    template_name = "update_member.html"
    success_url = "/member/update"
    success_message = "Changement contact NOC enregistré."
    context_object_name = "noc"

    def get_object(self, queryset=None):
        return Membre.objects.filter(user=self.request.user).first().noc

    def get_form(self, form_class=None):
        return NOCForm(instance=self.get_object(), prefix="noc")

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect("/member/update")

    def form_valid(self, form):
        form.save()


class BillingUpdateView(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    """
    This view updates billing contact associated with the requesting user.
    """
    model = Contact
    form_class = BillingForm
    template_name = "update_member.html"
    success_url = "/member/update"
    success_message = "Changement contact facturation enregistré."
    context_object_name = "billing"

    def get_object(self, queryset=None):
        return Membre.objects.filter(user=self.request.user).first().billing

    def get_form(self, form_class=None):
        return TechnicalForm(instance=self.get_object(), prefix="billing")

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect("/member/update")

    def form_valid(self, form):
        form.save()


class RouterUpdateView(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    """
    This view updates router associated with the requesting user.
    """
    model = Hote
    form_class = RouterForm
    template_name = "update_member.html"
    success_url = "/member/update"
    success_message = "Changement routeur enregistré. Un administrateur doit confirmer."
    context_object_name = "router"

    def get_object(self, queryset=None):
        return Hote.objects.filter(idmembre=Membre.objects.filter(user=self.request.user).first()).first()

    def get_form(self, form_class=None):
        return RouterForm(instance=self.get_object(), prefix="router")

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect("/member/update")

    def form_valid(self, form):
        form.instance.valid = False
        form.save()
        form.Prepare()
        form.save()


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
