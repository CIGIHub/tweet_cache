# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0004_auto_20150324_1424'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='analytics',
            options={'ordering': ('-date',), 'verbose_name_plural': 'analytics'},
        ),
        migrations.AlterModelOptions(
            name='tweet',
            options={'ordering': ('-time',)},
        ),
    ]
