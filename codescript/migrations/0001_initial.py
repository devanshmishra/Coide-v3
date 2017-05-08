# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-28 12:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeScript',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25)),
                ('banner', models.FileField(upload_to='codescript/%y/%m/%d')),
                ('html_file_path', models.FileField(upload_to='codescript')),
                ('css_file_path', models.FileField(upload_to='codescript')),
                ('js_file_path', models.FileField(upload_to='codescript')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('stars', models.IntegerField(default=0)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]