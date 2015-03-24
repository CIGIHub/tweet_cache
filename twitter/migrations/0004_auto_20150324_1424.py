# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0003_auto_20150324_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='analyticsreport',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 3, 24, 18, 24, 8, 454518, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='analyticsreport',
            name='user',
            field=models.ForeignKey(default=1, to='twitter.User'),
            preserve_default=False,
        ),
    ]
