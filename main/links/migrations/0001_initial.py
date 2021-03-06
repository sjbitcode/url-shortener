# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-29 05:37
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
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('destination', models.URLField(help_text='The destination url', max_length=300, verbose_name='Destination Url')),
                ('key', models.CharField(help_text='The unique identifier for the link', max_length=80, verbose_name='Key')),
                ('total_clicks', models.PositiveIntegerField(default=0, help_text='The total clicks on this link', verbose_name='Total clicks')),
                ('user', models.ForeignKey(blank=True, help_text='The creator of the link', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='links', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
