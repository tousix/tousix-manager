# -*- coding: utf8 -*-
__author__ = 'remy'

from django import forms
from database.models import Membre, Contact, Hote, ConnectionType
from localflavor.fr.forms import FRPhoneNumberField


class ConnexionChoiceField(forms.ModelChoiceField):
    """
    ModelChoiceField modification for display connection type information.
    """
    def label_from_instance(self, obj):
        return "%s" % obj.connection_type


class MemberForm(forms.ModelForm):
    """
    ModelForm with custom field for display connectiontype value.
    """
    connexion_type = ConnexionChoiceField(queryset=ConnectionType.objects.all(), empty_label=None)

    class Meta:
        model = Membre
        fields = ['nommembre', 'url', 'asnumber', 'connexion_type', 'fqdn_host']


class BillingForm(forms.ModelForm):
    """
    ModelForm for billing contact model.
    """
    telcontact = FRPhoneNumberField()

    class Meta:
        model = Contact
        exclude = ['idcontact']


class NOCForm(forms.ModelForm):
    """
    ModelForm for NOC contact model.
    """
    telcontact = FRPhoneNumberField()

    class Meta:
        model = Contact
        exclude = ['idcontact']


class TechnicalForm(forms.ModelForm):
    """
    ModelForm for technical contact model.
    """
    telcontact = FRPhoneNumberField()

    class Meta:
        model = Contact
        exclude = ['idcontact']


class RouterForm(forms.ModelForm):
    """
    ModelForm for router model.
    """
    class Meta:
        model = Hote
        fields = ['nomhote', 'machote']