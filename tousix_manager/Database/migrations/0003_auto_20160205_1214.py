# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Database', '0002_auto_20160204_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hote',
            name='nomhote',
            field=models.CharField(max_length=30, db_column='NomHote', verbose_name='Nom routeur'),
        ),
    ]
