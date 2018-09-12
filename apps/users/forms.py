# coding=utf-8
from django import forms


class LoginForm(forms.Form):
	username = forms.CharField(max_length=10, required=True)
	password = forms.CharField(min_length=5, required=True)
