# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-04 22:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_auto_20180304_2243'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news_hot',
            name='id',
        ),
        migrations.AlterField(
            model_name='news_hot',
            name='news',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='news.news'),
        ),
    ]
