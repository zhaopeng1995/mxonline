# -*- encoding:utf-8 -*-
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger

from course.models import Course, CourseResource
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")
        hot_courses = Course.objects.all().order_by("-clickNums")[:3]
        search_keywords = request.GET.get('keywords', '')

        # 课程搜索
        if search_keywords:
            all_courses = all_courses.filter(
                Q(name__icontains=search_keywords) | \
                Q(desc__icontains=search_keywords) | \
                Q(detail__icontains=search_keywords)
            )

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-studentsNums')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-clickNums')

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 9, request=request)
        courses = p.page(page)

        ret_dict = {'courses': courses, 'sort': sort, 'hot_courses': hot_courses}

        return render(request, 'course-list.html', ret_dict)


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        # 增加课程点击数
        course.clickNums += 1
        course.save()

        has_fav_course = False
        has_fav_org = False

        # 判断用户登录状态
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail" ,"msg": "用户未登录"}', content_type='application/json')
        else:
            if UserFavorite.objects.filter(user=request.user, fav_type=1, fav_id=course.id):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=course.course_org_id):
                has_fav_org = True

        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag).filter()
        else:
            relate_courses = []
        users = course.usercourse_set.all()[:5]
        ret_dict = {"course": course, 'users': users, 'relate_courses': relate_courses,
                    'has_fav_course': has_fav_course, 'has_fav_org': has_fav_org}
        return render(request, 'course-detail.html', ret_dict)


class CourseVideoView(LoginRequiredMixin, View):
    '''
    课程视频信息
    '''

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 查询该用户是否已经关联了该课程
        has_learned = UserCourse.objects.filter(user=request.user, course=course)

        if not has_learned:
            new_user_course = UserCourse(user=request.user, course=course)
            new_user_course.save()

        all_resources = CourseResource.objects.filter(course=course)

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取学过该课程的用户 也学过的其他课程，按点击数取得前五名
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-clickNums")[:5]

        ret_dict = {"course": course, 'all_resources': all_resources}
        return render(request, 'course-video.html', ret_dict)


class CourseCommentView(LoginRequiredMixin, View):
    '''
    课程评论信息
    '''

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.filter(course_id=course.id)
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取学过该课程的用户 也学过的其他课程，按点击数取得前五名
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-clickNums")[:5]

        ret_dict = {"course": course, 'all_comments': all_comments, 'relate_courses': relate_courses,
                    'all_resources': all_resources}
        return render(request, 'course-comment.html', ret_dict)


class AddFavCourseView(View):
    '''
    用户收藏以及取消收藏课程
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


class AddCommentView(View):
    '''
    用户添加课程评论
    '''

    def post(self, request):
        # 判断用户是否登录
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail" ,"msg": "用户未登录"}', content_type='application/json')

        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", '')
        if course_id > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success" ,"msg": "添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail" ,"msg": "添加失败"}', content_type='application/json')
