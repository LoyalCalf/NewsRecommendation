# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-07 08:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0007_auto_20180207_1625'),
        ('user', '0002_user_search'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_recommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.news')),
            ],
        ),
        migrations.CreateModel(
            name='user_similarity',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='similaryity', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('similary_user', models.TextField(null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='user_tag',
            name='news_baby',
        ),
        migrations.RemoveField(
            model_name='user_tag',
            name='news_car',
        ),
        migrations.RemoveField(
            model_name='user_tag',
            name='news_food',
        ),
        migrations.RemoveField(
            model_name='user_tag',
            name='news_funny',
        ),
        migrations.RemoveField(
            model_name='user_tag',
            name='news_history',
        ),
        migrations.RemoveField(
            model_name='user_tag',
            name='news_military',
        ),
        migrations.RemoveField(
            model_name='user_tag',
            name='news_world',
        ),
        migrations.AddField(
            model_name='user_recommendation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommendation', to=settings.AUTH_USER_MODEL),
        ),
    ]
