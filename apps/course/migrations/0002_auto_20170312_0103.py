# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-12 01:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseresource',
            name='download',
            field=models.FileField(upload_to='/course/resource/%Y/%m', verbose_name='\u8d44\u6e90\u6587\u4ef6\u5730\u5740'),
        ),
    ]