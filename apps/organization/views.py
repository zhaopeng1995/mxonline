# -*- coding: utf-8 -*-
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger

from operation.models import UserFavorite
from organization.forms import UserAskForm
from organization.models import CourseOrg, CityDict, Teacher


class OrgView(View):
    '''
    课程机构列表
    '''

    def get(self, request):
        # 取出所有课程机构
        all_orgs = CourseOrg.objects.all()
        # 取出所有城市
        all_cities = CityDict.objects.all()
        # 取出排名前三的机构

        # 机构搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords)
            )

        hot_orgs = all_orgs.order_by("-clickNums")[:3]
        # 城市筛选
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 类别筛选
        category = request.GET.get('ct', "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 统计筛选后的机构个数
        org_nums = all_orgs.count()

        # 分类排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-studentNums')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-courseNums')

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_orgs, 5, request=request)
        orgs = p.page(page)
        ret_dic = {"all_orgs": orgs, "all_cities": all_cities, "org_nums": org_nums, "city_id": city_id,
                   "category": category, 'hot_orgs': hot_orgs, "sort": sort}
        return render(request, 'org-list.html', ret_dic)


class AddUserAskView(View):
    '''
    用户添加咨询
    '''

    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success" }', content_type='application/json')
        else:
            return HttpResponse("{'status':'fail', 'msg':'提交出错'}", content_type='application/json')


class OrgHomeView(View):
    '''
    机构详情主页
    '''

    def get(self, request, org_id):
        current_page = 'home'
        has_fav = False
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 判断用户登录状态和收藏状态
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:2]
        ret_dic = {"all_courses": all_courses,
                   "all_teachers": all_teachers,
                   'course_org': course_org,
                   'current_page': current_page,
                   'has_fav': has_fav,
                   }
        return render(request, 'org-detail-homepage.html', ret_dic)


class OrgCourseView(View):
    '''
    机构课程展示页
    '''

    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        # 判断用户登录状态和收藏状态
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_courses = course_org.course_set.all()[:3]
        ret_dic = {"all_courses": all_courses,
                   'course_org': course_org,
                   'current_page': current_page,
                   'has_fav': has_fav,
                   }
        return render(request, 'org-detail-course.html', ret_dic)


class OrgDescView(View):
    '''
    机构介绍页
    '''

    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        # 判断用户登录状态和收藏状态
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        ret_dic = {'course_org': course_org,
                   'current_page': current_page,
                   'has_fav': has_fav,
                   }
        return render(request, 'org-detail-desc.html', ret_dic)


class OrgTeacherView(View):
    '''
    机构讲师展示页
    '''

    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        # 判断用户登录状态和收藏状态
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_teachers = course_org.teacher_set.all()
        ret_dic = {'course_org': course_org,
                   'current_page': current_page,
                   'all_teachers': all_teachers,
                   'has_fav': has_fav,
                   }
        return render(request, 'org-detail-teachers.html', ret_dic)


class AddFavOrgView(View):
    '''
    用户收藏以及取消收藏机构
    '''

    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        # 判断用户登录状态
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail" ,"msg": "用户未登录"}', content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 如果记录存在，则表示用户想要取消收藏
            exist_records.delete()
            return HttpResponse('{"status":"success" ,"msg": "收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse('{"status":"success" ,"msg": "已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail" ,"msg": "收藏出错"}', content_type='application/json')


class TeacherListView(View):
    ''''
    授课讲师列表显示页面
    '''

    def get(self, request):
        # 取出所有讲师
        all_teachers = Teacher.objects.all()
        # 取出排名前三的讲师
        hot_teachers = all_teachers.order_by("-favNums")[:3]

        # 机构搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_teachers = all_teachers.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) |
                Q(work_company__icontains=search_keywords)
            )

        # 统计筛选后的讲师个数
        teacher_nums = all_teachers.count()

        # 分类排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == 'hot':
                all_teachers = all_teachers.order_by("-clickNums")

        # 对授课讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_teachers, 5, request=request)
        teachers = p.page(page)

        ret_dic = {"all_teachers": teachers,
                   "hot_teachers": hot_teachers,
                   'teacher_nums': teacher_nums,
                   }

        return render(request, 'teachers-list.html', ret_dic)


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=teacher_id)
        courses = teacher.course_set.all()
        has_fav_teacher = False
        has_fav_org = False

        # 判断用户登录状态
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail" ,"msg": "用户未登录"}', content_type='application/json')
        else:
            if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
                has_fav_teacher = True
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
                has_fav_org = True

        # 取出排名前三的讲师
        hot_teachers = Teacher.objects.order_by("-favNums")[:3]

        ret_dic = {'teacher': teacher,
                   'courses': courses,
                   'hot_teachers': hot_teachers,
                   'has_fav_teacher': has_fav_teacher,
                   'has_fav_org': has_fav_org,
                   }
        return render(request, 'teacher-detail.html', ret_dic)
