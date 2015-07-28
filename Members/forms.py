# -*- coding: utf8 -*-
__author__ = 'remy'

from django import forms
from database.models import Membre, Contact, Hote, ConnectionType
from django.contrib.auth.forms import UserCreationForm
from localflavor.fr.forms import FRPhoneNumberField


class ConnexionChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.connection_type


class MemberForm(forms.ModelForm):
    connexion_type = ConnexionChoiceField(queryset=ConnectionType.objects.all(), empty_label=None)

    class Meta:
        model = Membre
        fields = ['nommembre', 'url', 'asnumber', 'connexion_type', 'fqdn_host']


class BillingForm(forms.ModelForm):

    telcontact = FRPhoneNumberField()

    class Meta:
        model = Contact
        exclude = ['idcontact']


class NOCForm(forms.ModelForm):

    telcontact = FRPhoneNumberField()

    class Meta:
        model = Contact
        exclude = ['idcontact']


class TechnicalForm(forms.ModelForm):

    telcontact = FRPhoneNumberField()

    class Meta:
        model = Contact
        exclude = ['idcontact']


class RouterForm(forms.ModelForm):
    class Meta:
        model = Hote
        fields = ['nomhote', 'machote']

class UserForm(UserCreationForm):
    pass