# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='current_followers',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
