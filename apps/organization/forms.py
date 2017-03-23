# -*- encoding:utf-8 -*-
# --------------------------------
# author : dbird
# create_time : 2017/3/20 0:46
# --------------------------------
import re

from django import forms

from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_moble(self):
        '''验证手机号码是否合法
        :return:
        '''
        mobile = self.clean_data('mobile')
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u'手机号码非法', code="mobile_invalid")
