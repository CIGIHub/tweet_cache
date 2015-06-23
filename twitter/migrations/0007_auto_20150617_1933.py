# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0006_auto_20150515_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='text',
            field=models.CharField(max_length=1028),
        ),
    ]
