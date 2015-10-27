#    Copyright 2015 Rémy Lapeyrade <remy at lapeyrade dot net>
#    Copyright 2015 LAAS-CNRS
#
#
#    This file is part of TouSIX-Manager.
#
#    TouSIX-Manager is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Foobar is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with TouSIX-Manager.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from Database.fields import PositiveBigIntegerField, MACAddressField
from django_fsm import FSMField, transition
from django.db.models import Q


class ConnectionType(models.Model):
    """
    Model used for referencing all the connection types avaliable in the topology.
    """
    connection_type = models.CharField(max_length=20, null=False)

    class Meta:
        db_table = 'Connection_type'


class Contact(models.Model):
    """
    Model for Contact registration.
    All the fields are optional.
    """
    idcontact = models.AutoField(db_column='idContact', primary_key=True)
    nomcontact = models.CharField(db_column='NomContact', max_length=50, blank=True, null=True, verbose_name="Nom")
    prenomcontact = models.CharField(db_column='PrenomContact', max_length=50, blank=True, null=True, verbose_name="Prénom")
    adressecontact = models.CharField(db_column='AdresseContact', max_length=300, blank=True, null=True, verbose_name="Adresse")
    mailcontact = models.EmailField(db_column='MailContact', max_length=100, blank=True, null=True, verbose_name="Mail")
    telcontact = models.CharField(db_column='TelContact', max_length=14, blank=True, null=True, verbose_name="Téléphone")

    class Meta:
        db_table = 'Contact'


class Pop(models.Model):
    """
    Model for referencing all the informations of POP.
    It is advised to use a short name,
    because the value is often used for logging and display information in a limited space.
    """
    idpop = models.AutoField(db_column='idPOP', primary_key=True)
    nompop = models.CharField(db_column='NomPOP', max_length=30, blank=True, null=True)
    adressepop = models.TextField(db_column='AdressePOP', max_length=300, blank=True, null=True)

    class Meta:
        db_table = 'POP'


class Membre(models.Model):
    """
    The member model contains all the information needed about an entity which is member of the IXP.
    """
    idmembre = models.AutoField(db_column='idMembre', primary_key=True)
    nommembre = models.CharField(db_column='NomMembre', max_length=30, blank=True, null=True, verbose_name="Nom membre")
    url = models.URLField(null=True, verbose_name="Lien site web")
    user = models.OneToOneField(User, null=True)
    statut = models.CharField(db_column='Statut', max_length=12, blank=True, null=True)
    asnumber = models.PositiveIntegerField(db_column='ASNumber', verbose_name="N°AS")
    connexion_type = models.ForeignKey(ConnectionType, blank=True, null=True, verbose_name="Type de connexion")
    fqdn_host = models.CharField(max_length=30, default="Undefined", verbose_name="FQDN Routeur")
    idpop = models.ForeignKey(Pop, to_field='idpop', db_column='idPoP', null=True)
    billing = models.OneToOneField(Contact, to_field='idcontact', related_name='billing', parent_link=True, blank=True, null=True, on_delete=models.SET_NULL)
    noc = models.OneToOneField(Contact, to_field='idcontact', related_name='noc', parent_link=True, blank=True, null=True, on_delete=models.SET_NULL)
    technical = models.OneToOneField(Contact, to_field='idcontact', related_name='technical', parent_link=True, blank=True, null=True, on_delete=models.SET_NULL)
    approved = models.BooleanField(default=False)

    class Meta:
        db_table = 'Membre'


class Controleur(models.Model):
    """
    Model for some controller information.
    """
    idctrl = models.AutoField(db_column='IdCTRL', primary_key=True)
    ipctrl = models.GenericIPAddressField(db_column='IPCTRL', blank=True, null=True)
    idpop = models.OneToOneField(Pop, to_field='idpop', db_column='idPOP', unique=True)

    class Meta:
        db_table = 'Contrôleur'


class Switch(models.Model):
    """
    Model representing any type of switch (even the legacy ones could be referenced).
    """
    idswitch = PositiveBigIntegerField(db_column='idSwitch', primary_key=True)
    nomswitch = models.CharField(db_column='nomSwitch', max_length=20, blank=True, null=True)
    ipswitch = models.CharField(db_column='IPSwitch', max_length=39, blank=True, null=True)
    idpop = models.OneToOneField(Pop, to_field='idpop', db_column='idPOP', unique=True, blank=True, null=True)

    class Meta:
        db_table = 'Switch'


