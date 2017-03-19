# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger

from organization.models import CourseOrg, CityDict


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
