# -*- coding: utf8 -*-
__author__ = 'remy'

from django import forms
from database.models import Membre, Contact, Hote
from django.contrib.auth.models import User

class MemberForm(forms.ModelForm):
    class Meta:
        model = Membre
        fields = ['nommembre', 'url', 'asnumber', 'connexion_type', 'fqdn_host']

class BillingForm(forms.ModelForm):
    empty = forms.BooleanField(label="Laisser vide ?", required=False)

    class Meta:
        model = Contact
        fields = ['nomcontact', 'prenomcontact', 'adressecontact', 'mailcontact', 'telcontact']

    def isempty(self):
        return self.cleaned_data["empty"]

class NOCForm(forms.ModelForm):
    empty = forms.BooleanField(label="Laisser vide ?", required=False)

    class Meta:
        model = Contact
        fields = ['nomcontact', 'prenomcontact', 'adressecontact', 'mailcontact', 'telcontact']

    def isempty(self):
        return self.cleaned_data["empty"]

class TechnicalForm(forms.ModelForm):
    empty = forms.BooleanField(label="Laisser vide ?", required=False)

    class Meta:
        model = Contact
        fields = ['nomcontact', 'prenomcontact', 'adressecontact', 'mailcontact', 'telcontact']

    def isempty(self):
        return self.cleaned_data["empty"]

class RouterForm(forms.ModelForm):
    class Meta:
        model = Hote
        fields = ['nomhote', 'machote', 'ipv4hote', 'ipv6hote']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']