# coding=utf-8
from datetime import datetime

from django.db import models
from organization.models import CourseOrg, Teacher


# Create your models here.

class Course(models.Model):
	name = models.CharField(max_length=50, verbose_name=u'课程名称')
	desc = models.CharField(max_length=300, verbose_name=u'课程描述')
	detail = models.TextField(verbose_name=u'课程详情')
	degree = models.CharField(choices=(
		('low_level', u'初级'), ('middle_level', u'中级'), ('high_level', u'高级')
	), max_length=20, verbose_name=u'课程等级')
	learn_times = models.IntegerField(default=0, verbose_name=u'学习时长(min)')
	students_nums = models.IntegerField(default=0, verbose_name=u'学习人数')
	fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
	image = models.ImageField(upload_to='courses/%Y/%m', verbose_name=u'封面')
	click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
	add_time = models.DateTimeField(default=datetime.now,
			verbose_name=u'添加时间')
	
	# 外键
	course_org = models.ForeignKey(CourseOrg, verbose_name='课程机构', null=True,
			on_delete=None)
	teacher = models.ForeignKey(Teacher, verbose_name='所属教师', on_delete=None,
			null=True)
	
	
	class Meta:
		verbose_name = u'课程'
		verbose_name_plural = verbose_name
	
	
	def __unicode__(self):
		return self.name
	
	def __str__(self):
		return self.name


class Lesson(models.Model):
	course = models.ForeignKey(Course, verbose_name=u'课程', on_delete=None)
	name = models.CharField(max_length=100, verbose_name=u'章节名')
	add_time = models.DateTimeField(default=datetime.now,
			verbose_name=u'添加时间')
	
	
	class Meta:
		verbose_name = u'章节'
		verbose_name_plural = verbose_name
	
	
	def __unicode__(self):
		return self.name
	
	def __str__(self):
		return self.name


class Video(models.Model):
	lesson = models.ForeignKey(Lesson, verbose_name=u'章节', on_delete=None)
	name = models.CharField(max_length=100, verbose_name=u'视频名')
	add_time = models.DateTimeField(default=datetime.now,
			verbose_name=u'添加时间')
	
	
	class Meta:
		verbose_name = u'视频'
		verbose_name_plural = verbose_name
	
	
	def __unicode__(self):
		return self.name
	
	def __str__(self):
		return self.name


class CourseResource(models.Model):
	course = models.ForeignKey(Course, verbose_name=u'课程', on_delete=None)
	name = models.CharField(max_length=100, verbose_name=u'名称')
	download_url = models.FileField(upload_to='course/resource/%Y/%m',
			verbose_name=u'资源文件', max_length=100)
	add_time = models.DateTimeField(default=datetime.now,
			verbose_name=u'添加时间')
	
	
	class Meta:
		verbose_name = u'课程资源'
		verbose_name_plural = verbose_name
	
	
	def __unicode__(self):
		return self.name
	
	def __str__(self):
		return self.name
