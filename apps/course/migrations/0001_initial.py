# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-22 15:30
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='\u8bfe\u7a0b\u540d\u79f0')),
                ('desc', models.CharField(max_length=300, verbose_name='\u8bfe\u7a0b\u63cf\u8ff0')),
                ('detail', models.TextField(verbose_name='\u8bfe\u7a0b\u8be6\u60c5')),
                ('degree', models.CharField(choices=[('cj', '\u521d\u7ea7'), ('zj', '\u4e2d\u7ea7'), ('gj', '\u9ad8\u7ea7')], max_length=10)),
                ('learn_times', models.IntegerField(default=0, verbose_name='\u5b66\u4e60\u65f6\u957f')),
                ('studentsNums', models.IntegerField(default=0, verbose_name='\u5b66\u4e60\u4eba\u6570')),
                ('favNums', models.IntegerField(default=0, verbose_name='\u6536\u85cf\u4eba\u6570')),
                ('image', models.ImageField(upload_to='courses/%Y/%d', verbose_name='\u5c01\u9762')),
                ('clickNums', models.IntegerField(default=0, verbose_name='\u70b9\u51fb\u6570')),
                ('category', models.CharField(default='\u540e\u7aef\u5f00\u53d1', max_length=32, verbose_name='\u8bfe\u7a0b\u7c7b\u522b')),
                ('tag', models.CharField(default='', max_length=32, verbose_name='\u8bfe\u7a0b\u6807\u7b7e')),
                ('need_known', models.CharField(default='', max_length=300, verbose_name='\u8bfe\u7a0b\u987b\u77e5')),
                ('teacher_tips', models.CharField(default='', max_length=300, verbose_name='\u8bb2\u5e08\u63d0\u793a')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u70b9\u51fb\u6570')),
                ('course_org', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.CourseOrg', verbose_name='\u8bfe\u7a0b\u673a\u6784')),
                ('teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.Teacher', verbose_name='\u8bb2\u5e08')),
            ],
            options={
                'verbose_name': '\u8bfe\u7a0b',
                'verbose_name_plural': '\u8bfe\u7a0b',
            },
        ),
        migrations.CreateModel(
            name='CourseResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='\u8d44\u6e90\u540d')),
                ('download', models.FileField(upload_to='/course/resource/%Y/%m', verbose_name='\u8d44\u6e90\u6587\u4ef6\u5730\u5740')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course', verbose_name='\u8bfe\u7a0b')),
            ],
            options={
                'verbose_name': '\u8bfe\u7a0b\u8d44\u6e90',
                'verbose_name_plural': '\u8bfe\u7a0b\u8d44\u6e90',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='\u7ae0\u8282\u540d')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course', verbose_name='\u8bfe\u7a0b')),
            ],
            options={
                'verbose_name': '\u7ae0\u8282',
                'verbose_name_plural': '\u7ae0\u8282',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='\u89c6\u9891\u540d')),
                ('url', models.CharField(default='', max_length=200, verbose_name='\u8bbf\u95ee\u5730\u5740')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
                ('lesson', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.Lesson', verbose_name='\u7ae0\u8282')),
            ],
            options={
                'verbose_name': '\u89c6\u9891',
                'verbose_name_plural': '\u89c6\u9891',
            },
        ),
    ]
