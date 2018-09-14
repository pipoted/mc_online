# coding=utf-8
from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
	username = forms.CharField(max_length=10, required=True)
	password = forms.CharField(min_length=5, required=True)


class RegisterForm(forms.Form):
	email = forms.EmailField(required=True)
	password = forms.CharField(min_length=5, required=True)
	captcha = CaptchaField(error_messages={'invalid': u'验证码验证错误'})  # 进行验证码的验证


class ForgetForm(forms.Form):
	email = forms.EmailField(required=True)
	captcha = CaptchaField(error_messages={'invalid': u'验证码验证错误'})  # 进行验证码的验证


class ModifyPwdForm(forms.Form):
	password = forms.CharField(min_length=5, required=True)
	re_password = forms.CharField(min_length=5, required=True)
