# coding=utf-8
import xadmin
from xadmin import views
from .models import EmailVarifyRecord, Banner


class BaseSetting(object):
	enable_themes = True
	use_bootswatch = True


class GlobalSetting(object):
	site_title = 'MC后台管理系统'
	site_footer = 'MC在线网'
	menu_style = 'accordion'


class EmailVarifyRecordAdmin(object):
	list_display = [
		'code', 'email', 'send_type', 'send_time',
	]
	search_fields = [
		'code', 'email', 'send_type',
	]
	list_filter = [
		'code', 'email', 'send_type', 'send_time',
	]


class BannerAdmin(object):
	list_display = [
		'title', 'image', 'url', 'index', 'add_time',
	]
	search_fields = [
		'title', 'image', 'index',
	]
	list_filter = [
		'title', 'image', 'url', 'index', 'add_time',
	]


xadmin.site.register(EmailVarifyRecord, EmailVarifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
