# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0002_user_current_followers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Analytics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('followers', models.PositiveIntegerField(default=0)),
                ('following', models.PositiveIntegerField(default=0)),
                ('listed', models.PositiveIntegerField(default=0)),
                ('tweet_count', models.PositiveIntegerField(default=0)),
                ('retweet_count', models.PositiveIntegerField(default=0)),
                ('reply_count', models.PositiveIntegerField(default=0)),
                ('user_mention_count', models.PositiveIntegerField(default=0)),
                ('link_count', models.PositiveIntegerField(default=0)),
                ('hashtag_count', models.PositiveIntegerField(default=0)),
                ('user', models.ForeignKey(to='twitter.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AnalyticsReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tweets_reweeted_count', models.PositiveIntegerField(default=0)),
                ('tweets_favorited_count', models.PositiveIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='user',
            name='capture_analytics',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='capture_tweets',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
