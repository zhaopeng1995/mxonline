# -*- encoding:utf-8 -*-
# --------------------------------
# author : dbird
# create_time : 2017/3/20 13:46
# --------------------------------
from django.conf.urls import url

from course.views import CourseListView, CourseDetailView, AddFavCourseView, CourseVideoView, CourseCommentView, \
    AddCommentView

urlpatterns = [
    url(r'list/$', CourseListView.as_view(), name='course_list'),
    url(r'detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^add_fav/$', AddFavCourseView.as_view(), name='add_fav_course'),
    url(r'detail/(?P<course_id>\d+)/video/$', CourseVideoView.as_view(), name='course_video'),
    url(r'detail/(?P<course_id>\d+)/comment/$', CourseCommentView.as_view(), name='course_comment'),
    url(r'^add_comment/$', AddCommentView.as_view(), name='add_comment'),

]
