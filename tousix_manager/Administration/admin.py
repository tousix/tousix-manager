from tousix_manager.Administration.actions import generate_routeserver_conf, generate_openflow_rules, get_rules_list, change_hote_status
from tousix_manager.Administration.adminsite import admin_tousix
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from fsm_admin.mixins import FSMTransitionMixin
from tousix_manager.Administration.forms import HoteForm, SwitchForm, MembreForm, PortForm, UserMembreForm
from tousix_manager.Database.models import Membre, Hote, Port, Pop, Contact, Switch, LogSwitch, Regles, ConnectionType, UserMembre


# Register your models here.


class HoteInLine(admin.TabularInline):
    """
    Class which permits host visibility in other models related.
    """
    model = Hote
    max_num = 3
    min_num = 0
    extra = 1
    form = HoteForm


@admin.register(Membre)
class MembreAdmin(admin.ModelAdmin):
    """
    Class for member visibility in admin panel.
    """
    list_display = ["nommembre", "url", "asnumber", "approved"]
    inlines = [HoteInLine]
    list_filter = ['approved']
    form = MembreForm
    search_fields = ["nommembre", "asnumber"]
    actions = [generate_routeserver_conf]


@admin.register(Hote)
class HoteAdmin(FSMTransitionMixin, admin.ModelAdmin):
    """
    Class for router visibility in admin panel.
    """
    list_display = ["nomhote", "ipv4hote", "ipv6hote", "machote", "membre", "pop", "switch", "port", "etat"]
    exclude = ["idmembre"]
    list_filter = ['valid']
    search_fields = ["nomhote", "ipv4hote", "ipv6hote", "machote"]
    form = HoteForm
    actions = [generate_routeserver_conf, change_hote_status]
    readonly_fields = ['etat']
    fsm_field = ['etat']

    def save_model(self, request, obj, form, change):
        """
        Method used for changing the status when the MAC address was modified.
        :param request:
        :param obj:
        :param form:
        :param change:
        :return:
        """
        previous = self.model.objects.filter(idhote=obj.idhote).first()
        obj.save()
        if obj.etat == "Production":
            if obj.machote != previous.machote:
                obj.Prepare()
                obj.save()


@admin.register(Port)
class PortAdmin(admin.ModelAdmin):
    """
    Class for port visibility in admin panel.
    """
    list_display = ["idport", "switch", "numport", "typeport", "enabled"]
    inlines = [HoteInLine]
    form = PortForm
    list_filter = ["idswitch__nomswitch"]
    search_fields = ["numport", 'idswitch__nomswitch']


@admin.register(Pop)
class PopAdmin(admin.ModelAdmin):
    """
    Class for POP visibility in admin panel.
    """
    list_display = ["nompop"]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Class for contact visibility in admin panel.
    """
    exclude = ["idcontact"]
    list_display = ["nomcontact", "prenomcontact", "telcontact", "mailcontact"]
    search_fields = ["nomcontact", "prenomcontact"]


@admin.register(Switch)
class SwitchAdmin(admin.ModelAdmin):
    """
    Class for switch visibility in admin panel.
    """
    list_display = ["nomswitch", "ipswitch", "idswitch"]
    form = SwitchForm
    search_fields = ["nomswitch", "ipswitch", "idswitch"]
    actions = [generate_openflow_rules]


@admin.register(LogSwitch)
class LogSwitchAdmin(admin.ModelAdmin):
    """
    Class for log visibility in admin panel.
    """
    list_display = ['nomswitch', "time", "level", "message"]
    search_fields = ['idswitch__nomswitch', "level", "time"]
    list_filter = ['idswitch__nomswitch', "level"]
    readonly_fields = ['idlog', "idswitch", "time", "level", "message", "json"]


@admin.register(Regles)
class ReglesField(FSMTransitionMixin, admin.ModelAdmin):
    """
    Class for rules visibility in admin panel.
    """
    readonly_fields = ['idregle', 'typeregle', 'regle', 'idswitch', 'etat']
    list_display = ['switch', 'regle', 'typeregle', 'etat']
    search_fields = ['regle']
    list_filter = ['idswitch__nomswitch', "typeregle", "source__nomhote", "destination__nomhote"]
    actions = [get_rules_list]
    fsm_field = ['etat']


@admin.register(ConnectionType)
class ConnectionTypeAdmin(admin.ModelAdmin):
    """
    Class for ConnectionType visibility in admin panel
    """
    list_display = ["connection_type"]

@admin.register(UserMembre)
class UserMembreAdmin(admin.ModelAdmin):
    list_display = ['user', 'nommembre']
    form = UserMembreForm

admin_tousix.register(Regles, ReglesField)
admin_tousix.register(LogSwitch, LogSwitchAdmin)
admin_tousix.register(Switch, SwitchAdmin)
admin_tousix.register(Contact, ContactAdmin)
admin_tousix.register(Pop, PopAdmin)
admin_tousix.register(Port, PortAdmin)
admin_tousix.register(Hote, HoteAdmin)
admin_tousix.register(Membre, MembreAdmin)
admin_tousix.register(ConnectionType, ConnectionTypeAdmin)
admin_tousix.register(UserMembre, UserMembreAdmin)