# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TakeInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tname', models.CharField(max_length=10)),
                ('taddr', models.CharField(max_length=100)),
                ('tcode', models.CharField(max_length=6)),
                ('tphone', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uname', models.CharField(max_length=20)),
                ('upwd', models.CharField(max_length=40)),
                ('umail', models.CharField(max_length=20)),
                ('utel', models.CharField(default=b'', max_length=20)),
                ('uaddr', models.CharField(default=b'', max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='takeinfo',
            name='userid',
            field=models.ForeignKey(to='users.UserInfo'),
        ),
    ]
