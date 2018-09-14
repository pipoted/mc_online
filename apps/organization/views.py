# coding=utf-8
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg, CityDict, Teacher
from .forms import UserAskForm
from operation.models import UserAsk
from courses.models import Course
from operation.models import UserFavorite


class OrgView(View):
	"""
	课程机构列表功能
	"""
	
	def get(self, request):
		# 取得标签信息
		all_orgs = CourseOrg.objects.all()  # 课程机构
		hot_orgs = all_orgs.order_by('-click_nums')[:3]  # 根据点击量对课程进行排名
		
		all_citys = CityDict.objects.all()  # 城市
		
		# 根据城市标签对列表进行筛选
		city_id = request.GET.get('city', '')
		if city_id:
			city_id = int(city_id)
			all_orgs = all_orgs.filter(city_id=city_id)
		
		# 根据类别进行筛选
		category = request.GET.get('ct', '')
		if category:
			all_orgs = all_orgs.filter(category=category)
		
		# 根据学习人数与课程数对列表进行排列
		sort = request.GET.get('sort', '')
		if sort:
			if sort == 'students':
				all_orgs = all_orgs.order_by('-student_nums')
			elif sort == 'courses':
				all_orgs = all_orgs.order_by('-course_nums')
		
		# 对课程机构进行分页
		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1
		
		p = Paginator(all_orgs, 1, request=request)
		orgs = p.page(page)
		
		org_nums = all_orgs.count()
		return render(request, 'org-list.html', {
			'all_orgs': orgs,
			'all_citys': all_citys,
			'org_nums': org_nums,
			'city_id': city_id,
			'category': category,
			'hot_orgs': hot_orgs,
			'sort': sort,
		})


class AddUserAskView(View):
	"""
	用户添加咨询功能
	"""
	
	def post(self, request):
		user_ask_form = UserAskForm(request.POST)
		if user_ask_form.is_valid():
			# 接受表单传过来且经过验证的参数
			name = request.POST.get('name', '')
			if request.is_ajax():
				user_ask_form.save(user_ask_form.cleaned_data)
				# 验证成功返回json数据
				return JsonResponse({'status': 'success'})
		else:
			return JsonResponse({
				'status': 'fail',
				'msg': user_ask_form.errors,
			})


class OrgHomeView(View):
	"""
	机构首页
	"""
	
	def get(self, request, org_id):
		course_org = CourseOrg.objects.get(id=int(org_id))
		# 通过外键关联将课程与教师数据取出
		all_courses = course_org.course_set.all()[:3]
		all_teachers = course_org.teacher_set.all()[:1]
		
		# 判断该页面是否收藏
		has_fav = False
		if request.user.is_authenticated:
			if UserFavorite.objects.filter(user=request.user.id,
					fav_id=course_org.id, fav_type=2):
				has_fav = True
		
		return render(request, 'org-detail-homepage.html', {
			'all_courses': all_courses,
			'all_teachers': all_teachers,
			'course_org': course_org,
			'has_fav': has_fav,
		})


class OrgCourseView(View):
	"""
	机构课程列表
	"""
	
	def get(self, request, org_id):
		course_org = CourseOrg.objects.get(id=int(org_id))
		all_courses = course_org.course_set.all()
		
		# 判断该页面是否收藏
		has_fav = False
		if request.user.is_authenticated:
			if UserFavorite.objects.filter(user=request.user.id,
					fav_id=course_org.id, fav_type=1):
				has_fav = True
		
		# 分页数据处理
		try:
			page = request.GET.get('page', 1)
		except PageNotAnInteger:
			page = 1
		
		p = Paginator(all_courses, 1, request=request)
		page_data = p.page(page)
		
		# fixme: 分页数据显示有问题
		return render(request, 'org-detail-course.html', {
			'all_courses': all_courses,
			'course_org': course_org,
			'page_data': page_data,
			'has_fav': has_fav,
		})


class OrgDescView(View):
	"""
	机构介绍页面
	"""
	
	def get(self, request, org_id):
		course_org = CourseOrg.objects.get(id=int(org_id))
		
		return render(request, 'org-detail-desc.html', {
			'course_org': course_org,
		})


class OrgTeacherView(View):
	"""
	机构讲师页面
	"""
	
	def get(self, request, org_id):
		course_org = CourseOrg.objects.get(id=int(org_id))
		all_teachers = course_org.teacher_set.all()
		
		# 判断该页面是否收藏
		has_fav = False
		if request.user.is_authenticated:
			if UserFavorite.objects.filter(user=request.user.id,
					fav_id=course_org.id, fav_type=3):
				has_fav = True
		
		# todo: 添加一个分页
		return render(request, 'org-detail-teachers.html', {
			'all_teachers': all_teachers,
			'course_org': course_org,
			'has_fav': has_fav,
		})


class AddFavView(View):
	"""
	ajax实现用户收藏以及取消收藏
	"""
	
	def post(self, request):
		fav_id = request.POST.get('fav_id', 0)
		fav_type = request.POST.get('fav_type', 0)  # 收藏的类型
		res = {  # 用于ajax放回的json数据
			'status': None,
			'msg': None,
		}
		# 判断用户是否登录
		if not request.user.is_authenticated:
			res['status'] = 'fail'
			res['msg'] = '用户未登录'
			return JsonResponse(data=res)
		
		exist_records = UserFavorite.objects.filter(user=request.user.id,
				fav_id=int(fav_id), fav_type=int(fav_type))
		if exist_records:
			# 如果该收藏记录已经存在, 则点击操作将取消收藏
			exist_records.delete()
			res['status'] = 'fail'
			res['msg'] = '收藏'
			return JsonResponse(res)
		else:  # 不存在则保存
			if int(fav_id) > 0 and int(fav_type) > 0:
				user_fav = UserFavorite(
						user_id=request.user.id,
						fav_id=int(fav_id),
						fav_type=int(fav_type),
				)
				user_fav.save()
				res['status'] = 'success'
				res['msg'] = '已收藏'
				return JsonResponse(res)  # 收藏成功
			else:
				res['status'] = 'fail'
				res['msg'] = '发生未知问题, 保存出错'
				return JsonResponse(res)  # 收藏失败
