# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-04 22:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_auto_20180207_1625'),
    ]

    operations = [
        migrations.CreateModel(
            name='news_hot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(default=0)),
                ('pubtime', models.DateTimeField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.news')),
            ],
            options={
                'ordering': ['-score'],
            },
        ),
        migrations.AddField(
            model_name='news_profile',
            name='pubtime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='news_profile',
            name='news',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='news_profile', serialize=False, to='news.news'),
        ),
    ]
