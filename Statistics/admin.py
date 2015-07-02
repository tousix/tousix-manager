from django.contrib import admin
from django import forms

from database.models import Membre, Hote, Port, Pop, Contact

# Register your models here.

class HoteInLine(admin.TabularInline):
    model = Hote

class PortInLine(admin.TabularInline):
    model = Port

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        exclude = ['idcontact']

@admin.register(Membre)
class MembreAdmin(admin.ModelAdmin):
    list_display = ["nommembre", "statut", "asnumber"]
    inlines = [HoteInLine]
    fields = ["nommembre", "statut", "asnumber"]

@admin.register(Hote)
class HoteAdmin(admin.ModelAdmin):
    list_display = ["nomhote", "ipv4hote", "ipv6hote", "parent_membre", "pop", "switch", "port"]
    exclude = ["idmembre", 'idport']


@admin.register(Port)
class PortAdmin(admin.ModelAdmin):
    list_display = ["switch", "numport", "typeport", "usable"]
    inlines = [HoteInLine]

@admin.register(Pop)
class PopAdmin(admin.ModelAdmin):
    list_display = ["nompop"]
