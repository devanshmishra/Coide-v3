# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-28 14:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0015_auto_20170428_1730'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['timestamp']},
        ),
    ]
