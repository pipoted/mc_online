# coding=utf-8
"""mc_online URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls import url
from django.views.static import serve
from mc_online.settings import MEDIA_ROOT

from users.views import (
	LoginView, RegisterView, ActiveUserView,
	ForgetPwdView, ResetView, ModifyPwdView,
)
from organization.views import OrgView

urlpatterns = [
	path('xadmin/', xadmin.site.urls),
	path('', TemplateView.as_view(template_name='index.html'), name='index'),
	path('login/', LoginView.as_view(), name='login'),
	path('register/', RegisterView.as_view(), name='register'),
	path('captcha/', include('captcha.urls')),
	path('forget/', ForgetPwdView.as_view(), name='forget_pwd'),
	# 邮件验证界面
	url(r'^active/(?P<active_code>.*?)/$', ActiveUserView.as_view(),
			name='user_active'),
	url(r'^reset/(?P<active_code>.*?)/$', ResetView.as_view(),
			name='reset_pwd'),
	url(r'^modify_pwd/(?P<active_code>.*?)/$', ModifyPwdView.as_view(),
			name='modify_pwd'),
	
	# 课程机构url配置
	url(r'^org/', include('organization.urls')),
	
	# 课程相关url配置
	url(r'^course/', include('courses.urls')),
	
	# 上传文件访问
	url(r'^media/(?P<path>.*)/$', serve, {'document_root': MEDIA_ROOT}),
]
