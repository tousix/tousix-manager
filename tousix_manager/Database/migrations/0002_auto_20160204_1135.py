# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Database', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='switch',
            name='idpop',
            field=models.ForeignKey(null=True, db_column='idPOP', to='Database.Pop', blank=True),
        ),
    ]
