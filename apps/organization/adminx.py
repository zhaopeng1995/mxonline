# -*- encoding:utf-8 -*-
# --------------------------------
# author : dbird
# create_time : 2017/3/10 20:52
# --------------------------------
# -*- coding: utf-8 -*-
import xadmin
from organization.models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'clickNums','favNums','image','address','city','add_time']
    search_fields = ['name', 'desc', 'clickNums','favNums','image','address','city']
    list_filter = ['name', 'desc', 'clickNums','favNums','image','address','city','add_time']


class TeacherAdmin(object):
    list_display = ['name', 'work_years', 'work_company','work_position','points','clickNums','org','add_time']
    search_fields = ['name', 'work_years', 'work_company','work_position','points','clickNums','org']
    list_filter = ['name', 'work_years', 'work_company','work_position','points','clickNums','org','add_time']

xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)