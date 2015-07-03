from django.contrib import admin
from django import forms

from database.models import Membre, Hote, Port, Pop, Contact, Switch
from admin_TouSIX.forms import HoteForm, SwitchForm, MembreForm
# Register your models here.

class HoteInLine(admin.TabularInline):
    model = Hote
    max_num = 1
    form = HoteForm

class PortInLine(admin.TabularInline):
    model = Port

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        exclude = ['idcontact']

@admin.register(Membre)
class MembreAdmin(admin.ModelAdmin):
    list_display = ["nommembre", "url", "asnumber", "approved"]
    inlines = [HoteInLine]
    list_filter = ['approved']
    form = MembreForm
    search_fields = ["nommembre", "asnumber"]

@admin.register(Hote)
class HoteAdmin(admin.ModelAdmin):
    list_display = ["nomhote", "ipv4hote", "ipv6hote", "membre", "pop", "switch", "port"]
    exclude = ["idmembre"]
    list_filter = ['valid']
    search_fields = ["nomhote", "ipv4hote", "ipv6hote", "machote"]
    form = HoteForm

@admin.register(Port)
class PortAdmin(admin.ModelAdmin):
    list_display = ["switch", "numport", "typeport", "usable"]
    inlines = [HoteInLine]
    exclude = ["idswitch"]
    list_filter = ["idswitch__nomswitch"]

@admin.register(Pop)
class PopAdmin(admin.ModelAdmin):
    list_display = ["nompop"]

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    exclude = ["idcontact"]
    list_display = ["nomcontact", "prenomcontact", "telcontact", "mailcontact"]
    search_fields = ["nomcontact", "prenomcontact"]

@admin.register(Switch)
class SwichAdmin(admin.ModelAdmin):
    list_display = ["nomswitch", "ipswitch", "idswitch"]
    form = SwitchForm
