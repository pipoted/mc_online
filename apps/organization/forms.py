# coding=utf-8
import re
from django import forms

from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
	class Meta:
		model = UserAsk
		fields = [
			'name', 'mobile', 'course_name',
		]
	
	
	def clean_mobile(self):
		"""
		验证手机号码是否合法
		"""
		mobile = self.cleaned_data.get('mobile')
		REGEX_MOBILE = '^1[835]\d{9}$'
		p = re.compile(REGEX_MOBILE)
		if p.match(p):
			return mobile  # 验证成功将数据返回
		else:
			raise forms.ValidationError(u'手机号格式不正确', code='mobile_invalid')
