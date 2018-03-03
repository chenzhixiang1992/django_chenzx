# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-03-03 17:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, default='image/avatar/you.png', max_length=200, null=True, upload_to='image/avatar', verbose_name='头像'),
        ),
    ]
