# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from database.fields import PositiveBigIntegerField, MACAddressField


class ConnectionType(models.Model):
    connection_type = models.CharField(max_length=20, null=False)

    class Meta:
        db_table = 'Connection_type'


class Contact(models.Model):
    idcontact = models.AutoField(db_column='idContact', primary_key=True)  # Field name made lowercase.
    nomcontact = models.CharField(db_column='NomContact', max_length=50, blank=True, null=True, verbose_name="Nom")  # Field name made lowercase.
    prenomcontact = models.CharField(db_column='PrenomContact', max_length=50, blank=True, null=True, verbose_name="Prénom")  # Field name made lowercase.
    adressecontact = models.CharField(db_column='AdresseContact', max_length=300, blank=True, null=True, verbose_name="Adresse")  # Field name made lowercase.
    mailcontact = models.EmailField(db_column='MailContact', max_length=100, blank=True, null=True, verbose_name="Mail")  # Field name made lowercase.
    telcontact = models.CharField(db_column='TelContact', max_length=14, blank=True, null=True, verbose_name="Téléphone")  # Field name made lowercase.

    class Meta:
        db_table = 'Contact'


class Pop(models.Model):
    idpop = models.AutoField(db_column='idPOP', primary_key=True)  # Field name made lowercase.
    nompop = models.CharField(db_column='NomPOP', max_length=30, blank=True, null=True)  # Field name made lowercase.
    adressepop = models.TextField(db_column='AdressePOP', max_length=300, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'POP'


class Membre(models.Model):
    idmembre = models.AutoField(db_column='idMembre', primary_key=True)  # Field name made lowercase.
    user = models.OneToOneField(User, null=True)
    nommembre = models.CharField(db_column='NomMembre', max_length=30, blank=True, null=True, verbose_name="Nom membre")  # Field name made lowercase.
    url = models.URLField(null=True, verbose_name="Lien site web")
    statut = models.CharField(db_column='Statut', max_length=12, blank=True, null=True)  # Field name made lowercase.
    asnumber = models.PositiveIntegerField(db_column='ASNumber', verbose_name="N°AS")  # Field name made lowercase.
    connexion_type = models.ForeignKey(ConnectionType, blank=True, null=True, verbose_name="Type de connexion")
    fqdn_host = models.CharField(max_length=30, default="Undefined", verbose_name="FQDN Routeur")
    idpop = models.ForeignKey(Pop, to_field='idpop', db_column='idPoP', null=True)
    billing = models.OneToOneField(Contact, to_field='idcontact', related_name='billing', parent_link=True, blank=True, null=True)
    noc = models.OneToOneField(Contact, to_field='idcontact', related_name='noc', parent_link=True, blank=True, null=True)
    technical = models.OneToOneField(Contact, to_field='idcontact', related_name='technical', parent_link=True, blank=True, null=True)
    approved = models.BooleanField(default=False)

    class Meta:
        db_table = 'Membre'


class Controleur(models.Model):
    idctrl = models.AutoField(db_column='IdCTRL', primary_key=True)  # Field name made lowercase.
    ipctrl = models.GenericIPAddressField(db_column='IPCTRL', blank=True, null=True)  # Field name made lowercase.
    idpop = models.OneToOneField(Pop, to_field='idpop', db_column='idPOP', unique=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Contrôleur'


class Switch(models.Model):
    idswitch = PositiveBigIntegerField(db_column='idSwitch', primary_key=True)  # Field name made lowercase.
    nomswitch = models.CharField(db_column='nomSwitch', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ipswitch = models.CharField(db_column='IPSwitch', max_length=39, blank=True, null=True)  # Field name made lowercase.
    idpop = models.OneToOneField(Pop, to_field='idpop', db_column='idPOP', unique=True, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Switch'


class LogSwitch(models.Model):
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
    idctrl = models.ForeignKey(Controleur, to_field='idctrl', db_column='IdCTRL')  # Field name made lowercase.
    idswitch = models.ForeignKey(Switch, to_field='idswitch', db_column='idSwitch')  # Field name made lowercase.

    class Meta:
        db_table = 'ContrôleSwitch'


class Port(models.Model):
    idport = models.AutoField(db_column='idPort', primary_key=True)  # Field name made lowercase.
    numport = models.IntegerField(db_column='numPort', blank=True, null=True)  # Field name made lowercase.
    typeport = models.CharField(db_column='TypePort', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usable = models.BooleanField(db_column='Usable')  # Field name made lowercase.
    idswitch = models.ForeignKey(Switch, to_field='idswitch', db_column='idSwitch')  # Field name made lowercase.

    def switch(self):
        return self.idswitch.nomswitch

    def string_description(self):
            return "POP " + self.idswitch.idpop.nompop + ": " + self.idswitch.nomswitch + " port " + str(self.numport)

    class Meta:
        db_table = 'Port'


class Hote(models.Model):
    idhote = models.AutoField(db_column='IdHote', primary_key=True)  # Field name made lowercase.
    nomhote = models.CharField(db_column='NomHote', max_length=30, blank=True, verbose_name="Nom routeur")  # Field name made lowercase.
    machote = MACAddressField(db_column='MACHote', verbose_name="Addresse MAC")  # Field name made lowercase.
    ipv4hote = models.GenericIPAddressField(db_column='IPv4Hote', verbose_name="Adresse IPv4", null=True)  # Field name made lowercase.
    ipv6hote = models.GenericIPAddressField(db_column='IPv6Hote', verbose_name="Adresse IPv6", null=True)  # Field name made lowercase.
    idmembre = models.ForeignKey(Membre, to_field='idmembre', db_column='idMembre')  # Field name made lowercase.
    idport = models.ForeignKey(Port, to_field='idport', db_column='idPort', blank=True, null=True)  # Field name made lowercase.
    valid = models.BooleanField(default=False)

    def membre(self):
        return self.idmembre.nommembre

    def switch(self):
        if self.idport is None:
            return "Undefined"
        else:
            return self.idport.idswitch.nomswitch

    def port(self):
        if self.idport is None:
            return "Undefined"
        else:
            return self.idport.numport

    def pop(self):
        if self.idport is None:
            return "Undefined"
        else:
            return self.idport.idswitch.idpop.nompop

    class Meta:
        db_table = 'Hôte'
        unique_together = (('idhote', 'idmembre'),)


class Flux(models.Model):
    idflux = models.AutoField(db_column='idFlux', primary_key=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=45)  # Field name made lowercase.
    hote_dst = models.ForeignKey(Hote, to_field='idhote', db_column='Hôte_dst', related_name='hote_dst', null=True)  # Field name made lowercase.
    hote_src = models.ForeignKey(Hote, to_field='idhote', db_column='Hôte_src', related_name='hote_src', null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Flux'


class Regles(models.Model):
    idregle = models.AutoField(db_column='idRegle', primary_key=True)  # Field name made lowercase.
    typeregle = models.CharField(db_column='TypeRegle', max_length=40, blank=True, null=True)  # Field name made lowercase.
    regle = models.TextField(db_column='Regle', blank=True, null=True)  # Field name made lowercase.
    idswitch = models.ForeignKey(Switch, to_field='idswitch', db_column='idSwitch')  # Field name made lowercase.
    source = models.ForeignKey(Hote, related_name="source", verbose_name="Source", null=True)
    destination = models.ForeignKey(Hote, related_name="destination", verbose_name="Destination", null=True)

    def switch(self):
        return self.idswitch.nomswitch

    class Meta:
        db_table = 'Règles'


class Stats(models.Model):
    time = models.DateTimeField(db_column='Time', null=False)  # Field name made lowercase.
    bytes = models.BigIntegerField(db_column='Bytes', blank=True, null=True)  # Field name made lowercase.
    packets = models.BigIntegerField(db_column='Packets', blank=True, null=True)  # Field name made lowercase.
    idflux = models.ForeignKey(Flux, to_field='idflux', db_column='idFlux')  # Field name made lowercase.
    idswitch = models.ForeignKey(Switch, to_field='idswitch', db_column='idSwitch', null=False)

    class Meta:
        db_table = 'Stats'


class Statsport(models.Model):
    time = models.DateTimeField(db_column='Time')  # Field name made lowercase.
    port_idport = models.OneToOneField(Port, to_field='idport', db_column='Port_idPort', unique=True)  # Field name made lowercase.

    class Meta:
        db_table = 'StatsPort'
        unique_together = (('port_idport', 'time'),)



class Switchlink(models.Model):
    idport1 = models.OneToOneField(Port, to_field='idport', db_column='idPort1', related_name='idport1', unique=True)  # Field name made lowercase.
    idport2 = models.OneToOneField(Port, to_field='idport', db_column='idPort2', related_name='idport2', unique=True)  # Field name made lowercase.

    class Meta:
        db_table = 'SwitchLink'
        unique_together = (('idport1', 'idport2'),)


# Import database signals
from database.signals import post_save_hote, pre_delete_hote