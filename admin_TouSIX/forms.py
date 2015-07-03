# -*- coding: utf8 -*-
__author__ = 'remy'

from django import forms
from database.models import Hote, Port
from django.forms.utils import ErrorList

class PortChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.string_description()

class HoteForm(forms.ModelForm):

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
            # Set editing value for instance
            self.fields["idport"].queryset = Port.objects.\
                                             filter(usable=True).\
                                             exclude(idport__in=(Hote.objects
                                                                 .exclude(idhote=self.instance.idhote)
                                                                 .values("idport")))
            self.fields["idport"].initial = {self.instance.idport_id: self.instance.idport.string_description}

    class Meta:
        model = Hote
        exclude = ["idmembre"]
