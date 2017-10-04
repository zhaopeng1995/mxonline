# -*- encoding:utf-8 -*-
# --------------------------------
# author : dbird
# create_time : 2017/3/20 0:55
# --------------------------------
from django.conf.urls import url, include
from django.contrib import admin
import xadmin
from django.views.generic import TemplateView
from django.views.static import serve

from Mxonline.settings import MEDIA_ROOT
from organization.views import OrgView
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView

urlpatterns = [

]