class LogSwitch(models.Model):
    """
    This model contains all logs delivered by the :model:`Database.Switch` trough the web application.
    The JSON field is optionnal, but it is recommended to fill it with the other informations when it is possible.
    Additional methods could extract information from JSON data in the future.
    """
    idlog = models.AutoField(primary_key=True)
    idswitch = models.ForeignKey(Switch, to_field='idswitch', db_column='idSwitch', unique=False)
    time = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=10)
    message = models.TextField()
    json = models.TextField(null=True)

    def nomswitch(self):
        return self.idswitch.nomswitch

    class Meta:
        db_table = "SwitchLog"


class Contorleswitch(models.Model):
    """
    Model which shows the relationship between :model:`Database.Switch` connected on multiple :model:`Database.Controleur`.
    """
    idctrl = models.ForeignKey(Controleur, to_field='idctrl', db_column='IdCTRL')
    idswitch = models.ForeignKey(Switch, to_field='idswitch', db_column='idSwitch')

    class Meta:
        db_table = 'ContrôleSwitch'


class Port(models.Model):
    """
    Model for ports in :model:`Database.Switch`.
    """
    idport = models.AutoField(db_column='idPort', primary_key=True)
    numport = models.IntegerField(db_column='numPort', blank=True, null=True)
    typeport = models.CharField(db_column='TypePort', max_length=10, blank=True, null=True)
    usable = models.BooleanField(db_column='Usable')
    idswitch = models.ForeignKey(Switch, to_field='idswitch', db_column='idSwitch')

    def switch(self):
        """
        Returns the string name of the :model:`Database.Switch` linked to this port.
        :return: Switch name
        """
        return self.idswitch.nomswitch

    def string_description(self):
        """
        Return a complete information about the location of the port.
        :return: String port information
        """
        return "POP " + self.idswitch.idpop.nompop + ": " + self.idswitch.nomswitch + " port " + str(self.numport)

    class Meta:
        db_table = 'Port'


class Hote(models.Model):
    """
    Model for routeurs present in the topology.
    It is recommended, even if it is optional,
    to fill all the fields before doing any actions with deployment and rules generation app.

    It is also recommended to avoid to modify the etat field, unless you know what you are doing.
    This fields is linked with side effect methods.
    """
    idhote = models.AutoField(db_column='IdHote', primary_key=True)
    nomhote = models.CharField(db_column='NomHote', max_length=30, blank=True, verbose_name="Nom routeur")
    machote = MACAddressField(db_column='MACHote', verbose_name="Adresse MAC", blank=False, null=False)
    ipv4hote = models.GenericIPAddressField(db_column='IPv4Hote', verbose_name="Adresse IPv4", null=True)
    ipv6hote = models.GenericIPAddressField(db_column='IPv6Hote', verbose_name="Adresse IPv6", null=True)
    idmembre = models.ForeignKey(Membre, to_field='idmembre', db_column='idMembre')
    idport = models.ForeignKey(Port, to_field='idport', db_column='idPort', blank=True, null=True)
    valid = models.BooleanField(default=False)
    etat = FSMField(default="Inactive")

    def membre(self):
        """
        Returns the member name associated with this router.
        :return: Member name
        """
        return self.idmembre.nommembre

    def switch(self):
        """
        Returns the string name of the :model:`Database.Switch` linked to this router, if it was defined by the administrator.
        :return: Switch name
        """
        if self.idport is None:
            return "Undefined"
        else:
            return self.idport.idswitch.nomswitch

    def port(self):
        """
        Returns the string name of the :model:`Database.Port` number linked to this router, if it was defined by the administrator.
        :return: Port number
        """
        if self.idport is None:
            return "Undefined"
        else:
            return self.idport.numport

    def pop(self):
        """
        Returns the string name of the :model:`Database.POP` which the router is linked, if it was defined by the administrator.
        :return: POP name
        """
        if self.idport is None:
            return "Undefined"
        else:
            return self.idport.idswitch.idpop.nompop

    class Meta:
        db_table = 'Hôte'
        unique_together = (('idhote', 'idmembre'),)

    @transition(field=etat, source="Inactive", target="Production", custom={"admin":False})
    def Deploy(self):
        """
        Transition method for deploy a router in the topology, pushing all the rules necessary.
        :return:
        """
        if self.valid is True:
            manager = Manager()
            manager.create_rules(Switch.objects.all())
            deployment = RulesDeployment()
            deployment.send_rules(Switch.objects.all())
        else:
            raise Exception("Not a valid router.")

    @transition(field=etat, source="Production", target="Changing", custom={"admin":False})
    def Prepare(self):
        """
        Transition method for moving the rules of the previous configuration into a special state,
        and applies rules for the new configuration.
        :return:
        """
        regles = Regles.objects.filter(Q(source=self) | Q(destination=self))
        for regle in regles:
            regle.ChangeRulesStatus()
            regle.save()
        manager = Manager()
        manager.create_rules(Switch.objects.all())
        deployment = RulesDeployment()
        deployment.send_rules(Switch.objects.all())

    @transition(field=etat, source="Changing", target="Production")
    def Apply(self):
        """
        Transition method for removing rules applied for the previous configuration of the router.
        :return:
        """
        regles_deprecated = Regles.objects.filter((Q(source=self) | Q(destination=self)) & Q(etat="Deprecated"))
        regles_production = Regles.objects.filter((Q(source=self) | Q(destination=self)) & Q(etat="Production")).values("regle")
        regles_invalides = regles_deprecated.exclude(Q(regle__in=regles_production))
        deployment = RulesDeployment()
        deployment.remove_rules(regles_invalides)
        regles_deprecated.delete()


