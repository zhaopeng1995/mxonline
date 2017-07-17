# -*- encoding:utf-8 -*-
# --------------------------------
# author : dbird
# create_time : 2017/3/23 18:42
# --------------------------------
from django.conf.urls import url

from users.views import UserInfoView, UserCourseView, UserFavCourseView, UserMessageView, UploadImageView, \
    UpdatePwdView, \
    SendEmailCodeView, UpdateEmailView, UserFavTeacherView, UserFavOrgView, LogOutView

urlpatterns = [
    # 用户信息
    url(r'info/$', UserInfoView.as_view(), name='user_info'),

    # 用户头像上传
    url(r'image/upload/$', UploadImageView.as_view(), name='image_upload'),

    # 用户个人中心修改密码
    url(r'update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),

    # 用户修改邮箱发送验证码
    url(r'sendemail_code/$', SendEmailCodeView.as_view(), name='send_emailcode'),
    # 用户修改邮箱发送验证码
    url(r'update_email/$', UpdateEmailView.as_view(), name='update_email'),

    # 用户课程
    url(r'course/$', UserCourseView.as_view(), name='user_course'),
    # 用户收藏的课程
    url(r'fav/course/$', UserFavCourseView.as_view(), name='fav_course'),
    # 用户收藏的讲师
    url(r'fav/teacher/$', UserFavTeacherView.as_view(), name='fav_teacher'),
    # 用户收藏的机构
    url(r'fav/org/$', UserFavOrgView.as_view(), name='fav_org'),
    # 用户消息
    url(r'message/$', UserMessageView.as_view(), name='user_message'),


]
