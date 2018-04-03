# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Database', '0007_merge_faucet'),
    ]

    operations = [
        migrations.AddField(
            model_name='switch',
            name='faucet_class',
            field=models.CharField(blank=True, max_length=35),
        ),
        migrations.AddField(
            model_name='switchlink',
            name='name',
            field=models.CharField(default='link', max_length=25),
        ),
    ]
