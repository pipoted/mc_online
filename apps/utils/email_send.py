# coding=utf-8
from django.core.mail import send_mail
from random import randint, choice

from users.models import EmailVarifyRecord
from mc_online.settings import EMAIL_FROM


def send_register_email(email, send_type='register'):
	"""
	发送注册邮件
	:param send_type: 邮件类型,是注册还是找回密码
	:type send_type: str
	:type email: UserProfile
	"""
	email_record = EmailVarifyRecord()
	random_str = generate_random_str(max_length=16)
	email_record.code = random_str
	email_record.email = email
	email_record.send_type = send_type
	email_record.save()
	
	# 准备发送邮件
	email_title = ''
	email_body = ''
	
	if send_type == 'register':
		email_title = '注册激活链接'
		email_body = '点击如下链接激活您的账号: http://127.0.0.1:8002/active/{0}'.format(
				random_str)
		
		send_status = send_mail(subject=email_title, message=email_body,
				from_email=EMAIL_FROM, recipient_list=[email])
		if send_status:
			pass
	elif send_type == 'forget':
		email_title = '密码充值链接'
		email_body = '点击如下链接重置您的密码: http://127.0.0.1:8002/reset/{0}'.format(
				random_str)
		
		send_status = send_mail(subject=email_title, message=email_body,
				from_email=EMAIL_FROM, recipient_list=[email])
		if send_status:
			pass


# 生成一串随机字符串
def generate_random_str(max_length=8):
	random_str = []
	for i in range(0, max_length):
		random_str.append(choice(
				chr(randint(65, 90)), chr(randint(97, 122)), str(randint(0, 9))
		))
	
	return random_str
