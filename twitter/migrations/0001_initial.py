# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FollowersStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('followers', models.PositiveIntegerField()),
                ('as_of', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-as_of'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tweet_id', models.BigIntegerField()),
                ('time', models.DateTimeField()),
                ('account', models.CharField(max_length=30)),
                ('profile_image_url', models.CharField(max_length=256)),
                ('text', models.CharField(max_length=140)),
                ('processed_text', models.CharField(max_length=1028, null=True, blank=True)),
                ('hide', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.CharField(max_length=32, blank=True)),
                ('screen_name', models.CharField(max_length=128)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tweet',
            name='user',
            field=models.ForeignKey(blank=True, to='twitter.User', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='followersstats',
            name='user',
            field=models.ForeignKey(blank=True, to='twitter.User', null=True),
            preserve_default=True,
        ),
    ]
