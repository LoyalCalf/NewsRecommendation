# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-06 16:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20180304_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_profile',
            name='avatar',
            field=models.ImageField(default='avatar/default.jpg', upload_to='avatar/%Y%m%d'),
        ),
        migrations.DeleteModel(
            name='Avatar',
        ),
    ]
