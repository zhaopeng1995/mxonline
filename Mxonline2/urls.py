# -*- coding: utf-8 -*-
"""Mxonline2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
import xadmin
from django.views.generic import TemplateView
from django.views.static import serve

from Mxonline2.settings import MEDIA_ROOT
from organization.views import OrgView
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url('^$', TemplateView.as_view(template_name='index.html'), name='index'),
    # url('^login/$', userlogin, name='login'),
    url('^login/$', LoginView.as_view(), name='login'),
    url('^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='active_user' ),
    url(r'^forgetpwd/$', ForgetPwdView.as_view(), name='forgetpwd'),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='resetpwd'),
    url(r'^modifypwd/$', ModifyPwdView.as_view(), name='modifypwd'),
    # 课程机构url配置
    url(r'^org/', include('organization.urls',namespace='org')),
    # 课程url配置
    url(r'^course/', include('course.urls',namespace='course')),

    # 配置上传那文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {"document_root":MEDIA_ROOT}),

]
