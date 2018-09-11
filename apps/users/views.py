# coding=utf-8
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


# Create your views here.
def user_login(request):
	if request.method == 'POST':
		user_name = request.POST.get('username', '')
		pass_word = request.POST.get('password', '')
		# 对表单信息进行验证
		user = authenticate(username=user_name, password=pass_word)
		if user is not None:
			login(request, user=user)  # 进行登录
			return render(request, 'index.html')
		else:
			return render(request, 'index.html')
	elif request.method == 'GET':
		return render(request, 'login.html')