class Flux(models.Model):
    """
    Model for flow between two :model:`Database.Hote`.
    Even if the two routers are optional, it is recommended to fill at least one of the fields.
    If the value for an router is null, it is considered representing all the routers present in the topology.
    """
    idflux = models.AutoField(db_column='idFlux', primary_key=True)
    type = models.CharField(db_column='Type', max_length=45)
    hote_dst = models.ForeignKey(Hote, to_field='idhote', db_column='Hôte_dst', related_name='hote_dst', null=True)
    hote_src = models.ForeignKey(Hote, to_field='idhote', db_column='Hôte_src', related_name='hote_src', null=True)

    class Meta:
        db_table = 'Flux'


class Regles(models.Model):
    """
    Model for saving rules associated with :model:`Database.Switch`.
    It is recommended to keep up-to-date this model with the production,
    as the controller could ask to apply the rules in the Database.
    """
    idregle = models.AutoField(db_column='idRegle', primary_key=True)
    typeregle = models.CharField(db_column='TypeRegle', max_length=40, blank=True, null=True)
    regle = models.TextField(db_column='Regle', blank=True, null=True)
    idswitch = models.ForeignKey(Switch, to_field='idswitch', db_column='idSwitch')
    source = models.ForeignKey(Hote, related_name="source", verbose_name="Source", null=True)
    destination = models.ForeignKey(Hote, related_name="destination", verbose_name="Destination", null=True)
    etat = FSMField(default="Production")

    @transition(field=etat, source="Production", target="Deprecated")
    def ChangeRulesStatus(self):
        """
        This transition method does nothing, it needs to be called just to make a transition for the etat field.
        :return:
        """
        pass

    def switch(self):
        """
        Return the name of the :model:`Database.Switch` associated with this rule.
        :return:
        """
        return self.idswitch.nomswitch

    class Meta:
        db_table = 'Règles'
        verbose_name = "Règle"


class Stats(models.Model):
    """
    Model which holds all the data per :model:`Database.Flux` of the :model:`Database.Switch`.
    """
    time = models.DateTimeField(db_column='Time', null=False)
    bytes = models.BigIntegerField(db_column='Bytes', blank=True, null=True)
    packets = models.BigIntegerField(db_column='Packets', blank=True, null=True)
    idflux = models.ForeignKey(Flux, to_field='idflux', db_column='idFlux')
    idswitch = models.ForeignKey(Switch, to_field='idswitch', db_column='idSwitch', null=False)

    class Meta:
        db_table = 'Stats'


class Statsport(models.Model):
    """
    Model for save stats send by controlllers about :model:`Database.Port`.
    """
    time = models.DateTimeField(db_column='Time')
    port_idport = models.OneToOneField(Port, to_field='idport', db_column='Port_idPort', unique=True)

    class Meta:
        db_table = 'StatsPort'
        unique_together = (('port_idport', 'time'),)



class Switchlink(models.Model):
    """
    This model is used for representing logical links between two :model:`Database.Switch`.
    """
    idport1 = models.OneToOneField(Port, to_field='idport', db_column='idPort1', related_name='idport1', unique=True)
    idport2 = models.OneToOneField(Port, to_field='idport', db_column='idPort2', related_name='idport2', unique=True)

    class Meta:
        db_table = 'SwitchLink'
        unique_together = (('idport1', 'idport2'),)


# Import Database signals
from Database.signals import post_save_hote, pre_delete_hote

#Import other apps class
from Rules_Generation.manager import Manager
from Rules_Deployment.rules import RulesDeployment