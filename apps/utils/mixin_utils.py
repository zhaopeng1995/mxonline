# -*- encoding:utf-8 -*-
# --------------------------------
# author : dbird
# create_time : 2017/3/23 11:30
# --------------------------------

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class LoginRequiredMixin(object):

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)