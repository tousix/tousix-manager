# -*- coding: utf8 -*-
__author__ = 'remy'

from django import forms
from database.models import Hote, Port, Switch, Pop, Membre, ConnectionType
from django.forms.utils import ErrorList


class PortChoiceField(forms.ModelChoiceField):
    """
    ModelChoiceField modification for display complete port information.
    """
    def label_from_instance(self, obj):
        return "%s" % obj.string_description()


class HoteForm(forms.ModelForm):
    """
    ModelForm with custom router display.
    This form handles the link between :model:`database.Port` and :model:`database.Hote`.
    Depending of the context (relationship non-established, initial value), it will
    create a custom list with complete description all the ports avaliable.
    """
    idport = PortChoiceField(queryset=Port.objects
                             .filter(usable=True)
                             .exclude(idport__in=(Hote.objects.values("idport"))), empty_label=None)

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=None,
                 empty_permitted=False, instance=None):
        super(HoteForm, self).__init__(data, files, auto_id, prefix,
                                       initial, error_class, label_suffix,
                                       empty_permitted, instance)
        if self.instance.idhote is not None:
            # Set idport editing value for instance
            self.fields["idport"].queryset = Port.objects.\
                                             filter(usable=True).\
                                             exclude(idport__in=(Hote.objects
                                                                 .exclude(idhote=self.instance.idhote)
                                                                 .values("idport")))
            if self.instance.idport is not None:
                self.fields["idport"].initial = {self.instance.idport_id: self.instance.idport.string_description}

    class Meta:
        model = Hote
        exclude = ["idmembre"]


class PopChoiceField(forms.ModelChoiceField):
    """
    ModelChoiceField modification for display POP name instead of complete object.
    """
    def label_from_instance(self, obj):
        return "%s" % obj.nompop


class SwitchForm(forms.ModelForm):
    """
    ModelForm for modify :model:`database.Switch` with custom fields.
    """
    idpop = PopChoiceField(queryset=Pop.objects.all(), empty_label=None)

    class Meta:
        model = Switch
        fields = ['nomswitch', 'idswitch', 'ipswitch', 'idpop']


class ConnexionChoiceField(forms.ModelChoiceField):
    """
    ModelChoiceField modification for display Connection type name instead of complete object.
    """
    def label_from_instance(self, obj):
        return "%s" % obj.connection_type


class MembreForm(forms.ModelForm):
    """
    ModelForm for modify :model:`database.Membre` with custom fields.
    """
    idpop = PopChoiceField(queryset=Pop.objects.all())
    connexion_type = ConnexionChoiceField(queryset=ConnectionType.objects.all())

    class Meta:
        model = Membre
        fields = ["nommembre", "asnumber", "connexion_type", "fqdn_host", "idpop", "approved"]