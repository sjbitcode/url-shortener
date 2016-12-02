# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-26 20:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0005_auto_20161115_2208'),
        ('analytics', '0002_referer_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Country name', max_length=120, verbose_name='Country name')),
                ('code', models.CharField(help_text='Country code', max_length=5, verbose_name='Country code')),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_clicks', models.PositiveIntegerField(default=0, help_text='The total clicks for this region', verbose_name='Total region clicks')),
                ('last_visited', models.DateTimeField(default=django.utils.timezone.now)),
                ('country', models.ForeignKey(default=None, blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='regions', to='analytics.Country', verbose_name='Country')),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='regions', to='links.Link', verbose_name='Link')),
            ],
        ),
    ]