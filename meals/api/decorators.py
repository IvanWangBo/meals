# coding=utf-8
import urllib
import functools

from django.http import HttpResponseRedirect

from base_view import HttpApiBaseView
from common.constants import UserAdminType


class BasePermissionDecorator(HttpApiBaseView):
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, obj_type):
        return functools.partial(self.__call__, obj)

    def __call__(self, *args, **kwargs):
        if len(args) == 2:
            self.request = args[1]
        else:
            self.request = args[0]

        if self.check_permission():
            return self.func(*args, **kwargs)
        else:
            if self.request.is_ajax():
                return self.error_response({}, u"请先登录")
            else:
                return HttpResponseRedirect("/login/?__from=" + urllib.quote(self.request.path))

    def check_permission(self):
        raise NotImplementedError()


class login_required(BasePermissionDecorator):
    def check_permission(self):
        return self.request.user.is_authenticated()


class admin_required(BasePermissionDecorator):
    def check_permission(self):
        return self.request.user.is_authenticated() and self.request.user.admin_type == UserAdminType.admin


class company_required(BasePermissionDecorator):
    def check_permission(self):
        return self.request.user.is_authenticated() and self.request.user.admin_type == UserAdminType.company


class personnel_required(BasePermissionDecorator):
    def check_permission(self):
        return self.request.user.is_authenticated() and self.request.user.admin_type == UserAdminType.personnel
