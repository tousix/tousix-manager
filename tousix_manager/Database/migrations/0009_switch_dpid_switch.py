# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
import tousix_manager.Database.fields
from django.apps import apps
from django.db.models import F


def copy_field():
    MyModel = apps.get_model('Database', 'Switch')
    MyModel.objects.all().update(dpid_switch=F('idswitch'))

class Migration(migrations.Migration):

    dependencies = [
        ('Database', '0008_faucet_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='switch',
            name='dpid_switch',
            field=tousix_manager.Database.fields.PositiveBigIntegerField(default=1),
        ),
        migrations.RunPython(copy_field)
    ]
