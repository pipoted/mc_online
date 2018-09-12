# coding=utf-8
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View

from .models import UserProfile
from .forms import LoginForm


# noinspection PyBroadException
class CustomBackend(ModelBackend):
	
	def authenticate(self, request, username=None, password=None, **kwargs):
		try:
			user = UserProfile.objects.get(
					Q(username=username) | Q(email=username) |
					Q(mobile=username))
			if user.check_password(password):
				return user
		except Exception as e:
			return None


class LoginView(View):
	
	def get(self, request):
		return render(request, 'login.html')
	
	def post(self, request):
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			user_name = request.POST.get('username', '')
			pass_word = request.POST.get('password', '')
			# 对表单信息进行验证
			user = authenticate(username=user_name, password=pass_word)
			if user is not None:
				login(request, user=user)  # 进行登录
				return render(request, 'index.html', {'msg': '用户名或密码错误!'})
		else:
			return render(request, 'login.html', {
				'login_form': login_form
			})


class RegisterView(View):
	
	def get(self, request):
		pass
	
	def post(self, request):
		pass
