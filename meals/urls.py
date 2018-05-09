# coding=utf-8
import settings
from django.conf.urls import url
from django.contrib import admin
from api.users.views import LoginView
from api.users.views import LogoutView
from api.users.views import RegisterView
from django.views.generic import TemplateView


# 通用返回格式：
# 正确: {"code": 200, "data": data, "message": message}
# 错误: {"code": 401, "data": data, "message": message}

urlpatterns = [
    #url(r'^admin/', admin.site.urls),

    # html
    url(r'^login/$', TemplateView.as_view(template_name="login.html"), name="user_login_page"),
    url(r'^personnel/$', TemplateView.as_view(template_name="personnel/index.html"), name="personnel_index_page"),
    url(r'^admin/$', TemplateView.as_view(template_name="admin/index.html"), name="admin_index_page"),
    url(r'^company/$', TemplateView.as_view(template_name="company/index.html"), name="company_index_page"),
    url(r'^restaurant/$', TemplateView.as_view(template_name="restaurant/index.html"), name="restaurant_index_page"),

    # user api
    url(r'^api/login/$', LoginView.as_view()), # 登录
    url(r'^api/logout/$', LogoutView.as_view()), # 登出
    url(r'^api/register/$', RegisterView.as_view()), # 注册用户
    #data:
    #[{
    #    "company_id": 1001,
    #    "company_name": "xxx",
    #    "admin_account": "admin",
    #    "phone_number": "123456789"
    #}
    #]

    # 点餐


    #
]