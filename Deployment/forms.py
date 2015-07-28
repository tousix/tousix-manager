# -*- coding: utf8 -*-
__author__ = 'remy'

from django import forms


class ConfirmForm(forms.Form):
    confirm = forms.BooleanField(widget=forms.HiddenInput(), initial=True)
