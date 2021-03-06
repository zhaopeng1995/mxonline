# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import models


# Create your models here.

class CityDict(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'城市')
    desc = models.TextField(verbose_name=u'城市描述')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'城市'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'机构名称')
    desc = models.TextField(verbose_name=u'机构描述')
    category = models.CharField(default="pxjg", verbose_name=u'机构类别', max_length=20,
                                choices=(('pxjg', u'培训机构'), ('gx', u'高校'), ('gr', u'个人')))
    clickNums = models.IntegerField(default=0, verbose_name=u'点击数')
    studentNums = models.IntegerField(default=0, verbose_name=u'学习人数')
    courseNums = models.IntegerField(default=0, verbose_name=u'课程数')
    favNums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name=u'封面图')
    address = models.CharField(max_length=150, verbose_name=u'机构地址')
    city = models.ForeignKey(CityDict, verbose_name=u'所在城市')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u'课程机构'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    # 获取课程机构的教师数量
    def get_teacher_nums(self):
        return self.teacher_set.all().count()


class Teacher(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'教师名')
    age = models.IntegerField(default=18, verbose_name=u'年龄')
    work_years = models.IntegerField(default=0, verbose_name=u'工作年限')
    work_company = models.CharField(max_length=50, verbose_name=u'就职公司')
    work_position = models.CharField(max_length=50, verbose_name=u'公司职位')
    image = models.ImageField(upload_to="teacher/%Y/%m", null=True, verbose_name=u'照片')
    points = models.CharField(max_length=50, verbose_name=u'教学特点')
    clickNums = models.IntegerField(default=0, verbose_name=u'点击数')
    favNums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    add_time = models.DateTimeField(default=datetime.now)
    org = models.ForeignKey(CourseOrg, verbose_name=u'所属机构')

    class Meta:
        verbose_name = u'教师'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
