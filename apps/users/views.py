# -*- encoding:utf-8 -*-

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View

from course.models import Course
from operation.models import UserCourse
from operation.models import UserFavorite
from organization.models import Teacher, CourseOrg
from users.forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from users.models import UserProfile, EmailVerifyRecord
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', )

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html")
                else:
                    return render(request, "login.html", {'msg': u"用户未激活！"})
            else:
                return render(request, "login.html", {'msg': u"用户名或密码错误！"})
        else:
            return render(request, "login.html", {'login_form': login_form})


class LogOutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm(request.POST)
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form, "msg": "该邮箱已经注册"})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()
            send_register_email(user_name, "register")
            return render(request, "login.html")
        else:
            print(u"验证码错误")
            return render(request, 'register.html', {"register_form": register_form, "msg": "验证码错误"})


class ActiveUserView(View):
    def get(self, request, active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
            return render(request, "login.html")
        else:
            return render(request, "active_fail.html")


class ForgetPwdView(View):
    def get(self, request):
        forgetpwd_form = ForgetPwdForm()
        return render(request, "forgetpwd.html", {"forgetpwd_form": forgetpwd_form})

    def post(self, request):
        forgetpwd_form = ForgetPwdForm(request.POST)
        if forgetpwd_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, "send_success.html", {"email": email})
        else:
            print(u"验证码错误")
            return render(request, 'register.html', {"forget_form": forgetpwd_form, "msg": "验证码错误"})


class ResetView(View):
    def get(self, request, active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
                record.is_used = True
            return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "active_fail.html")


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {"email": email, "msg": "密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, 'password_reset.html', {"email": email, "modify_form": modify_form})


class UserInfoView(LoginRequiredMixin, View):
    '''
    用户个人信息
    '''

    def get(self, request):
        user = UserProfile.objects.get(username=request.user.username)
        ret_dict = {'user': user}
        return render(request, 'usercenter-info.html', ret_dict)

    def post(self, request):
        userinfo_form = UserInfoForm(request.POST, instance=request.user)
        if userinfo_form.is_valid():
            userinfo_form.save()
            return JsonResponse({"status": 'success'})
        else:
            return JsonResponse(userinfo_form.errors)


class UploadImageView(LoginRequiredMixin, View):
    '''
    用户修改头像
    '''

    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            image = image_form.cleaned_data['image']
            request.user.image = image
            request.user.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail'})


class UpdatePwdView(View):
    '''
    个人中心修改用户密码
    '''

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return JsonResponse({"status": "fail", "msg": "密码不一致"})
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return JsonResponse({"status": "success", "msg": "密码修改成功"})
        else:
            return JsonResponse({"status": "fail", "msg": "填写错误"})


class SendEmailCodeView(LoginRequiredMixin, View):
    '''
    用户修改邮箱发送验证码
    '''

    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return JsonResponse({'email': "邮箱已经存在"})
        send_register_email(email, "update_email")
        return JsonResponse({'status': 'success'}, safe=True)


class UpdateEmailView(LoginRequiredMixin, View):
    '''
    用户修改个人邮箱
    '''

    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        exist_record = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email', is_used=False)

        if exist_record:
            if exist_record.count() == 1:
                record = exist_record.get(code=code)
                user = request.user
                user.email = email
                record.is_used = True
                user.save()
                return JsonResponse({"status": 'success'})
            else:
                return JsonResponse({"email": '验证码异常:多条验证码'})

        else:
            return JsonResponse({"email": '验证码错误'})


class UserCourseView(LoginRequiredMixin, View):
    '''
    我的课程
    '''

    def get(self, request):
        my_courses = UserCourse.objects.filter(user=request.user)
        ret_dict = {'user': request.user, 'my_courses': my_courses}
        return render(request, 'usercenter-mycourse.html', ret_dict)


# 用户个人中心收藏 begin
class UserFavCourseView(LoginRequiredMixin, View):
    '''
    我收藏的课程
    '''

    def get(self, request):
        all_courses_ids = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type='1')
        all_courses_ids = [fav_course.fav_id for fav_course in fav_courses]
        all_courses = Course.objects.filter(id__in=all_courses_ids)
        ret_dict = {'all_courses': all_courses}
        return render(request, 'usercenter-fav-course.html', ret_dict)


class UserFavTeacherView(LoginRequiredMixin, View):
    '''
    我收藏的讲师
    '''

    def get(self, request):
        all_teachers_ids = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type='3')
        all_teachers_ids = [fav_course.fav_id for fav_course in fav_teachers]
        all_teachers = Teacher.objects.filter(id__in=all_teachers_ids)
        ret_dict = {'all_teachers': all_teachers}
        return render(request, 'usercenter-fav-teacher.html', ret_dict)


class UserFavOrgView(LoginRequiredMixin, View):
    '''
    我收藏的机构
    '''

    def get(self, request):
        all_orgs_ids = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type='2')
        all_orgs_ids = [fav_course.fav_id for fav_course in fav_orgs]
        all_orgs = CourseOrg.objects.filter(id__in=all_orgs_ids)
        ret_dict = {'all_orgs': all_orgs}
        return render(request, 'usercenter-fav-org.html', ret_dict)


# 用户个人中心收藏 end


class UserMessageView(LoginRequiredMixin, View):
    '''
    用户个人信息
    '''

    def get(self, request):
        user = UserProfile.objects.get(username=request.user.username)
        ret_dict = {'user': user}
        return render(request, 'usercenter-message.html', ret_dict)

# def userlogin(request):
#     if request.method == "POST":
#         user_name = request.POST.get("username", "")
#         pass_word = request.POST.get("password", "")
#         user = authenticate(username=user_name, password=pass_word)
#         if user is not None:
#             login(request, user)
#             return render(request, "index.html", {})
#         else:
#             return render(request, "login.html", {"msg": u"用户名或密码错误！"})
#     if request.method == "GET":
#         return render(request, 'login.html', {})
