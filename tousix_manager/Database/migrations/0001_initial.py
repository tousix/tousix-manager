# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tousix_manager.Database.fields
import django_fsm
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ConnectionType',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('connection_type', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'Connection_type',
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('idcontact', models.AutoField(serialize=False, db_column='idContact', primary_key=True)),
                ('nomcontact', models.CharField(blank=True, verbose_name='Nom', db_column='NomContact', null=True, max_length=50)),
                ('prenomcontact', models.CharField(blank=True, verbose_name='Prénom', db_column='PrenomContact', null=True, max_length=50)),
                ('adressecontact', models.CharField(blank=True, verbose_name='Adresse', db_column='AdresseContact', null=True, max_length=300)),
                ('mailcontact', models.EmailField(blank=True, verbose_name='Mail', db_column='MailContact', null=True, max_length=100)),
                ('telcontact', models.CharField(blank=True, verbose_name='Téléphone', db_column='TelContact', null=True, max_length=14)),
            ],
            options={
                'db_table': 'Contact',
            },
        ),
        migrations.CreateModel(
            name='Contorleswitch',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'ContrôleSwitch',
            },
        ),
        migrations.CreateModel(
            name='Controleur',
            fields=[
                ('idctrl', models.AutoField(serialize=False, db_column='IdCTRL', primary_key=True)),
                ('ipctrl', models.GenericIPAddressField(blank=True, db_column='IPCTRL', null=True)),
            ],
            options={
                'db_table': 'Contrôleur',
            },
        ),
        migrations.CreateModel(
            name='Flux',
            fields=[
                ('idflux', models.AutoField(serialize=False, db_column='idFlux', primary_key=True)),
                ('type', models.CharField(db_column='Type', max_length=45)),
            ],
            options={
                'db_table': 'Flux',
            },
        ),
        migrations.CreateModel(
            name='Hote',
            fields=[
                ('idhote', models.AutoField(serialize=False, db_column='IdHote', primary_key=True)),
                ('nomhote', models.CharField(blank=True, verbose_name='Nom routeur', db_column='NomHote', max_length=30)),
                ('machote', tousix_manager.Database.fields.MACAddressField(verbose_name='Adresse MAC', db_column='MACHote', max_length=17)),
                ('ipv4hote', models.GenericIPAddressField(verbose_name='Adresse IPv4', db_column='IPv4Hote', null=True)),
                ('ipv6hote', models.GenericIPAddressField(verbose_name='Adresse IPv6', db_column='IPv6Hote', null=True)),
                ('valid', models.BooleanField(default=False)),
                ('etat', django_fsm.FSMField(default='Inactive', max_length=50)),
            ],
            options={
                'db_table': 'Hôte',
            },
        ),
        migrations.CreateModel(
            name='LogSwitch',
            fields=[
                ('idlog', models.AutoField(serialize=False, primary_key=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('level', models.CharField(max_length=10)),
                ('message', models.TextField()),
                ('json', models.TextField(null=True)),
            ],
            options={
                'db_table': 'SwitchLog',
            },
        ),
        migrations.CreateModel(
            name='Membre',
            fields=[
                ('idmembre', models.AutoField(serialize=False, db_column='idMembre', primary_key=True)),
                ('nommembre', models.CharField(blank=True, verbose_name='Nom membre', db_column='NomMembre', null=True, max_length=30)),
                ('url', models.URLField(verbose_name='Lien site web', null=True)),
                ('statut', models.CharField(blank=True, db_column='Statut', null=True, max_length=12)),
                ('asnumber', models.PositiveIntegerField(verbose_name='N°AS', db_column='ASNumber')),
                ('fqdn_host', models.CharField(verbose_name='FQDN Routeur', max_length=30, default='Undefined')),
                ('billing', models.OneToOneField(related_name='billing', blank=True, parent_link=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Database.Contact')),
                ('noc', models.OneToOneField(related_name='noc', blank=True, parent_link=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Database.Contact')),
                ('technical', models.OneToOneField(related_name='technical', blank=True, parent_link=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Database.Contact')),
                ('approved', models.BooleanField(default=False)),
                ('connexion_type', models.ForeignKey(to='Database.ConnectionType', blank=True, verbose_name='Type de connexion', null=True)),
            ],
            options={
                'db_table': 'Membre',
            },
        ),
        migrations.CreateModel(
            name='Pop',
            fields=[
                ('idpop', models.AutoField(serialize=False, db_column='idPOP', primary_key=True)),
                ('nompop', models.CharField(blank=True, db_column='NomPOP', null=True, max_length=30)),
                ('adressepop', models.TextField(blank=True, db_column='AdressePOP', null=True, max_length=300)),
            ],
            options={
                'db_table': 'POP',
            },
        ),
        migrations.CreateModel(
            name='Port',
            fields=[
                ('idport', models.AutoField(serialize=False, db_column='idPort', primary_key=True)),
                ('numport', models.IntegerField(blank=True, db_column='numPort', null=True)),
                ('typeport', models.CharField(blank=True, db_column='TypePort', null=True, max_length=10)),
                ('usable', models.BooleanField(db_column='Usable')),
            ],
            options={
                'db_table': 'Port',
            },
        ),
        migrations.CreateModel(
            name='Regles',
            fields=[
                ('idregle', models.AutoField(serialize=False, db_column='idRegle', primary_key=True)),
                ('typeregle', models.CharField(blank=True, db_column='TypeRegle', null=True, max_length=40)),
                ('regle', models.TextField(blank=True, db_column='Regle', null=True)),
                ('etat', django_fsm.FSMField(default='Production', max_length=50)),
                ('destination', models.ForeignKey(related_name='destination', verbose_name='Destination', to='Database.Hote', null=True)),
            ],
            options={
                'db_table': 'Règles',
                'verbose_name': 'Règle',
            },
        ),
        migrations.CreateModel(
            name='Stats',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(db_column='Time')),
                ('bytes', models.BigIntegerField(blank=True, db_column='Bytes', null=True)),
                ('packets', models.BigIntegerField(blank=True, db_column='Packets', null=True)),
                ('idflux', models.ForeignKey(db_column='idFlux', to='Database.Flux')),
            ],
            options={
                'db_table': 'Stats',
            },
        ),
        migrations.CreateModel(
            name='Statsport',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(db_column='Time')),
                ('port_idport', models.OneToOneField(db_column='Port_idPort', to='Database.Port')),
            ],
            options={
                'db_table': 'StatsPort',
            },
        ),
        migrations.CreateModel(
            name='Switch',
            fields=[
                ('idswitch', tousix_manager.Database.fields.PositiveBigIntegerField(serialize=False, db_column='idSwitch', primary_key=True)),
                ('nomswitch', models.CharField(blank=True, db_column='nomSwitch', null=True, max_length=20)),
                ('ipswitch', models.CharField(blank=True, db_column='IPSwitch', null=True, max_length=39)),
                ('idpop', models.OneToOneField(db_column='idPOP', to='Database.Pop', blank=True, null=True)),
            ],
            options={
                'db_table': 'Switch',
            },
        ),
        migrations.CreateModel(
            name='Switchlink',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('idport1', models.OneToOneField(db_column='idPort1', related_name='idport1', to='Database.Port')),
                ('idport2', models.OneToOneField(db_column='idPort2', related_name='idport2', to='Database.Port')),
            ],
            options={
                'db_table': 'SwitchLink',
            },
        ),
        migrations.CreateModel(
            name='UserMembre',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('membre', models.ForeignKey(to='Database.Membre')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'UserMembre',
            },
        ),
        migrations.AddField(
            model_name='stats',
            name='idswitch',
            field=models.ForeignKey(db_column='idSwitch', to='Database.Switch'),
        ),
        migrations.AddField(
            model_name='regles',
            name='idswitch',
            field=models.ForeignKey(db_column='idSwitch', to='Database.Switch'),
        ),
        migrations.AddField(
            model_name='regles',
            name='source',
            field=models.ForeignKey(related_name='source', verbose_name='Source', to='Database.Hote', null=True),
        ),
        migrations.AddField(
            model_name='port',
            name='idswitch',
            field=models.ForeignKey(db_column='idSwitch', to='Database.Switch'),
        ),
        migrations.AddField(
            model_name='membre',
            name='idpop',
            field=models.ForeignKey(db_column='idPoP', to='Database.Pop', null=True),
        ),
        migrations.AddField(
            model_name='logswitch',
            name='idswitch',
            field=models.ForeignKey(db_column='idSwitch', to='Database.Switch'),
        ),
        migrations.AddField(
            model_name='hote',
            name='idmembre',
            field=models.ForeignKey(db_column='idMembre', to='Database.Membre'),
        ),
        migrations.AddField(
            model_name='hote',
            name='idport',
            field=models.ForeignKey(db_column='idPort', to='Database.Port', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='flux',
            name='hote_dst',
            field=models.ForeignKey(db_column='Hôte_dst', related_name='hote_dst', to='Database.Hote', null=True),
        ),
        migrations.AddField(
            model_name='flux',
            name='hote_src',
            field=models.ForeignKey(db_column='Hôte_src', related_name='hote_src', to='Database.Hote', null=True),
        ),
        migrations.AddField(
            model_name='controleur',
            name='idpop',
            field=models.OneToOneField(db_column='idPOP', to='Database.Pop'),
        ),
        migrations.AddField(
            model_name='contorleswitch',
            name='idctrl',
            field=models.ForeignKey(db_column='IdCTRL', to='Database.Controleur'),
        ),
        migrations.AddField(
            model_name='contorleswitch',
            name='idswitch',
            field=models.ForeignKey(db_column='idSwitch', to='Database.Switch'),
        ),
        migrations.AlterUniqueTogether(
            name='switchlink',
            unique_together=set([('idport1', 'idport2')]),
        ),
        migrations.AlterUniqueTogether(
            name='statsport',
            unique_together=set([('port_idport', 'time')]),
        ),
        migrations.AlterUniqueTogether(
            name='hote',
            unique_together=set([('idhote', 'idmembre')]),
        ),
    ]
