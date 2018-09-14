# coding=utf-8
from django.conf.urls import url, include

urlpatterns = [
	url(r'^list/$', OrgView.as_view(), name='course_list'),  # 课程机构列表页
]
