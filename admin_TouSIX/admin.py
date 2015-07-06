from django.contrib import admin

from database.models import Membre, Hote, Port, Pop, Contact, Switch, LogSwitch, Regles
from admin_TouSIX.forms import HoteForm, SwitchForm, MembreForm
from admin_TouSIX.actions import generate_routeserver_conf

# Register your models here.

class HoteInLine(admin.TabularInline):
    model = Hote
    max_num = 1
    form = HoteForm

@admin.register(Membre)
class MembreAdmin(admin.ModelAdmin):
    list_display = ["nommembre", "url", "asnumber", "approved"]
    inlines = [HoteInLine]
    list_filter = ['approved']
    form = MembreForm
    search_fields = ["nommembre", "asnumber"]
    actions = [generate_routeserver_conf]

@admin.register(Hote)
class HoteAdmin(admin.ModelAdmin):
    list_display = ["nomhote", "ipv4hote", "ipv6hote", "membre", "pop", "switch", "port"]
    exclude = ["idmembre"]
    list_filter = ['valid']
    search_fields = ["nomhote", "ipv4hote", "ipv6hote", "machote"]
    form = HoteForm
    actions = [generate_routeserver_conf]

@admin.register(Port)
class PortAdmin(admin.ModelAdmin):
    list_display = ["switch", "numport", "typeport", "usable"]
    inlines = [HoteInLine]
    exclude = ["idswitch"]
    list_filter = ["idswitch__nomswitch"]
    search_fields = ["numport", 'idswitch__nomswitch']

@admin.register(Pop)
class PopAdmin(admin.ModelAdmin):
    list_display = ["nompop"]

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    exclude = ["idcontact"]
    list_display = ["nomcontact", "prenomcontact", "telcontact", "mailcontact"]
    search_fields = ["nomcontact", "prenomcontact"]

@admin.register(Switch)
class SwitchAdmin(admin.ModelAdmin):
    list_display = ["nomswitch", "ipswitch", "idswitch"]
    form = SwitchForm
    search_fields = ["nomswitch", "ipswitch", "idswitch"]

@admin.register(LogSwitch)
class LogSwitchAdmin(admin.ModelAdmin):
    list_display = ['nomswitch', "time", "level", "message"]
    search_fields = ['idswitch__nomswitch', "level", "time"]
    list_filter = ['idswitch__nomswitch', "level"]
    readonly_fields = ['idlog', "idswitch", "time", "level", "message", "json"]

@admin.register(Regles)
class ReglesField(admin.ModelAdmin):
    readonly_fields = ['idregle', 'typeregle', 'regle', 'idswitch']
    list_display = ['switch', 'regle', 'typeregle']
    search_fields = ['regle']
    list_filter = ['idswitch__nomswitch']
