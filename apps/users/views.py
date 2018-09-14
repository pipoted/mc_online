# coding=utf-8
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.base import View

from utils.email_send import send_register_email
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm
from .models import EmailVarifyRecord, UserProfile


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


class ActiveUserView(View):
	"""
	激活用户账号
	"""
	
	def get(self, request, active_code):
		all_record = EmailVarifyRecord.objects.filter(code=active_code)
		if all_record:
			for record in all_record:
				email = record.email
				user = UserProfile.objects.get(email=email)
				user.is_active = True
				user.save()
		else:
			return render(request, 'active_fail.html')
		return render(request, 'login.html')


class ResetView(View):
	"""
	邮箱验证过后,跳转到重置密码页面
	"""
	
	def get(self, request, active_code):
		all_record = EmailVarifyRecord.objects.filter(code=active_code)
		if all_record:
			for record in all_record:
				email = record.email
				return render(request, 'password_reset.html', {'email': email})
		else:
			return render(request, 'active_fail.html')
		return render(request, 'login.html')


class ModifyPwdView(View):
	"""
	重置密码功能
	"""
	
	def post(self, request):
		modify_form = ModifyPwdForm(request.POST)
		if modify_form.is_valid():
			password = request.POST.get('password', '')
			re_password = request.POST.get('re_password', '')
			email = request.POST.get('email', '')
			if password != re_password:
				return render(request, 'password_reset.html', {
					'email': email,
					'msg': '两次密码不一致'
				})
			
			user_profile = UserProfile.objects.get(email=email)
			user_profile.password = make_password(password)
			user_profile.save()
			
			return render(request, 'login.html')
		else:
			email = request.POST.get('email', '')
			return render(request, 'password_reset.html', {
				'email': email,
				'modify_form': modify_form
			})


class LoginView(View):
	"""
	实现登录功能
	"""
	
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
				if user.is_active:
					login(request, user=user)  # 进行登录
					return render(request, 'index.html')
				else:
					return render(request, 'index.html', {'msg': '该用户为经过邮箱验证'})
			else:
				return render(request, 'index.html', {'msg': '用户未激活!'})
		else:
			return render(request, 'login.html', {
				'login_form': login_form
			})


class RegisterView(View):
	"""
	实现注册功能
	"""
	
	def get(self, request):
		register_form = RegisterForm()
		return render(request, 'register.html',
				{'register_form': register_form})
	
	def post(self, request):
		register_form = RegisterForm()
		if register_form.is_valid():  # <-- 对验证码的验证已经完成
			email = request.POST.get('email', '')
			pass_word = request.POST.get('password', '')
			
			if UserProfile.objects.filter(email=email):
				return render(request, 'login.html', {
					'msg': '该用户已经存在!',
					'register_form': register_form
				})
			
			user_profile = UserProfile()
			user_profile.email = email
			user_profile.password = make_password(pass_word)
			user_profile.is_active = False
			user_profile.save()
			
			send_register_email(email=user_profile, send_type='register')
			return render(request, 'login.html')
		else:
			return render(request, 'register.html')


class ForgetPwdView(View):
	"""
	实现找回密码功能
	"""
	
	def get(self, request):
		forget_form = ForgetForm()
		return render(request, 'forgetpwd.html', {'forget_form': forget_form})
	
	def post(self, request):
		forget_form = ForgetForm(request.POST)
		if forget_form.is_valid():
			email = request.POST.get('email', '')
			send_register_email(email, 'forget')  # <---邮件发送成功
			
			return render(request, 'send_success.html')
		else:
			return render(request, 'forgetpwd.html',
					{'forget_form': forget_form})
