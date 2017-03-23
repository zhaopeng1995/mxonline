# -*- encoding:utf-8 -*-
# --------------------------------
# author : dbird
# create_time : 2017/3/20 13:46
# --------------------------------
from django.conf.urls import url

from organization.views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, \
    AddFavOrgView, TeacherListView, TeacherDetailView

urlpatterns = [
    url(r'^list/$', OrgView.as_view(), name='org_list'),
    url(r'^add_ask/$', AddUserAskView.as_view(), name='add_ask'),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name='org_course'),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='org_desc'),
    url(r'^teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name='org_teacher'),
    url(r'^add_fav/$', AddFavOrgView.as_view(), name='add_fav_org'),
    url(r'^teacher/list/$', TeacherListView.as_view(), name='teacher_list'),
    url(r'^teacher/detail/(?P<teacher_id>\d+)$', TeacherDetailView.as_view(), name='teacher_detail'),

]
