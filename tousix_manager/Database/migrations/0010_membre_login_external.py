# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Database', '0009_switch_dpid_switch'),
    ]

    operations = [
        migrations.AddField(
            model_name='membre',
            name='login_external',
            field=models.CharField(default='guest', max_length=35),
        ),
    ]
