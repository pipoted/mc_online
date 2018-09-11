# coding=utf-8
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class UserProfile(AbstractUser):
	"""
	用户表
	昵称,生日,性别,地址,手机号,头像
	"""
	nick_name = models.CharField(max_length=50, verbose_name=u'昵称', default='')
	birthday = models.DateField(verbose_name=u'生日', null=True, blank=True)
	gender = models.CharField(choices=(('male', u'男'), ('female', u'女')),
			default='female', max_length=7)
	address = models.CharField(max_length=100, default=u'')
	mobile = models.CharField(max_length=11, null=True, blank=True)
	image = models.ImageField(upload_to='image/%Y/%m',
			default=u'image/default.png', max_length=100)
	
	
	class Meta:
		verbose_name = '用户信息'
		verbose_name_plural = verbose_name
	
	
	def __unicode__(self):
		return self.username


class EmailVarifyRecord(models.Model):
	"""
	邮箱验证码
	验证码,邮箱,验证码类型,发送时间
	"""
	code = models.CharField(max_length=20, verbose_name=u'验证码')
	email = models.EmailField(max_length=50, verbose_name=u'邮箱')
	send_type = models.CharField(choices=(('register', u'注册'),
	('forget', '找回密码')), max_length=10, verbose_name=u'验证码类型')
	send_time = models.DateTimeField(default=datetime.now,
			verbose_name=u'发送时间')
	
	
	class Meta:
		verbose_name = u'邮箱验证码'
		verbose_name_plural = verbose_name
	
	
	def __unicode__(self):
		return '{0}({1})'.format(self.code, self.email)


class Banner(models.Model):
	"""
	轮播图信息
	轮播图标题, 轮播图图片, 图片访问地址, 图片展示顺序, 添加时间
	"""
	title = models.CharField(max_length=100, verbose_name=u'标题')
	image = models.ImageField(upload_to='banner/%Y/%m', verbose_name=u'轮播图',
			max_length=100)
	url = models.URLField(max_length=200, verbose_name=u'访问地址')
	index = models.IntegerField(default=100, verbose_name=u'轮播顺序')
	add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
	
	
	class Meta:
		verbose_name = u'轮播图'
		verbose_name_plural = verbose_name
