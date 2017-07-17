# -*- encoding:utf-8 -*-
# --------------------------------
# author : dbird
# create_time : 2017/3/11 22:47
# --------------------------------
from captcha.fields import CaptchaField
from django import forms

from users.models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ModifyPwdForm(forms.Form):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name','birthday','gender','address','mobile']