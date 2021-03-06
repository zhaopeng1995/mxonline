# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import models

from organization.models import CourseOrg, Teacher


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'课程名称')
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    detail = models.TextField(verbose_name=u'课程详情')
    degree = models.CharField(choices=(('cj', u'初级'), ('zj', u'中级'), ('gj', u'高级')), max_length=10)
    teacher = models.ForeignKey(Teacher, verbose_name=u'讲师', null=True , blank=True)
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长')
    studentsNums = models.IntegerField(default=0, verbose_name=u'学习人数')
    favNums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(upload_to='courses/%Y/%d', verbose_name=u'封面')
    clickNums = models.IntegerField(default=0, verbose_name=u'点击数')
    category = models.CharField(default=u'后端开发', max_length=32, verbose_name=u'课程类别')
    tag = models.CharField(default='', max_length=32, verbose_name=u'课程标签')
    course_org = models.ForeignKey(CourseOrg, verbose_name=u'课程机构', null=True, blank=True)
    need_known = models.CharField(default='', max_length=300 , verbose_name=u'课程须知')
    teacher_tips = models.CharField(default='', max_length=300, verbose_name=u'讲师提示')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'点击数')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    # 获取课程章节数目
    def get_zj_nums(self):
        return self.lesson_set.all().count()

    # 获取课程所有章节
    def get_course_chapter(self):
        return self.lesson_set.all()


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.course.name + ' - ' + self.name

    # 获取章节所有视频
    def get_chapter_video(self):
        return self.video_set.all()


class Video(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'视频名')
    lesson = models.ForeignKey(Lesson, null=True, blank=True, verbose_name=u'章节')
    url = models.CharField(max_length=200, default='', verbose_name=u'访问地址')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.lesson.name + ' - ' + self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'资源名')
    download = models.FileField(upload_to='/course/resource/%Y/%m', verbose_name='资源文件地址')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name
