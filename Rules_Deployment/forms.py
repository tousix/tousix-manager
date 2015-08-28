# -*- coding: utf8 -*-
__author__ = 'remy'

from django import forms


class ConfirmForm(forms.Form):
    """
    Confirmation form for verification views, it could be inserted into a submit button for example.
    """
    confirm = forms.BooleanField(widget=forms.HiddenInput(), initial=True)
